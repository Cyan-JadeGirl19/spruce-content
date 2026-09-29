#!/usr/bin/env python3
"""Business card variants — SL black, SP teal (brand), SP black + family mockup.
Same 3.5x2in +0.125in bleed, 300 DPI system as the original SL pine card."""
import os, random
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import spruce_kit

ROOT = '/home/user/spruce'
OUT = f'{ROOT}/business_card'
os.makedirs(OUT, exist_ok=True)
W, H, DPI = 1125, 675, 300
FONTS = f'{ROOT}/assets/fonts'

GOLD  = (240, 176, 45)
CYAN  = (28, 200, 208)
LIME  = (144, 208, 0)
CREAM = (246, 240, 226)
SAGE  = (164, 178, 156)
DK    = (13, 25, 15)

def F(s, w="Bold"):
    return ImageFont.truetype(f"{FONTS}/Poppins-{w}.ttf", s)
_SFC = {}
def SF(s, wght=700):
    k = (s, wght)
    if k not in _SFC:
        f = ImageFont.truetype(f"{FONTS}/PlayfairDisplay.ttf", s)
        try: f.set_variation_by_axes([wght])
        except Exception: pass
        _SFC[k] = f
    return _SFC[k]

def rich(d, cx, y, segs, font, lh=None):
    total = sum(d.textlength(t, font=font) for t, _ in segs)
    x = cx - total / 2
    for t, c in segs:
        d.text((x, y), t, font=font, fill=c, anchor="lm")
        x += d.textlength(t, font=font)
    return y + (lh or font.size * 1.25)

def caps_tracked(d, cx, y, text, font, fill, tracking=3):
    w = sum(d.textlength(c, font=font) + tracking for c in text) - tracking
    x = cx - w / 2
    for c in text:
        d.text((x, y), c, font=font, fill=fill, anchor="lm")
        x += d.textlength(c, font=font) + tracking

def glow(img, cx, cy, r, color, peak=36):
    g = Image.new('L', (256, 256), 0)
    gd = ImageDraw.Draw(g)
    for i in range(128, 0, -2):
        gd.ellipse([128 - i, 128 - i, 128 + i, 128 + i], fill=int(peak * (1 - i / 128)))
    g = g.resize((r * 2, r * 2))
    ov = Image.new('RGBA', img.size, (0, 0, 0, 0))
    ov.paste(Image.new('RGBA', (r * 2, r * 2), color + (255,)), (cx - r, cy - r), g)
    img.alpha_composite(ov)
    return img

def sparkles(img, n, seed, ymax, cmax=80, accent=GOLD):
    rnd = random.Random(seed)
    ov = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for _ in range(n):
        x, y = rnd.uniform(30, W - 30), rnd.uniform(30, ymax)
        r = rnd.uniform(2.0, 5.0)
        c = accent if rnd.random() < 0.6 else CREAM
        a = rnd.randint(28, cmax)
        d.line([(x - r * 2.2, y), (x + r * 2.2, y)], fill=c + (a,), width=1)
        d.line([(x, y - r * 2.2), (x, y + r * 2.2)], fill=c + (a,), width=1)
        d.ellipse([x - r * .5, y - r * .5, x + r * .5, y + r * .5], fill=c + (min(255, a + 60),))
    img.alpha_composite(ov.filter(ImageFilter.GaussianBlur(0.6)))
    return img

