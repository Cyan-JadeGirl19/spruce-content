#!/usr/bin/env python3
"""Spruce Lights full card family sheet — 4 editions, fronts + backs, BRIGHT flat-lay."""
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageEnhance

OUT = '/home/user/spruce/business_card'
FONTS = '/home/user/spruce/assets/fonts'

def F(s, w="SemiBold"):
    return ImageFont.truetype(f'{FONTS}/Poppins-{w}.ttf', s)

def build():
    scene = Image.open(f'{OUT}/plate_sl_top.png').convert('RGBA')
    scene = ImageEnhance.Brightness(scene).enhance(1.48)      # lift the walnut plate
    scene = ImageEnhance.Contrast(scene).enhance(1.02)
    W, H = scene.size
    accent = (240, 176, 45)
    d0 = ImageDraw.Draw(scene)
    d0.text((64, 42), "SPRUCE LIGHTS", font=F(42, "ExtraBold"), fill=accent)
    sub = "business card family · front & back · 3.5×2 in + bleed · 300 DPI"
    tw = d0.textlength(sub, font=F(20))
    d0.text((W - 64 - tw, 56), sub, font=F(20), fill=(168, 164, 152))
    d0.line([(64, 110), (W - 64, 110)], fill=accent + (120,), width=2)

    editions = [
        (f'{OUT}/SL_card_FRONT.png',      f'{OUT}/SL_card_BACK.png',      'PINE'),
        (f'{OUT}/SL_card_black_FRONT.png', f'{OUT}/SL_card_black_BACK.png', 'BLACK'),
        (f'{OUT}/SL_card_qr_FRONT.png',   f'{OUT}/SL_card_qr_BACK.png',   'QR'),
        (f'{OUT}/SL_card_will_FRONT.png', f'{OUT}/SL_card_will_BACK.png', 'WILL BRUCE'),
    ]
    card_w = 336
    margin = 80
    span = W - 2 * margin
    cxs = [margin + span * (i + 0.5) / 4 for i in range(4)]
    row_cy = [318, 690]

    def place(img_path, cx, cy, label):
        im = Image.open(img_path).convert('RGB')
        im = im.resize((card_w, int(im.height * card_w / im.width)), Image.LANCZOS)
        im = ImageEnhance.Brightness(im).enhance(1.16)        # cards read clearly
        m = Image.new('L', im.size, 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, im.width - 1, im.height - 1],
                                            int(im.width * 0.034), fill=255)
        im.putalpha(m)
        c = im.rotate(-1.2 if cy == row_cy[0] else 1.2, expand=True, resample=Image.BICUBIC)
        a = c.getchannel('A').point(lambda v: v * 80 // 255)
        blk = Image.new('RGBA', c.size, (12, 9, 5, 255)); blk.putalpha(a)
        sh = Image.new('RGBA', scene.size, (0, 0, 0, 0))
        sh.paste(blk, (int(cx - c.width // 2 + 8), int(cy - c.height // 2 + 14)), blk)
        scene.alpha_composite(sh.filter(ImageFilter.GaussianBlur(11)))
        scene.alpha_composite(c, (int(cx - c.width // 2), int(cy - c.height // 2)))
        dd = ImageDraw.Draw(scene)
        f_lab = F(19)
        lw = dd.textlength(label, font=f_lab)
        bb = dd.textbbox((0, 0), label, font=f_lab)
        ly = int(cy + c.height // 2 + 30)
        dd.rounded_rectangle([cx - lw / 2 - 14, ly - 15, cx + lw / 2 + 14, ly + 15], 15,
                             fill=(12, 12, 12, 140), outline=accent + (110,), width=1)
        dd.text((cx - lw / 2 - bb[0], ly - (bb[1] + bb[3]) / 2), label, font=f_lab, fill=(232, 220, 192))

    for i, (fr, bk, name) in enumerate(editions):
        place(fr, cxs[i], row_cy[0], f"{name} — FRONT")
        place(bk, cxs[i], row_cy[1], f"{name} — BACK")

    scene.convert('RGB').save(f'{OUT}/SL_card_front_back.jpg', quality=92)
    print('bright family sheet written')

build()
