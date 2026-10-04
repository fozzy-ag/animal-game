#!/usr/bin/env python3
"""Generate flat-style face images for every animal, for Android versions
whose emoji font is too old to draw them reliably.

Run from anywhere:  python3 create_animals.py
Writes assets/img/<name>.png for all 18 animals.
"""
import os
from PIL import Image, ImageDraw

S = 4           # supersample factor
OUT = 512       # final pixel size
MARGIN = 0.05   # fraction of the canvas kept clear around the subject

# ---------------------------------------------------------------- palette
FUR = {
    'cat': (154, 160, 172), 'dog': (198, 142, 92), 'cow': (246, 246, 250),
    'pig': (247, 168, 190), 'chicken': (250, 240, 222), 'bird': (108, 176,
    224), 'frog': (126, 200, 130), 'lion': (226, 176, 108),
    'monkey': (176, 128, 88), 'sheep': (250, 248, 244), 'goat': (214, 202,
    186), 'horse': (166, 116, 78), 'rabbit': (236, 232, 228),
    'octopus': (240, 142, 130), 'turtle': (108, 178, 122),
    'elephant': (162, 170, 182), 'duck': (250, 214, 96),
}
PINK = (240, 160, 180)
DARK = (58, 62, 74)
WHITE = (255, 255, 255)
CREAM = (250, 240, 214)
ORANGE = (244, 168, 62)
SHADE = (0, 0, 0, 46)          # generic translucent shading


