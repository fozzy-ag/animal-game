#!/usr/bin/env python3
import struct, zlib, os, math

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

def make_icon(w, h):
    pixels = []
    cx, cy = w / 2, h / 2
    for y in range(h):
        for x in range(w):
            dx, dy = x - cx, y - cy
            dist = math.sqrt(dx*dx + dy*dy)
            radius = w * 0.45
            
            if dist < radius:
                # Gradient background: warm orange to yellow
                t = (dx + dy) / (w * 0.9)
                t = max(0, min(1, (t + 1) / 2))
                r = lerp(255, 255, t)
                g = lerp(120, 220, t)
                b = lerp(50, 50, t)
                
                # Paw pad (center)
                paw_dist = math.sqrt(dx*dx + (dy - h*0.02)**2)
                paw_r = w * 0.18
                if paw_dist < paw_r:
                    r, g, b = 60, 40, 30
                
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
                        r, g, b = 60, 40, 30
                
                # Anti-alias edge
                if dist > radius - 1:
                    alpha = max(0, min(255, int(255 * (radius - dist + 1))))
                    pixels.append((r, g, b, alpha))
                else:
                    pixels.append((r, g, b, 255))
            else:
                pixels.append((0, 0, 0, 0))
    
    return create_png(w, h, pixels)

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
    data = make_icon(size, size)
    path = os.path.join(d, 'ic_launcher.png')
    with open(path, 'wb') as f:
        f.write(data)
    print(f'{density}: {size}x{size} -> {len(data)} bytes')

print('Icons created!')
