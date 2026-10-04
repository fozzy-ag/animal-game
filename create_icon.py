#!/usr/bin/env python3
"""Generate the launcher icon.

Written with struct/zlib rather than Pillow so it runs on a bare Termux
install with no Python packages.

The palette is configurable because the repo ships two apps that sit side by
side on the launcher: main is the emoji build, android7-images is the
Android 7-10 image build. Identical icons with different labels is a
reliable way to open the wrong one, so the legacy build passes its own
colours. Defaults reproduce the original orange icon byte for byte.

  python3 create_icon.py
  python3 create_icon.py --from '#2f7fb5' --to '#7fd4e8' --paw '#12303f'
"""
import argparse
import math
import os
import struct
import zlib


def parse_color(text):
    text = text.lstrip('#')
    if len(text) != 6:
        raise argparse.ArgumentTypeError('expected #rrggbb, got %r' % text)
    try:
        return tuple(int(text[i:i + 2], 16) for i in (0, 2, 4))
    except ValueError:
        raise argparse.ArgumentTypeError('not a hex colour: %r' % text)


def create_png(w, h, pixels):
    def chunk(ctype, data):
        c = ctype + data
        return struct.pack('>I', len(data)) + c + struct.pack('>I', zlib.crc32(c) & 0xffffffff)
    sig = b'\x89PNG\r\n\x1a\n'
    ihdr = struct.pack('>IIBBBBB', w, h, 8, 6, 0, 0, 0)
    raw = b''
    for y in range(h):
        raw += b'\x00'
        for x in range(w):
            raw += bytes(pixels[y * w + x])
    idat = zlib.compress(raw)
    return sig + chunk(b'IHDR', ihdr) + chunk(b'IDAT', idat) + chunk(b'IEND', b'')


def lerp(a, b, t):
    return int(a + (b - a) * t)


def make_icon(w, h, top, bottom, paw):
    pixels = []
    cx, cy = w / 2, h / 2
    for y in range(h):
        for x in range(w):
            dx, dy = x - cx, y - cy
            dist = math.sqrt(dx*dx + dy*dy)
            radius = w * 0.45

            if dist < radius:
                # Gradient background, corner to corner.
                t = (dx + dy) / (w * 0.9)
                t = max(0, min(1, (t + 1) / 2))
                r = lerp(top[0], bottom[0], t)
                g = lerp(top[1], bottom[1], t)
                b = lerp(top[2], bottom[2], t)

                # Paw pad (center)
                paw_dist = math.sqrt(dx*dx + (dy - h*0.02)**2)
                paw_r = w * 0.18
                if paw_dist < paw_r:
                    r, g, b = paw

                # Toe beans
                toe_positions = [
                    (-w*0.12, -h*0.15, w*0.07),
                    (w*0.12, -h*0.15, w*0.07),
                    (-w*0.2, -h*0.02, w*0.06),
                    (w*0.2, -h*0.02, w*0.06),
                ]
                for tx, ty, tr in toe_positions:
                    td = math.sqrt((dx - tx)**2 + (dy - ty)**2)
                    if td < tr:
                        r, g, b = paw

                # Anti-alias edge
                if dist > radius - 1:
                    alpha = max(0, min(255, int(255 * (radius - dist + 1))))
                    pixels.append((r, g, b, alpha))
                else:
                    pixels.append((r, g, b, 255))
            else:
                pixels.append((0, 0, 0, 0))

    return create_png(w, h, pixels)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--from', dest='top', type=parse_color, default=parse_color('#ff7832'),
                    help='gradient start, #rrggbb (default #ff7832)')
    ap.add_argument('--to', dest='bottom', type=parse_color, default=parse_color('#ffdc32'),
                    help='gradient end, #rrggbb (default #ffdc32)')
    ap.add_argument('--paw', type=parse_color, default=parse_color('#3c281e'),
                    help='paw print colour, #rrggbb (default #3c281e)')
    args = ap.parse_args()

    sizes = {
        'mdpi': 48,
        'hdpi': 72,
        'xhdpi': 96,
        'xxhdpi': 144,
    }

    base = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'res')
    for density, size in sizes.items():
        d = f'{base}/mipmap-{density}'
        os.makedirs(d, exist_ok=True)
        data = make_icon(size, size, args.top, args.bottom, args.paw)
        path = os.path.join(d, 'ic_launcher.png')
        with open(path, 'wb') as f:
            f.write(data)
        print(f'{density}: {size}x{size} -> {len(data)} bytes')

    print('Icons created!')


if __name__ == '__main__':
    main()
