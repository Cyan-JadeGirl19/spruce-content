#!/usr/bin/env python3
"""Spruce Lights business card — 3.5x2.0in + 0.125in bleed, 300 DPI (1125x675).
Website Edition palette: dark pine, cream Playfair serif, gold accents, sage text.
Front: logo-led with serif tagline. Back: contact block with site badge."""
import os, math
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = '/home/user/spruce'
OUT = f'{ROOT}/business_card'
os.makedirs(OUT, exist_ok=True)

W, H = 1125, 675                 # 3.75 x 2.25 in @ 300dpi (includes bleed)
DPI = 300
TRIM = 37                        # 0.125 in bleed each side
SAFE = 75                        # keep live content inside this

PINE   = (13, 27, 16)            # site dark pine
PINE_L = (22, 42, 26)
CREAM  = (246, 240, 226)
SAGE   = (164, 178, 156)
GOLD   = (240, 176, 45)
DK     = (13, 25, 15)

FONTS = f'{ROOT}/assets/fonts'
def F(size, weight="Bold"):
    return ImageFont.truetype(f"{FONTS}/Poppins-{weight}.ttf", size)
_SFC = {}
def SF(size, wght=700, italic=False):
    k = (size, wght, italic)
    if k not in _SFC:
        fn = f"{FONTS}/PlayfairDisplay-Italic.ttf" if italic else f"{FONTS}/PlayfairDisplay.ttf"
        f = ImageFont.truetype(fn, size)
        try: f.set_variation_by_axes([wght])
        except Exception: pass
        _SFC[k] = f
    return _SFC[k]

def rich(d, cx, y, segs, font, lh=None):
    """centered rich text: segs = [(text, color), ...]; returns new y"""
    total = sum(d.textlength(t, font=font) for t, _ in segs)
    x = cx - total / 2
    for t, c in segs:
        d.text((x, y), t, font=font, fill=c, anchor="lm")
        x += d.textlength(t, font=font)
    return y + (lh or font.size * 1.25)

def caps_tracked(d, cx, y, text, font, fill, tracking=3):
    w = sum(d.textlength(ch, font=font) + tracking for ch in text) - tracking
    x = cx - w / 2
    for ch in text:
        d.text((x, y), ch, font=font, fill=fill, anchor="lm")
        x += d.textlength(ch, font=font) + tracking

def glow(img, cx, cy, r, color, peak=42):
    g = Image.new('L', (256, 256), 0)
    gd = ImageDraw.Draw(g)
    for i in range(128, 0, -2):
        a = int(peak * (1 - i / 128))
        gd.ellipse([128 - i, 128 - i, 128 + i, 128 + i], fill=a)
    g = g.resize((r * 2, r * 2))
    ov = Image.new('RGBA', img.size, (0, 0, 0, 0))
    ov.paste(Image.new('RGBA', (r * 2, r * 2), color + (255,)), (cx - r, cy - r), g)
    img.alpha_composite(ov)
    return img

def sparkles(img, n, seed, ymax, cmax=88):
    rnd = __import__('random').Random(seed)
    ov = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for _ in range(n):
        x, y = rnd.uniform(30, W - 30), rnd.uniform(30, ymax)
        r = rnd.uniform(2.0, 5.0)
        c = GOLD if rnd.random() < 0.6 else CREAM
        a = rnd.randint(30, cmax)
        d.line([(x - r * 2.2, y), (x + r * 2.2, y)], fill=c + (a,), width=1)
        d.line([(x, y - r * 2.2), (x, y + r * 2.2)], fill=c + (a,), width=1)
        d.ellipse([x - r * .5, y - r * .5, x + r * .5, y + r * .5], fill=c + (min(255, a + 60),))
    img.alpha_composite(ov.filter(ImageFilter.GaussianBlur(0.6)))
    return img

