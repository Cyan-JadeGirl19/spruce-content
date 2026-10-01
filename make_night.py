#!/usr/bin/env python3
"""v2 — real-pixel day->night with silhouette-anchored C9 strings.
Roof edge auto-detected from the day photo; bulbs hang right on the eave."""
import math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

SRC = '/home/user/spruce/assets/bg/sl_house_day.jpg'
OUT = '/home/user/spruce/assets/bg/sl_house_night_real.jpg'
W, H = 1536, 1024

day = Image.open(SRC).convert('RGB').resize((W, H), Image.LANCZOS)
arr = np.asarray(day).astype(np.float32)
lum = arr.mean(axis=2)

# ---------- roof silhouette: first dark pixel from top, per x ----------
sil = {}
for xx in range(180, W - 40):
    col = lum[:, xx]
    for yy in range(180, 700):
        if col[yy] < 95 and col[yy + 2] < 110 and col[yy + 5] < 120:
            sil[xx] = yy
            break

def edge(x):
    """smoothed silhouette y at x"""
    xs = [sil[i] for i in range(max(180, x - 6), min(W - 41, x + 7)) if i in sil]
    return int(np.median(xs)) if xs else None

# ---------- 1. night grade: deep blue dusk ----------
xx = np.linspace(0, 1, W)[None, :].repeat(H, 0)
yy = np.arange(H)[:, None].repeat(W, 1).astype(np.float32) / H
sky = np.clip((330 - yy * H) / 330, 0, 1)                       # sky zone weight
mult = 1.0 - 0.68 * (1 - sky * 0.45) - 0.10 * sky               # darken ground+sky
night = arr * mult[..., None]
tint_sky = np.array([0.62, 0.74, 1.18])                          # navy sky
tint_gnd = np.array([0.84, 0.90, 1.10])                          # cool ground
tint = tint_gnd[None, None, :] * (1 - sky[..., None]) + tint_sky[None, None, :] * sky[..., None]
night = night * tint
img = Image.fromarray(night.clip(0, 255).astype(np.uint8))

# stars in the upper sky
st = Image.new('RGBA', (W, H), (0, 0, 0, 0))
sd = ImageDraw.Draw(st)
rnd = random.Random(4)
for _ in range(90):
    sx, sy = rnd.uniform(320, W - 20), rnd.uniform(10, 240)
    r = rnd.uniform(0.6, 1.6)
    sd.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(220, 228, 255, rnd.randint(60, 150)))
img.paste(Image.alpha_composite(img.convert('RGBA'), st).convert('RGB'), (0, 0))

# ---------- 2. C9 strings anchored to detected eave ----------
bulbs = Image.new('RGB', (W, H), (0, 0, 0))
glowl = Image.new('RGB', (W, H), (0, 0, 0))
bd = ImageDraw.Draw(bulbs); gd = ImageDraw.Draw(glowl)

def string(x0, x1, y_off=9, step=13, use_edge=True, pts=None):
    P = []
    if pts:
        for (a, b) in pts: P.append((a, b))
    else:
        for xx2 in range(int(x0), int(x1) + 1, 4):
            ey = edge(xx2)
            if ey is not None:
                P.append((xx2, ey + y_off))
    for i in range(len(P) - 1):
        ax, ay = P[i]; bx2, by2 = P[i + 1]
        d = math.hypot(bx2 - ax, by2 - ay)
        n = max(1, int(d / step))
        for k in range(n):
            t = k / n
            px, py = ax + (bx2 - ax) * t, ay + (by2 - ay) * t
            j = rnd.randint(-5, 5)
            c = tuple(min(255, v + rnd.randint(-10, 8)) for v in (255, 224, 160))
            bd.ellipse([px - 3.2, py - 3.2, px + 3.2, py + 3.2], fill=c)
            gd.ellipse([px - 8, py - 8, px + 8, py + 8], fill=(210, 150, 80))