def grad_surface(base, dark, glowc, frame, strand=None, strand_bottom=False, accent=GOLD, frame_w=2):
    img = Image.new('RGBA', (W, H), base + (255,))
    gr = Image.new('L', (1, H))
    for y in range(H):
        gr.putpixel((0, y), int(255 * (y / H) ** 1.2))
    img.paste(Image.new('RGB', (W, H), dark), (0, 0), gr.resize((W, H)))
    img = glow(img, W // 2, int(H * 0.36), 420, glowc, peak=32)
    img = sparkles(img, 22, 11, H - 60, accent=accent)
    if strand:
        s = spruce_kit.bulb_strand(W, 9, 44, bulb=16, seed=7)
        if strand_bottom:
            s = s.transpose(Image.FLIP_TOP_BOTTOM)
            img.alpha_composite(s, (0, H - s.height + 8))
        else:
            img.alpha_composite(s, (0, -8))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([72, 72, W - 72, H - 72], 26, outline=frame + (120,), width=frame_w)
    return img

def grad_line(d, cx, y, half=70, c0=CYAN, c1=LIME, width=5):
    for x in range(-half, half):
        t = (x + half) / (2 * half)
        c = tuple(int(c0[i] + (c1[i] - c0[i]) * t) for i in range(3))
        d.line([(cx + x, y - width // 2), (cx + x, y + width // 2)], fill=c)

def dot(d, x, y, r=4.5, c=GOLD):
    d.ellipse([x - r, y - r, x + r, y + r], fill=c)

def contact_rows(d, rows, dotc):
    for txt, f, c, yy in rows:
        tw = d.textlength(txt, font=f)
        dot(d, W/2 - tw/2 - 26, yy - 2, 4.5, dotc)
        d.text((W/2, yy), txt, font=f, fill=c, anchor="mm")

# ================================================================ SPRUCE LIGHTS (black)
def sl_card(surface='black'):
    logo = spruce_kit.load_logo(spruce_kit.SL, light_bg=False)
    lw = 470
    lg = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)

    front = grad_surface((15, 15, 17), (6, 6, 8), (46, 40, 26), GOLD, strand=True, accent=GOLD, frame_w=5)
    front.alpha_composite(lg, (W // 2 - lg.width // 2, 148))
    d = ImageDraw.Draw(front)
    rich(d, W // 2, 486, [("Your home, ", CREAM), ("aglow", GOLD), (" all season long.", CREAM)], SF(43, 700))
    caps_tracked(d, W // 2, 556, "HOLIDAY LIGHTING & EVENTS", F(20, "SemiBold"), SAGE, tracking=6)
    front.convert('RGB').save(f'{OUT}/SL_card_{surface}_FRONT.png', dpi=(DPI, DPI))

    back = grad_surface((15, 15, 17), (6, 6, 8), (46, 40, 26), GOLD, strand=False, accent=GOLD, frame_w=5)
    d = ImageDraw.Draw(back)
    f_b = F(19, "SemiBold")
    btxt = "THE SOUTHEAST'S #1 CHRISTMAS LIGHT INSTALLATION SERVICE"
    bw = sum(d.textlength(c, font=f_b) + 1.6 for c in btxt) - 1.6 + 88
    bx0 = W / 2 - bw / 2
    d.rounded_rectangle([bx0, 102, bx0 + bw, 148], 23, fill=(10, 10, 12, 215), outline=GOLD + (150,), width=2)
    dot(d, bx0 + 30, 125, 5)
    caps_tracked(d, W / 2 + 14, 124, btxt, f_b, GOLD, tracking=1.6)
    rich(d, W // 2, 226, [("Let's ", CREAM), ("Light Up", GOLD), (" Your Holidays", CREAM)], SF(56, 760))
    d.line([(W/2 - 70, 282), (W/2 + 70, 282)], fill=GOLD + (200,), width=4)
    contact_rows(d, [
        ("(864) 288-2459", F(37, "SemiBold"), CREAM, 338),
        ("sprucelights.com", F(31, "SemiBold"), GOLD, 392),
        ("@spruceholidaylighting", F(26, "Medium"), SAGE, 438),
    ], GOLD)
    d.text((W/2, 492), "Greenville  •  Upstate SC  •  Grand Strand  •  Western NC",
           font=F(21, "Regular"), fill=SAGE, anchor="mm")
    s = spruce_kit.bulb_strand(W, 9, 44, bulb=16, seed=7).transpose(Image.FLIP_TOP_BOTTOM)
    back.alpha_composite(s, (0, H - s.height + 8))
    back.convert('RGB').save(f'{OUT}/SL_card_{surface}_BACK.png', dpi=(DPI, DPI))

# ================================================================ SPRUCE PRO (teal / black)
SP_TXT  = (240, 246, 246)
SP_SUB  = (168, 196, 200)

def sp_card(surface='midnight'):
    if surface == 'midnight':
        base, dark, glowc, frame = (14, 26, 54), (6, 12, 28), (24, 46, 94), CYAN
    else:
        base, dark, glowc, frame = (13, 16, 18), (5, 7, 9), (16, 52, 58), CYAN
    logo = spruce_kit.load_logo(spruce_kit.SP, light_bg=False)
    lw = 470
    lg = logo.resize((lw, int(logo.height * lw / logo.width)), Image.LANCZOS)

    front = grad_surface(base, dark, glowc, frame, strand=False, accent=CYAN)
    front.alpha_composite(lg, (W // 2 - lg.width // 2, 156))
    d = ImageDraw.Draw(front)
    rich(d, W // 2, 486, [("Exterior cleaning, ", SP_TXT), ("done right.", CYAN)], F(36, "SemiBold"))
    grad_line(d, W // 2, 534, half=64, width=4)
    caps_tracked(d, W // 2, 566, "HOUSE WASHING • PRESSURE WASHING • WINDOWS • GUTTER GUARDS",
                 F(17, "SemiBold"), SP_SUB, tracking=3)
    front.convert('RGB').save(f'{OUT}/SP_card_{surface}_FRONT.png', dpi=(DPI, DPI))

    back = grad_surface(base, dark, glowc, frame, strand=False, accent=CYAN)
    d = ImageDraw.Draw(back)
    f_b = F(19, "SemiBold")
    btxt = "LICENSED & INSURED  •  SERVING THE UPSTATE SINCE 2006"
    bw = sum(d.textlength(c, font=f_b) + 1.6 for c in btxt) - 1.6 + 88
    bx0 = W / 2 - bw / 2
    d.rounded_rectangle([bx0, 102, bx0 + bw, 148], 23, fill=(10, 20, 42, 215) if surface == 'midnight' else (8, 10, 12, 215),
                        outline=CYAN + (150,), width=2)
    dot(d, bx0 + 30, 125, 5, CYAN)
    caps_tracked(d, W / 2 + 14, 124, btxt, f_b, CYAN, tracking=1.6)
    rich(d, W // 2, 226, [("A Cleaner Home, ", SP_TXT), ("All Year Long", CYAN)], F(54, "ExtraBold"))
    grad_line(d, W // 2, 284, half=70)
    contact_rows(d, [
        ("(864) 483-4300", F(37, "SemiBold"), SP_TXT, 338),
        ("sprucepro.com", F(31, "SemiBold"), CYAN, 392),
        ("@spruce_pro", F(26, "Medium"), SP_SUB, 438),
    ], CYAN)
    d.text((W/2, 492), "Greenville  •  Upstate SC  •  Surrounding Areas",
           font=F(21, "Regular"), fill=SP_SUB, anchor="mm")
    back.convert('RGB').save(f'{OUT}/SP_card_{surface}_BACK.png', dpi=(DPI, DPI))

# ================================================================ generate
sl_card('black')
sp_card('midnight')
sp_card('black')

def pdf(front, back, name):
    Image.open(f'{OUT}/{front}').save(f'{OUT}/{name}', save_all=True,
                                      append_images=[Image.open(f'{OUT}/{back}')], resolution=DPI)
pdf('SL_card_black_FRONT.png', 'SL_card_black_BACK.png', 'SL_business_card_black.pdf')
pdf('SP_card_midnight_FRONT.png', 'SP_card_midnight_BACK.png', 'SP_business_card_midnight.pdf')
pdf('SP_card_black_FRONT.png', 'SP_card_black_BACK.png', 'SP_business_card_black.pdf')

# ================================================================ family mockup
MW, MH = 1700, 1100
m = Image.new('RGB', (MW, MH), (10, 17, 12))
gr = Image.new('L', (1, MH))
for y in range(MH):
    gr.putpixel((0, y), int(255 * (y / MH) ** 1.3))
m.paste(Image.new('RGB', (MW, MH), (6, 12, 8)), (0, 0), gr.resize((MW, MH)))
m = glow(m.convert('RGBA'), MW // 2, 430, 760, (26, 46, 30), 30).convert('RGB')
m = sparkles(m.convert('RGBA'), 46, 9, MH - 40, 70, accent=GOLD).convert('RGB')

def place(base, path, cx, cy, ang, scale=1.0):
    c = Image.open(path).convert('RGBA')
    c = c.resize((int(c.width * scale), int(c.height * scale)), Image.LANCZOS)
    c = c.rotate(ang, expand=True, resample=Image.BICUBIC)
    sh = Image.new('RGBA', (c.width + 60, c.height + 60), (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([30, 34, c.width + 30, c.height + 30], 30, fill=(0, 0, 0, 150))
    sh = sh.filter(ImageFilter.GaussianBlur(22))
    base.paste(Image.new('RGB', sh.size, (0, 0, 0)), (cx - c.width//2 - 30, cy - c.height//2 - 30), sh)
    base.paste(c, (cx - c.width // 2, cy - c.height // 2), c)

place(m, f'{OUT}/SP_card_midnight_FRONT.png',  int(MW*0.30), int(MH*0.32),  4, 0.86)
place(m, f'{OUT}/SL_card_black_FRONT.png', int(MW*0.70), int(MH*0.30), -5, 0.86)
place(m, f'{OUT}/SL_card_pine_FRONT.png' if os.path.exists(f'{OUT}/SL_card_pine_FRONT.png') else f'{OUT}/SL_card_FRONT.png',
      int(MW*0.36), int(MH*0.72), -3, 0.86)
place(m, f'{OUT}/SP_card_black_FRONT.png', int(MW*0.72), int(MH*0.73),  6, 0.86)
d = ImageDraw.Draw(m)
d.text((MW // 2, MH - 44), "BUSINESS CARD FAMILY  ·  Spruce Lights (pine · black, bulb logo)  +  Spruce Pro (midnight · black, star logo)  ·  3.5×2 in + bleed · 300 DPI",
       font=F(22, "SemiBold"), fill=(150, 170, 152), anchor="mm")
m.save(f'{OUT}/SL_SP_card_family_mockup.jpg', quality=90)
print('variants + family mockup written')
