#!/usr/bin/env python3
"""Generate the fallback donkey image used on Android versions whose emoji
font predates Unicode 13 (U+1FACF DONKEY, shipped in Android 11).

Run from anywhere:  python3 create_donkey.py
Writes assets/img/donkey.png
"""
import os
from PIL import Image, ImageDraw

S = 4          # supersample factor, for antialiasing
OUT = 512      # final pixel size
GREY = (163, 179, 201, 255)
GREY_D = (143, 163, 191, 255)
EAR_IN = (240, 183, 197, 255)
MUZZLE = (238, 242, 248, 255)
MUZZLE_D = (214, 223, 234, 255)
EYE = (47, 62, 82, 255)
FORELOCK = (107, 125, 153, 255)
NOSTRIL = (123, 140, 166, 255)
CHEEK = (247, 168, 184, 120)

img = Image.new('RGBA', (OUT * S, OUT * S), (0, 0, 0, 0))
d = ImageDraw.Draw(img)


def ell(cx, cy, rx, ry, fill):
    d.ellipse([(cx - rx) * S, (cy - ry) * S, (cx + rx) * S, (cy + ry) * S], fill=fill)


def rot_ell(cx, cy, rx, ry, angle, fill):
    """Rotated ellipse, composited so it can sit at an angle."""
    pad = int(max(rx, ry) * 2.6)
    layer = Image.new('RGBA', (pad * S, pad * S), (0, 0, 0, 0))
    ImageDraw.Draw(layer).ellipse(
        [(pad / 2 - rx) * S, (pad / 2 - ry) * S, (pad / 2 + rx) * S, (pad / 2 + ry) * S],
        fill=fill)
    layer = layer.rotate(angle, resample=Image.BICUBIC)
    # layer is pad*S px and its centre sits at pad*S/2, so offset by cx*S - pad*S/2
    img.alpha_composite(layer, (int((cx - pad / 2) * S), int((cy - pad / 2) * S)))


# long ears first so they sit behind the head
rot_ell(150, 130, 30, 74, 20, GREY)
rot_ell(150, 134, 17, 55, 20, EAR_IN)
rot_ell(362, 130, 30, 74, -20, GREY)
rot_ell(362, 134, 17, 55, -20, EAR_IN)

# head
ell(256, 268, 108, 100, GREY)
ell(256, 300, 104, 92, GREY_D)          # subtle lower shading

# forelock
d.polygon([(256 * S, 172 * S), (214 * S, 232 * S), (256 * S, 214 * S),
           (298 * S, 232 * S)], fill=FORELOCK)

# muzzle
ell(256, 330, 74, 55, MUZZLE)
ell(256, 344, 66, 46, MUZZLE_D)

# nostrils
ell(226, 328, 10, 13, NOSTRIL)
ell(286, 328, 10, 13, NOSTRIL)

# smile
d.arc([226 * S, 322 * S, 286 * S, 366 * S], start=20, end=160,
      fill=NOSTRIL, width=int(6 * S))

# eyes
ell(212, 256, 19, 23, EYE)
ell(300, 256, 19, 23, EYE)
ell(221, 246, 7, 7, (255, 255, 255, 255))
ell(309, 246, 7, 7, (255, 255, 255, 255))

# cheeks
ell(180, 300, 17, 11, CHEEK)
ell(332, 300, 17, 11, CHEEK)

# Trim to the drawn content, then re-centre it with equal margins so the
# subject is optically centred no matter how the coordinates above are tuned.
# Cropping happens at full resolution and the image is downsampled exactly
# once, which avoids the ringing that repeated resampling introduces (and
# keeps the PNG small enough to compress).
bbox = img.getbbox()
subject = img.crop(bbox)
margin = int(OUT * 0.04)
avail = OUT - margin * 2
scale = min(avail / subject.width, avail / subject.height)
nw, nh = max(1, round(subject.width * scale)), max(1, round(subject.height * scale))
subject = subject.resize((nw, nh), Image.BOX)
img = Image.new('RGBA', (OUT, OUT), (0, 0, 0, 0))
img.alpha_composite(subject, ((OUT - nw) // 2, (OUT - nh) // 2))

here = os.path.dirname(os.path.abspath(__file__))
dest = os.path.join(here, 'assets', 'img')
os.makedirs(dest, exist_ok=True)
path = os.path.join(dest, 'donkey.png')
img.save(path, 'PNG', optimize=True)
print(f'donkey.png  {OUT}x{OUT}  {os.path.getsize(path)} bytes  ->  {path}')