# left block eave + center gable: manual (tree branches break auto-detection)
string(0, 0, pts=[(210, 411), (528, 373)])
string(0, 0, pts=[(532, 372), (752, 247), (900, 395)])
string(910, 1420, y_off=10)
# garage gable: manual pts nudged onto trim
for seg in ([(926, 486), (1036, 440)], [(1036, 440), (1146, 482)]):
    (ax, ay), (bx2, by2) = seg
    n = int(math.hypot(bx2 - ax, by2 - ay) / 12)
    for k in range(n):
        t = k / n
        px, py = ax + (bx2 - ax) * t, ay + (by2 - ay) * t
        bd.ellipse([px - 3.2, py - 3.2, px + 3.2, py + 3.2], fill=(255, 226, 164))
        gd.ellipse([px - 8, py - 8, px + 8, py + 8], fill=(210, 150, 80))

# window warm traces (inset, subtle)
def rect_string(x0, y0, x1, y1, step=11):
    for (a, b, c2, d2) in [(x0, y0, x1, y0), (x1, y0, x1, y1), (x1, y1, x0, y1), (x0, y1, x0, y0)]:
        n = max(1, int(math.hypot(c2 - a, d2 - b) / step))
        for k in range(n):
            t = k / n
            px, py = a + (c2 - a) * t, b + (d2 - b) * t
            bd.ellipse([px - 2.6, py - 2.6, px + 2.6, py + 2.6], fill=(255, 218, 150))
            gd.ellipse([px - 6, py - 6, px + 6, py + 6], fill=(170, 120, 62))

for (x0, y0, x1, y1) in [(292, 429, 329, 495), (448, 429, 485, 495),
                          (717, 429, 763, 495), (805, 429, 853, 495)]:
    rect_string(x0, y0, x1, y1)

# ---------- 3. glows ----------
wg = Image.new('RGB', (W, H), (0, 0, 0))
wd = ImageDraw.Draw(wg)
# lit windows (muted)
for (x0, y0, x1, y1) in [(294, 431, 327, 493), (450, 431, 483, 493),
                          (719, 431, 761, 493), (807, 431, 851, 493)]:
    wd.rounded_rectangle([x0, y0, x1, y1], 5, fill=(86, 62, 32))
wd.rounded_rectangle([571, 455, 607, 490], 5, fill=(70, 50, 28))       # upper arch window
wd.rectangle([583, 596, 633, 700], fill=(60, 44, 26))                   # door glass
for sx in (538, 654):                                                   # sconces
    wd.ellipse([sx - 6, 562, sx + 6, 586], fill=(120, 85, 42))
# path lights
for i in range(6):
    t = i / 5
    px = 852 - t * 80; py = 760 + t * 240
    wd.ellipse([px - 26, py - 15, px + 26, py + 15], fill=(46, 33, 16))
    bd.ellipse([px - 2.4, py - 4, px + 2.4, py + 1], fill=(255, 224, 164))
# tree uplight + shrubs
wd.ellipse([40, 660, 240, 900], fill=(64, 46, 24))
for bx in range(180, 940, 105):
    wd.ellipse([bx - 34, 706, bx + 34, 758], fill=(34, 25, 14))
wg = wg.filter(ImageFilter.GaussianBlur(16))

# ---------- 4. composite ----------
def screen(base, add):
    a = np.asarray(base).astype(np.float32) / 255
    b = np.asarray(add).astype(np.float32) / 255
    return Image.fromarray((255 - (255 - a * 255) * (255 - b * 255) / 255).clip(0, 255).astype(np.uint8))

img = screen(img, wg)
img = screen(img, glowl.filter(ImageFilter.GaussianBlur(6)))
img = screen(img, bulbs.filter(ImageFilter.GaussianBlur(1.0)))
img = screen(img, bulbs)

# vignette
vig = Image.new('L', (W, H), 0)
vd = ImageDraw.Draw(vig)
vd.ellipse([-W * 0.22, -H * 0.3, W * 1.22, H * 1.28], fill=255)
vig = vig.filter(ImageFilter.GaussianBlur(150))
img = Image.composite(img, Image.new('RGB', (W, H), (3, 7, 16)), vig)
img.save(OUT, quality=92)
print('v2 night written')