class C:
    """Tiny drawing surface with 0-512 logical coordinates."""

    def __init__(self):
        self.im = Image.new('RGBA', (OUT * S, OUT * S), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)

    def circ(self, cx, cy, r, fill):
        self.d.ellipse([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S],
                       fill=fill)

    def ell(self, cx, cy, rx, ry, fill):
        self.d.ellipse([(cx - rx) * S, (cy - ry) * S, (cx + rx) * S, (cy + ry) * S],
                       fill=fill)

    def poly(self, pts, fill):
        self.d.polygon([(x * S, y * S) for x, y in pts], fill=fill)

    def tri(self, p1, p2, p3, fill):
        self.poly([p1, p2, p3], fill)

    def arc(self, box, start, end, fill, w):
        self.d.arc([v * S for v in box], start, end, fill=fill, width=int(w * S))

    def line(self, pts, fill, w):
        self.d.line([(x * S, y * S) for x, y in pts], fill=fill, width=int(w * S),
                    joint='curve')

    def eyes(self, dx=0, dy=0, r=15, gap=52, cy=245):
        self.circ(256 - gap + dx, cy + dy, r, WHITE)
        self.circ(256 + gap + dx, cy + dy, r, WHITE)
        self.circ(256 - gap + dx + r * 0.22, cy + dy, r * 0.62, DARK)
        self.circ(256 + gap + dx + r * 0.22, cy + dy, r * 0.62, DARK)

    def smile(self, cy=310, w=54, wide=150):
        self.arc((256 - w, cy - w * 0.75, 256 + w, cy + w * 0.75), 20, 160,
                 DARK, 7)

    def finish(self):
        bbox = self.im.getbbox()
        sub = self.im.crop(bbox)
        avail = int(OUT * (1 - MARGIN * 2))
        k = min(avail / sub.width, avail / sub.height)
        nw, nh = max(1, round(sub.width * k)), max(1, round(sub.height * k))
        sub = sub.resize((nw, nh), Image.BOX)
        out = Image.new('RGBA', (OUT, OUT), (0, 0, 0, 0))
        out.alpha_composite(sub, ((OUT - nw) // 2, (OUT - nh) // 2))
        return out


# ---------------------------------------------------------------- animals
def cat(c):
    f = FUR['cat']
    c.tri((150, 200), (168, 96), (232, 176), f)
    c.tri((362, 200), (344, 96), (280, 176), f)
    c.tri((163, 196), (176, 126), (216, 178), PINK)
    c.tri((349, 196), (336, 126), (296, 178), PINK)
    c.circ(256, 250, 128, f)
    c.ell(256, 312, 74, 54, (238, 238, 242))
    c.eyes(r=17, cy=242)
    c.tri((238, 296), (274, 296), (256, 318), PINK)
    c.arc((238, 300, 256, 330), 90, 180, DARK, 6)
    c.arc((256, 300, 274, 330), 0, 90, DARK, 6)
    for dy in (-14, 0, 14):
        c.line([(196, 306 + dy), (96, 288 + dy)], (90, 90, 100, 190), 5)
        c.line([(316, 306 + dy), (416, 288 + dy)], (90, 90, 100, 190), 5)


def dog(c):
    f = FUR['dog']
    c.ell(150, 268, 44, 104, (168, 116, 72))
    c.ell(362, 268, 44, 104, (168, 116, 72))
    c.circ(256, 250, 128, f)
    c.ell(256, 322, 70, 56, (232, 198, 160))
    c.eyes(r=16, cy=238)
    c.ell(256, 312, 27, 21, DARK)
    c.arc((226, 312, 256, 344), 100, 180, DARK, 6)
    c.arc((256, 312, 286, 344), 0, 80, DARK, 6)
    c.tri((150, 176), (186, 132), (206, 188), (168, 116, 72, 0))


def cow(c):
    c.ell(150, 176, 40, 34, CREAM)
    c.ell(362, 176, 40, 34, CREAM)
    c.circ(256, 250, 130, FUR['cow'])
    c.circ(180, 196, 40, (70, 74, 84))
    c.circ(336, 300, 30, (70, 74, 84))
    c.ell(256, 322, 78, 56, PINK)
    c.eyes(r=15, cy=240)
    c.ell(230, 316, 13, 17, (196, 118, 138))
    c.ell(282, 316, 13, 17, (196, 118, 138))


def pig(c):
    f = FUR['pig']
    c.tri((146, 216), (128, 128), (222, 178), (222, 138, 162))
    c.tri((366, 216), (384, 128), (290, 178), (222, 138, 162))
    c.circ(256, 252, 128, f)
    c.eyes(r=15, cy=238)
    c.ell(256, 318, 66, 50, (238, 148, 174))
    c.ell(234, 318, 13, 19, (190, 100, 128))
    c.ell(278, 318, 13, 19, (190, 100, 128))


def chicken(c):
    c.circ(206, 168, 40, (232, 84, 88))
    c.circ(256, 152, 44, (232, 84, 88))
    c.circ(306, 168, 40, (232, 84, 88))
    c.circ(256, 268, 118, FUR['chicken'])
    c.eyes(r=15, cy=238)
    c.tri((256, 286), (196, 300), (256, 330), ORANGE)
    c.circ(190, 306, 20, (238, 148, 168, 110))
    c.circ(322, 306, 20, (238, 148, 168, 110))


def bird(c):
    f = FUR['bird']
    c.ell(300, 350, 96, 74, (86, 152, 200))
    c.circ(256, 250, 122, f)
    c.eyes(r=16, cy=236)
    c.tri((256, 268), (168, 288), (256, 312), ORANGE)
    c.circ(320, 214, 22, (86, 152, 200))


def frog(c):
    f = FUR['frog']
    c.circ(176, 190, 62, f)
    c.circ(336, 190, 62, f)
    c.circ(176, 190, 40, WHITE)
    c.circ(336, 190, 40, WHITE)
    c.circ(176, 190, 24, DARK)
    c.circ(336, 190, 24, DARK)
    c.ell(256, 292, 132, 106, f)
    c.arc((150, 268, 362, 400), 30, 150, (46, 110, 60), 9)


def lion(c):
    f = FUR['lion']
    mane = (196, 142, 74)
    for i in range(14):
        a = i * 25.7
        import math
        c.circ(256 + 132 * math.cos(math.radians(a)),
               262 + 132 * math.sin(math.radians(a)), 42, mane)
    c.circ(256, 262, 116, f)
    c.ell(256, 306, 68, 50, (246, 226, 196))
    c.eyes(r=15, cy=248)
    c.tri((240, 288), (272, 288), (256, 308), DARK)
    c.arc((240, 296, 256, 322), 90, 180, DARK, 5)
    c.arc((256, 296, 272, 322), 0, 90, DARK, 5)


def monkey(c):
    f = FUR['monkey']
    c.circ(146, 258, 48, (140, 98, 64))
    c.circ(366, 258, 48, (140, 98, 64))
    c.circ(256, 258, 122, f)
    c.ell(256, 312, 74, 58, (232, 196, 158))
    c.eyes(r=16, cy=244)
    for dx in (-22, 22):
        c.circ(256 + dx, 314, 5, (140, 98, 64))
    c.arc((232, 302, 256, 330), 90, 180, (140, 98, 64), 6)
    c.arc((256, 302, 280, 330), 0, 90, (140, 98, 64), 6)


def sheep(c):
    wool = FUR['sheep']
    for cx, cy, r in ((150, 200, 62), (256, 168, 66), (362, 200, 62),
                      (128, 292, 58), (384, 292, 58), (196, 128, 54),
                      (316, 128, 54)):
        c.circ(cx, cy, r, wool)
    c.ell(256, 296, 92, 84, (74, 70, 78))
    c.eyes(r=14, cy=286)
    c.ell(244, 336, 9, 12, (48, 44, 52))
    c.ell(268, 336, 9, 12, (48, 44, 52))


def goat(c):
    f = FUR['goat']
    c.arc((150, 108, 246, 244), 150, 330, (150, 138, 122), 17)
    c.arc((266, 108, 362, 244), 210, 30, (150, 138, 122), 17)
    c.tri((238, 372), (274, 372), (256, 452), (238, 226, 210))
    c.circ(256, 268, 118, f)
    c.ell(256, 330, 58, 44, (240, 234, 224))
    c.eyes(r=14, gap=50, cy=252)
    c.ell(248, 322, 8, 11, (130, 118, 108))
    c.ell(264, 322, 8, 11, (130, 118, 108))


def donkey(c):
    for cx, ang in ((150, 20), (362, -20)):
        c.ell(cx, 138, 30, 74, (163, 179, 201))
        c.ell(cx, 142, 17, 55, PINK)
    c.circ(256, 272, 108, (163, 179, 201))
    c.ell(256, 292, 104, 92, (143, 163, 191))
    c.poly([(256, 176), (216, 236), (256, 218), (296, 236)], (107, 125, 153))
    c.ell(256, 334, 74, 55, (238, 242, 248))
    c.eyes(r=19, gap=44, cy=258)
    c.ell(228, 332, 10, 13, (123, 140, 166))
    c.ell(284, 332, 10, 13, (123, 140, 166))
    c.arc((228, 328, 284, 372), 20, 160, (123, 140, 166), 6)


def horse(c):
    f = FUR['horse']
    c.tri((176, 196), (188, 96), (238, 172), f)
    c.tri((336, 196), (324, 96), (274, 172), f)
    c.poly([(256, 92), (216, 176), (232, 214)], (110, 76, 48))
    c.ell(256, 268, 96, 118, f)
    c.ell(256, 336, 68, 56, (216, 176, 142))
    c.eyes(r=15, gap=44, cy=252)
    c.ell(236, 324, 8, 12, (110, 76, 48))
    c.ell(276, 324, 8, 12, (110, 76, 48))


def rabbit(c):
    f = FUR['rabbit']
    c.ell(186, 118, 30, 96, f)
    c.ell(326, 118, 30, 96, f)
    c.ell(186, 124, 17, 72, PINK)
    c.ell(326, 124, 17, 72, PINK)
    c.circ(256, 292, 116, f)
    c.eyes(r=16, cy=282)
    c.tri((240, 338), (272, 338), (256, 358), PINK)
    c.line([(238, 352), (256, 366), (274, 352)], (200, 160, 170), 6)
    c.circ(196, 330, 20, (238, 186, 196, 120))
    c.circ(316, 330, 20, (238, 186, 196, 120))


def octopus(c):
    f = FUR['octopus']
    for i in range(7):
        x = 128 + i * 38
        c.ell(x, 388, 30, 56, f)
        c.circ(x, 430, 26, f)
    c.circ(256, 258, 132, f)
    c.circ(256, 330, 92, (250, 186, 176))
    c.eyes(r=26, gap=52, cy=236)
    c.circ(202, 336, 9, (196, 118, 140))
    c.circ(310, 336, 9, (196, 118, 140))
    c.arc((216, 344, 256, 386), 90, 180, (196, 118, 140), 7)
    c.arc((256, 344, 296, 386), 0, 90, (196, 118, 140), 7)


def turtle(c):
    shell = (86, 150, 104)
    for cx, cy in ((168, 372), (344, 372)):
        c.ell(cx, 382, 42, 30, (122, 184, 138))
    c.ell(256, 342, 176, 122, shell)
    for r, n, col in ((120, 6, (66, 124, 84)), (68, 4, (66, 124, 84))):
        import math
        for i in range(n):
            a = math.radians(i * 360 / n - 90)
            c.circ(256 + r * 0.92 * math.cos(a), 330 + r * 0.62 * math.sin(a),
                   30 if r > 100 else 22, col)
    c.circ(256, 330, 34, (66, 124, 84))
    c.circ(256, 176, 68, (132, 194, 146))
    c.eyes(r=15, gap=28, cy=168)
    c.arc((238, 196, 274, 224), 20, 160, (86, 150, 104), 6)


def elephant(c):
    f = FUR['elephant']
    c.ell(132, 268, 82, 106, (146, 154, 168))
    c.ell(380, 268, 82, 106, (146, 154, 168))
    c.ell(256, 250, 106, 100, f)
    c.ell(256, 396, 40, 82, f)
    c.ell(256, 300, 78, 70, (188, 196, 206))
    c.tri((206, 322), (222, 396), (238, 322), (250, 246, 234))
    c.tri((274, 322), (290, 396), (306, 322), (250, 246, 234))
    c.eyes(r=14, gap=46, cy=244)


def duck(c):
    c.circ(256, 246, 120, FUR['duck'])
    c.ell(256, 344, 92, 50, ORANGE)
    c.ell(256, 330, 92, 40, (250, 186, 84))
    c.eyes(r=16, cy=226)
    c.circ(300, 190, 26, (250, 186, 84))


DRAW = {
    'cat': cat, 'dog': dog, 'cow': cow, 'pig': pig, 'chicken': chicken,
    'bird': bird, 'frog': frog, 'lion': lion, 'monkey': monkey,
    'sheep': sheep, 'goat': goat, 'donkey': donkey, 'horse': horse,
    'rabbit': rabbit, 'octopus': octopus, 'turtle': turtle,
    'elephant': elephant, 'duck': duck,
}

if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__))
    dest = os.path.join(here, 'assets', 'img')
    os.makedirs(dest, exist_ok=True)
    total = 0
    for name, fn in DRAW.items():
        c = C()
        fn(c)
        img = c.finish()
        p = os.path.join(dest, f'{name}.png')
        img.save(p, 'PNG', optimize=True)
        sz = os.path.getsize(p)
        total += sz
        print(f'  {name:<10} {OUT}x{OUT}  {sz:>6} bytes')
    print(f'\n  {len(DRAW)} images, {total} bytes total  ->  {dest}')