def card_base(strand_top=True):
    img = Image.new('RGBA', (W, H), PINE + (255,))
    # vertical gradient pine
    gr = Image.new('L', (1, H))
    for y in range(H):
        gr.putpixel((0, y), int(255 * (y / H) ** 1.2))
    gr = gr.resize((W, H))
    img.paste(Image.new('RGB', (W, H), (7, 15, 9)), (0, 0), gr)
    img = glow(img, W // 2, int(H * 0.36), 420, PINE_L, peak=36)
    if strand_top:
        s = __import__('spruce_kit').bulb_strand(W, 9, 44, bulb=16, seed=7)
        img.alpha_composite(s, (0, -8))
    img = sparkles(img, 26, 11, H - 60)
    # gold hairline frame (inside trim, decorative)
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([72, 72, W - 72, H - 72], 26, outline=GOLD + (110,), width=2)
    return img

def dot(d, x, y, r=5.5, c=GOLD):
    d.ellipse([x - r, y - r, x + r, y + r], fill=c)

# ================================================================ FRONT
front = card_base(strand_top=True)
d = ImageDraw.Draw(front)
import spruce_kit
logo = spruce_kit.load_logo(spruce_kit.SL, light_bg=False)   # winter-white wordmark, color bulbs/hat
lw = 470
lg = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)
front.alpha_composite(lg, (W // 2 - lg.width // 2, 148))
d = ImageDraw.Draw(front)
# serif tagline — gold emphasis like the site headline
f_tag = SF(43, 700)
y = 486
rich(d, W // 2, y, [("Your home, ", CREAM), ("aglow", GOLD), (" all season long.", CREAM)], f_tag)
caps_tracked(d, W // 2, 556, "HOLIDAY LIGHTING & EVENTS", F(20, "SemiBold"), SAGE, tracking=6)
front.convert('RGB').save(f'{OUT}/SL_card_FRONT.png', dpi=(DPI, DPI))

# ================================================================ BACK
back = card_base(strand_top=False)
d = ImageDraw.Draw(back)
# site badge (from sprucelights.com hero)
f_b = F(19, "SemiBold")
btxt = "THE SOUTHEAST'S #1 CHRISTMAS LIGHT INSTALLATION SERVICE"
bw = sum(d.textlength(c, font=f_b) + 1.6 for c in btxt) - 1.6 + 88
bx0 = W / 2 - bw / 2
d.rounded_rectangle([bx0, 102, bx0 + bw, 148], 23, fill=DK + (215,), outline=GOLD + (150,), width=2)
dot(d, bx0 + 30, 125, 5)
caps_tracked(d, W / 2 + 14, 124, btxt, f_b, GOLD, tracking=1.6)
# headline
f_h = SF(56, 760)
rich(d, W // 2, 226, [("Let's ", CREAM), ("Light Up", GOLD), (" Your Holidays", CREAM)], f_h)
d = ImageDraw.Draw(back)
d.line([(W/2 - 70, 282), (W/2 + 70, 282)], fill=GOLD + (200,), width=4)
# contact rows
rows = [
    ("(864) 288-2459", F(37, "SemiBold"), CREAM, 338),
    ("sprucelights.com", F(31, "SemiBold"), GOLD, 392),
    ("@spruceholidaylighting", F(26, "Medium"), SAGE, 438),
]
for txt, f, c, yy in rows:
    tw = d.textlength(txt, font=f)
    dot(d, W/2 - tw/2 - 26, yy - 2, 4.5)
    d.text((W/2, yy), txt, font=f, fill=c, anchor="mm")
d.text((W/2, 492), "Greenville  •  Upstate SC  •  Grand Strand  •  Western NC",
       font=F(21, "Regular"), fill=SAGE, anchor="mm")
# bottom strand hugging trim
s = __import__('spruce_kit').bulb_strand(W, 9, 44, bulb=16, seed=7).transpose(Image.FLIP_TOP_BOTTOM)
back.alpha_composite(s, (0, H - s.height + 8))
back.convert('RGB').save(f'{OUT}/SL_card_BACK.png', dpi=(DPI, DPI))

# ================================================================ PDF (2 pages, 300dpi)
f_img = Image.open(f'{OUT}/SL_card_FRONT.png')
b_img = Image.open(f'{OUT}/SL_card_BACK.png')
f_img.save(f'{OUT}/SL_business_card.pdf', save_all=True, append_images=[b_img], resolution=DPI)

# ================================================================ MOCKUP
MW, MH = 1600, 1000
m = Image.new('RGB', (MW, MH), (10, 19, 12))
gr = Image.new('L', (1, MH))
for y in range(MH):
    gr.putpixel((0, y), int(255 * (y / MH) ** 1.3))
m.paste(Image.new('RGB', (MW, MH), (6, 13, 8)), (0, 0), gr.resize((MW, MH)))
m = glow(m.convert('RGBA'), MW//2, 380, 700, PINE_L, 30).convert('RGB')
m = sparkles(m.convert('RGBA'), 40, 5, MH - 40, 70).convert('RGB')

def place(base, card, cx, cy, ang, scale=1.0, shadow=True):
    c = card.resize((int(card.width * scale), int(card.height * scale)), Image.LANCZOS)
    c = c.rotate(ang, expand=True, resample=Image.BICUBIC)
    if shadow:
        sh = Image.new('RGBA', (c.width + 60, c.height + 60), (0, 0, 0, 0))
        ImageDraw.Draw(sh).rounded_rectangle([30, 34, c.width + 30, c.height + 30], 30, fill=(0, 0, 0, 150))
        sh = sh.filter(ImageFilter.GaussianBlur(22))
        base.paste(Image.new('RGB', sh.size, (0, 0, 0)), (cx - c.width//2 - 30, cy - c.height//2 - 30), sh)
    base.paste(c, (cx - c.width // 2, cy - c.height // 2), c if c.mode == 'RGBA' else None)

fr = Image.open(f'{OUT}/SL_card_FRONT.png').convert('RGBA')
bk = Image.open(f'{OUT}/SL_card_BACK.png').convert('RGBA')
place(m, bk, int(MW * 0.68), int(MH * 0.52), 5, 0.94)
place(m, fr, int(MW * 0.36), int(MH * 0.50), -7, 0.98)
d = ImageDraw.Draw(m)
d.text((MW // 2, MH - 46), "SPRUCE LIGHTS — BUSINESS CARD  ·  3.5×2 in + bleed  ·  Website Edition palette",
       font=F(22, "SemiBold"), fill=(150, 170, 152), anchor="mm")
m.save(f'{OUT}/SL_card_mockup.jpg', quality=90)
print('business card set written to', OUT)
