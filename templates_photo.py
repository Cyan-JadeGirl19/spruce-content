"""PHOTO-FIRST templates — client feedback: no blocks, no heavy writing.
Full-bleed photography, tiny logo + brand chip, ONE short caption line low on
the image (soft gradient for legibility — not a panel), slim contact footer."""
from spruce_kit import *

SQ = (1080, 1080)
ST = (1080, 1920)

def photo_post(brand, size, bg_path, caption, kicker=None, sub=None,
               focus=0.5, brighten=1.0, badge=None):
    W, H = size
    serif = brand["key"] == "spruce_lights"
    gold = (240, 176, 45) if serif else (28, 200, 208)
    cream = (246, 240, 226)
    img = bg_photo(bg_path, W, H, focus=focus, blur=1.2, brighten=brighten, sat=1.06)
    img = cinema(img, strength=0.4)
    # subtle bottom gradient only under the text zone (keeps photo open)
    band = int(H * 0.34)
    grad = Image.new('L', (1, band))
    for i in range(band):
        grad.putpixel((0, i), int(210 * (i / band) ** 1.6))
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    dark = Image.new('RGBA', (W, H), (4, 12, 6, 255) if serif else (0, 12, 16, 255))
    ov.paste(dark.crop((0, H - band, W, H)).convert('RGBA'), (0, H - band), grad.resize((W, band)))
    img.alpha_composite(ov)
    img = place_logo_top(img, brand, light_bg=False)

    d = ImageDraw.Draw(img)
    y = H - (330 if H > 1200 else 286) - (58 if sub else 0)
    if kicker:
        f = F(23, "SemiBold")
        d.text((W / 2, y), kicker.upper(), font=f, fill=gold, anchor="mm",
               stroke_width=1, stroke_fill=(0, 15, 8, 160))
        y += 44
    cs = 46 if H > 1200 else 40
    while cs > 30:
        f = ImageFont.truetype(f"{FONTS}/PlayfairDisplay.ttf", cs) if serif else F(cs, "Bold")
        if serif:
            try: f.set_variation_by_axes([760])
            except Exception: pass
        lines = wrap_text(caption, f, int(W * 0.86), d)
        if len(lines) <= 2 and max(d.textlength(l, font=f) for l in lines) <= W * 0.86:
            break
        cs -= 2
    for ln in lines:
        d.text((W / 2, y), ln, font=f, fill=cream, anchor="mm",
               stroke_width=2, stroke_fill=(0, 12, 6, 150))
        y += cs * 1.18
    if sub:
        fs = F(24, "Medium")
        d.text((W / 2, y + 8), sub, font=fs,
               fill=(196, 190, 176) if serif else (170, 196, 200), anchor="mm",
               stroke_width=1, stroke_fill=(0, 12, 6, 130))
    img = footer_bar(img, brand)
    from templates import _accent_arc
    return _accent_arc(img, brand)

from templates import before_after


def before_after(brand, size, path_a, path_b, kicker, title, la="BEFORE", lb="AFTER", focus=0.55):
    """photo-first BA: clean split, gold divider, small labels, one caption."""
    from templates import before_after as _badummy
    W, H = size
    serif = brand["key"] == "spruce_lights"
    gold = (240, 176, 45) if serif else (28, 200, 208)
    cream = (246, 240, 226)
    A = bg_photo(path_a, W // 2, H, focus=focus, blur=1.2, brighten=0.98, sat=1.03)
    B = bg_photo(path_b, W // 2, H, focus=focus, blur=1.2, brighten=1.04, sat=1.05)
    img = Image.new('RGBA', (W, H), (0, 0, 0, 255))
    img.paste(A.convert('RGB'), (0, 0))
    img.paste(B.convert('RGB'), (W // 2, 0))
    d = ImageDraw.Draw(img)
    d.line([(W // 2, 0), (W // 2, H)], fill=gold, width=6)
    f = F(26, "ExtraBold")
    for txt, cx in ((la, W // 4), (lb, W * 3 // 4)):
        tw = d.textlength(txt, font=f)
        ov = Image.new('RGBA', img.size, (0, 0, 0, 0))
        ImageDraw.Draw(ov).rounded_rectangle([cx - tw/2 - 22, 132, cx + tw/2 + 22, 186], 27,
            fill=(10, 18, 12, 200), outline=gold + (180,), width=2)
        img.alpha_composite(ov)
        d = ImageDraw.Draw(img)
        d.text((cx, 158), txt, font=f, fill=cream, anchor="mm")
    band = int(H * 0.26)
    grad = Image.new('L', (1, band))
    for i in range(band):
        grad.putpixel((0, i), int(200 * (i / band) ** 1.6))
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    dark = Image.new('RGBA', (W, H), (4, 12, 6, 255) if serif else (0, 12, 16, 255))
    ov.paste(dark.crop((0, H - band, W, H)).convert('RGBA'), (0, H - band), grad.resize((W, band)))
    img.alpha_composite(ov)
    img = place_logo_top(img, brand, light_bg=False)
    d = ImageDraw.Draw(img)
    y = H - (318 if H > 1200 else 274)
    cs = 48 if H > 1200 else 42
    f = ImageFont.truetype(f"{FONTS}/PlayfairDisplay.ttf", cs) if serif else F(cs, "Bold")
    if serif:
        try: f.set_variation_by_axes([760])
        except Exception: pass
    for ln in wrap_text(title, f, int(W * 0.8), d)[:2]:
        d.text((W / 2, y), ln, font=f, fill=cream, anchor="mm",
               stroke_width=2, stroke_fill=(0, 12, 6, 150))
        y += cs * 1.18
    img = footer_bar(img, brand)
    from templates import _accent_arc
    return _accent_arc(img, brand)
