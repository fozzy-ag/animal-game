#!/usr/bin/env python3
"""Fetch the animal artwork from Noto Color Emoji and normalise it.

Why: Android 7-10 cannot draw U+1FACF DONKEY (Unicode 13) or reliably draw
U+1F986 DUCK (Unicode 9.0, marginal on 7.0), so the image build of the app
ships artwork instead of relying on the system emoji font.

Source: Noto Color Emoji 2D bitmaps, googlefonts/noto-emoji, 2D/png/512/.
Licence: Apache License 2.0, Copyright 2013 Google, Inc. See CREDITS.md.
This is the same artwork Android 11+ would have drawn from its own font, so
the picture matches the emoji version of the app instead of imitating it.

Normalisation matters as much as the download. Noto positions each glyph at
its natural position inside the em square, so the artwork is not centred and
not consistently scaled: the turtle sat 36px off centre and six others
drifted 14-24px, which would make animals visibly jump around while
swiping. Each image is therefore cropped to its alpha bounding box and
re-centred at a common size, exactly as the hand-drawn set was.

Run from anywhere:  python3 fetch_emoji_images.py
"""
import os
import subprocess
import sys

from PIL import Image

BASE = 'https://raw.githubusercontent.com/googlefonts/noto-emoji/main/2D/png/512'
SIZE = 512      # final canvas
MARGIN = 0.05   # fraction of the canvas kept clear around the subject
RETRIES = 3

# id -> (codepoint, German name). The id must match the sound name in
# assets/game.html, since showAnimal() builds the path as img + '.png'.
ANIMALS = [
    ('cat',      '1f431', 'Katze'),
    ('dog',      '1f436', 'Hund'),
    ('cow',      '1f42e', 'Kuh'),
    ('pig',      '1f437', 'Schwein'),
    ('chicken',  '1f414', 'Huhn'),
    ('bird',     '1f426', 'Vogel'),
    ('frog',     '1f438', 'Frosch'),
    ('lion',     '1f981', 'Löwe'),
    ('monkey',   '1f435', 'Affe'),
    ('sheep',    '1f411', 'Schaf'),
    ('goat',     '1f410', 'Ziege'),
    ('donkey',   '1facf', 'Esel'),
    ('horse',    '1f40e', 'Pferd'),
    ('rabbit',   '1f430', 'Hase'),
    ('octopus',  '1f419', 'Oktopus'),
    ('turtle',   '1f422', 'Schildkröte'),
    ('elephant', '1f418', 'Elefant'),
    ('duck',     '1f986', 'Ente'),
]


def fetch(url, dest):
    for attempt in range(1, RETRIES + 1):
        r = subprocess.run(
            ['curl', '-sS', '-f', '--max-time', '40', '-o', dest, url],
            capture_output=True, text=True)
        if r.returncode == 0 and os.path.getsize(dest) > 0:
            return True
        if os.path.exists(dest):
            os.remove(dest)
        print('    attempt %d/%d failed: %s'
              % (attempt, RETRIES, r.stderr.strip()[:70]), file=sys.stderr)
    return False


def normalise(src):
    """Crop to the alpha bounding box, then re-centre at a common size."""
    im = Image.open(src).convert('RGBA')
    bbox = im.getbbox()
    if bbox is None:
        raise ValueError('image is fully transparent')
    sub = im.crop(bbox)
    avail = int(SIZE * (1 - MARGIN * 2))
    k = min(avail / sub.width, avail / sub.height)
    nw, nh = max(1, round(sub.width * k)), max(1, round(sub.height * k))
    # LANCZOS rather than BOX: these are 512px bitmaps with fine detail and
    # curved edges, where BOX would alias.
    sub = sub.resize((nw, nh), Image.LANCZOS)
    out = Image.new('RGBA', (SIZE, SIZE), (0, 0, 0, 0))
    out.alpha_composite(sub, ((SIZE - nw) // 2, (SIZE - nh) // 2))
    return out


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    dest = os.path.join(here, 'assets', 'img')
    os.makedirs(dest, exist_ok=True)
    tmp = os.path.join(here, 'sounds', 'candidates', 'noto-raw')
    os.makedirs(tmp, exist_ok=True)

    total, failed = 0, []
    for aid, cp, name in ANIMALS:
        raw = os.path.join(tmp, '%s-u%s.png' % (aid, cp))
        url = '%s/emoji_u%s.png' % (BASE, cp)
        if not fetch(url, raw):
            print('  %-10s DOWNLOAD FAILED' % aid)
            failed.append(aid)
            continue
        out = os.path.join(dest, '%s.png' % aid)
        normalise(raw).save(out, 'PNG', optimize=True)
        sz = os.path.getsize(out)
        total += sz
        print('  %-10s U+%s %-13s %6d bytes' % (aid, cp.upper(), name, sz))

    print('\n  %d images, %d bytes total  ->  %s' % (len(ANIMALS), total, dest))
    if failed:
        print('  FAILED: %s' % ', '.join(failed))
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
