#!/usr/bin/env python3
"""Two more Spruce Lights card variants:
  1. QR variant  — back features a scan-to-website code (sprucelights.com)
  2. Personal variant for Will Bruce (Owner)
Same Website-Edition pine system, thick gold frame, bulb strands."""
import random
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import spruce_kit
import qrcode

ROOT = '/home/user/spruce'
OUT = f'{ROOT}/business_card'
W, H, DPI = 1125, 675, 300
FONTS = f'{ROOT}/assets/fonts'

GOLD  = (240, 176, 45)
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

def glow(img, cx, cy, r, color, peak=32):
    g = Image.new('L', (256, 256), 0)
    gd = ImageDraw.Draw(g)
    for i in range(128, 0, -2):
        gd.ellipse([128 - i, 128 - i, 128 + i, 128 + i], fill=int(peak * (1 - i / 128)))
    g = g.resize((r * 2, r * 2))
    ov = Image.new('RGBA', img.size, (0, 0, 0, 0))
    ov.paste(Image.new('RGBA', (r * 2, r * 2), color + (255,)), (cx - r, cy - r), g)
    img.alpha_composite(ov)
    return img

def sparkles(img, n, seed, ymax, cmax=80):
    rnd = random.Random(seed)
    ov = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for _ in range(n):
        x, y = rnd.uniform(30, W - 30), rnd.uniform(30, ymax)
        r = rnd.uniform(2.0, 5.0)
        c = GOLD if rnd.random() < 0.6 else CREAM
        a = rnd.randint(28, cmax)
        d.line([(x - r * 2.2, y), (x + r * 2.2, y)], fill=c + (a,), width=1)
        d.line([(x, y - r * 2.2), (x, y + r * 2.2)], fill=c + (a,), width=1)
        d.ellipse([x - r * .5, y - r * .5, x + r * .5, y + r * .5], fill=c + (min(255, a + 60),))
    img.alpha_composite(ov.filter(ImageFilter.GaussianBlur(0.6)))
    return img

def surface(strand=True, strand_bottom=False):
    img = Image.new('RGBA', (W, H), (13, 27, 16, 255))
    gr = Image.new('L', (1, H))
    for y in range(H):
        gr.putpixel((0, y), int(255 * (y / H) ** 1.2))
    img.paste(Image.new('RGB', (W, H), (7, 15, 9)), (0, 0), gr.resize((W, H)))
    img = glow(img, W // 2, int(H * 0.36), 420, (22, 42, 26))
    img = sparkles(img, 24, 11, H - 60)
    if strand:
        s = spruce_kit.bulb_strand(W, 9, 44, bulb=16, seed=7)
        if strand_bottom:
            s = s.transpose(Image.FLIP_TOP_BOTTOM)
            img.alpha_composite(s, (0, H - s.height + 8))
        else:
            img.alpha_composite(s, (0, -8))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([72, 72, W - 72, H - 72], 26, outline=GOLD + (120,), width=5)
    return img

def dot(d, x, y, r=4.5):
    d.ellipse([x - r, y - r, x + r, y + r], fill=GOLD)

def logo_img(width):
    lg = spruce_kit.load_logo(spruce_kit.SL, light_bg=False)
    return lg.resize((width, int(lg.height * width / lg.width)), Image.LANCZOS)

def qr_img(url, box):
    q = qrcode.QRCode(border=1, box_size=12, error_correction=qrcode.constants.ERROR_CORRECT_M)
    q.add_data(url); q.make(fit=True)
    m = q.make_image(fill_color=(13, 27, 16), back_color="white").convert('RGB')
    return m.resize((box, box), Image.NEAREST)

# ============================================ 1. QR VARIANT (pine front + QR back)
front = surface(strand=True)
front.alpha_composite(logo_img(440), (W // 2 - 220, 152))
d = ImageDraw.Draw(front)
rich(d, W // 2, 486, [("Your home, ", CREAM), ("aglow", GOLD), (" all season long.", CREAM)], SF(43, 700))
caps_tracked(d, W // 2, 556, "HOLIDAY LIGHTING & EVENTS", F(20, "SemiBold"), SAGE, tracking=6)
front.convert('RGB').save(f'{OUT}/SL_card_qr_FRONT.png', dpi=(DPI, DPI))

back = surface(strand=False)
d = ImageDraw.Draw(back)
f_b = F(19, "SemiBold")
btxt = "THE SOUTHEAST'S #1 CHRISTMAS LIGHT INSTALLATION SERVICE"
bw = sum(d.textlength(c, font=f_b) + 1.6 for c in btxt) - 1.6 + 88
bx0 = W / 2 - bw / 2
d.rounded_rectangle([bx0, 100, bx0 + bw, 146], 23, fill=DK + (215,), outline=GOLD + (150,), width=2)
dot(d, bx0 + 30, 123, 5)
caps_tracked(d, W / 2 + 14, 122, btxt, f_b, GOLD, tracking=1.6)
rich(d, W // 2, 208, [("Let's ", CREAM), ("Light Up", GOLD), (" Your Holidays", CREAM)], SF(50, 760))
# left column — all contact details
cxL = 350
rows = [
    ("(864) 288-2459", F(30, "SemiBold"), CREAM, 322),
    ("sprucelights.com", F(26, "SemiBold"), GOLD, 370),
    ("@spruceholidaylighting", F(22, "Medium"), SAGE, 414),
    ("Designs • Install • Takedown • Storage", F(18, "Regular"), SAGE, 458),
]
for txt, f, c, yy in rows:
    tw = d.textlength(txt, font=f)
    dot(d, cxL - tw / 2 - 20, yy - 2, 3.8)
    d.text((cxL, yy), txt, font=f, fill=c, anchor="mm")
caps_tracked(d, cxL, 508, "GREENVILLE • UPSTATE SC • GRAND STRAND", F(14, "SemiBold"), SAGE, tracking=1)
# divider
d.line([(560, 292), (560, 518)], fill=GOLD + (70,), width=2)
# right column — QR
qs = 220
px0, py0 = 800 - qs // 2 - 14, 282
ov = Image.new('RGBA', back.size, (0, 0, 0, 0))
ImageDraw.Draw(ov).rounded_rectangle([px0, py0, px0 + qs + 28, py0 + qs + 28], 22, fill=(250, 247, 240, 255))
back.alpha_composite(ov)
back.paste(qr_img("https://sprucelights.com", qs), (px0 + 14, py0 + 14))
d = ImageDraw.Draw(back)
caps_tracked(d, 800, py0 + qs + 60, "SCAN FOR A FREE QUOTE", F(16, "Bold"), GOLD, tracking=3)
back.convert('RGB').save(f'{OUT}/SL_card_qr_BACK.png', dpi=(DPI, DPI))

# ============================================ 2. PERSONAL VARIANT — WILL BRUCE
front = surface(strand=True)
front.alpha_composite(logo_img(330), (W // 2 - 165, 118))
d = ImageDraw.Draw(front)
d.text((W / 2, 388), "Will Bruce", font=SF(78, 780), fill=CREAM, anchor="mm")
caps_tracked(d, W / 2, 452, "OWNER", F(26, "Bold"), GOLD, tracking=10)
d.line([(W/2 - 60, 486), (W/2 + 60, 486)], fill=GOLD + (190,), width=3)
d.text((W / 2, 530), "(864) 288-2459", font=F(27, "SemiBold"), fill=CREAM, anchor="mm")
caps_tracked(d, W / 2, 576, "SPRUCE LIGHTS & EVENTS", F(17, "SemiBold"), SAGE, tracking=5)
front.convert('RGB').save(f'{OUT}/SL_card_will_FRONT.png', dpi=(DPI, DPI))

back = surface(strand=False)
d = ImageDraw.Draw(back)
f_b = F(19, "SemiBold")
btxt = "DIRECT LINE"
bw = sum(d.textlength(c, font=f_b) + 1.8 for c in btxt) - 1.8 + 88
bx0 = W / 2 - bw / 2
d.rounded_rectangle([bx0, 102, bx0 + bw, 148], 23, fill=DK + (215,), outline=GOLD + (150,), width=2)
dot(d, bx0 + 30, 125, 5)
caps_tracked(d, W / 2 + 14, 124, btxt, f_b, GOLD, tracking=1.8)
d.text((W / 2, 224), "Will Bruce", font=SF(58, 760), fill=CREAM, anchor="mm")
caps_tracked(d, W / 2, 280, "OWNER, SPRUCE LIGHTING & EVENTS", F(19, "Bold"), GOLD, tracking=4)
d.line([(W/2 - 64, 312), (W/2 + 64, 312)], fill=GOLD + (190,), width=3)
rows = [
    ("(864) 288-2459", F(33, "SemiBold"), CREAM, 364),
    ("sprucelights.com", F(28, "SemiBold"), GOLD, 416),
    ("@spruceholidaylighting", F(24, "Medium"), SAGE, 460),
]
for txt, f, c, yy in rows:
    tw = d.textlength(txt, font=f)
    dot(d, W/2 - tw/2 - 24, yy - 2, 4.2)
    d.text((W/2, yy), txt, font=f, fill=c, anchor="mm")
d.text((W / 2, 506), "Greenville  •  Upstate SC  •  Grand Strand  •  Western NC",
       font=F(19, "Regular"), fill=SAGE, anchor="mm")
s = spruce_kit.bulb_strand(W, 9, 44, bulb=16, seed=7).transpose(Image.FLIP_TOP_BOTTOM)
back.alpha_composite(s, (0, H - s.height + 8))
back.convert('RGB').save(f'{OUT}/SL_card_will_BACK.png', dpi=(DPI, DPI))

# ============================================ PDFs
Image.open(f'{OUT}/SL_card_qr_FRONT.png').save(f'{OUT}/SL_business_card_qr.pdf', save_all=True,
    append_images=[Image.open(f'{OUT}/SL_card_qr_BACK.png')], resolution=DPI)
Image.open(f'{OUT}/SL_card_will_FRONT.png').save(f'{OUT}/SL_business_card_will.pdf', save_all=True,
    append_images=[Image.open(f'{OUT}/SL_card_will_BACK.png')], resolution=DPI)
print('QR + Will Bruce variants written')
