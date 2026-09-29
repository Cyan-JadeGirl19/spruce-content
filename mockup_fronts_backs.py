#!/usr/bin/env python3
"""Front & back flat-lay sheets — one per company, both editions, all four sides."""
from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = '/home/user/spruce/business_card'
FONTS = '/home/user/spruce/assets/fonts'

def F(s, w="SemiBold"):
    return ImageFont.truetype(f'{FONTS}/Poppins-{w}.ttf', s)

def sheet(plate_path, out, header, sub, cards, label_rgb, accent):
    """cards = [(front_path, back_path, edition_name, angle_f, angle_b), ...]"""
    scene = Image.open(plate_path).convert('RGBA')
    W, H = scene.size
    d0 = ImageDraw.Draw(scene)
    # header
    d0.text((64, 46), header, font=F(44, "ExtraBold"), fill=accent)
    tw = d0.textlength(sub, font=F(21))
    d0.text((W - 64 - tw, 62), sub, font=F(21), fill=(150, 152, 148))
    d0.line([(64, 118), (W - 64, 118)], fill=accent + (110,), width=2)

    card_w = 500
    col_cx = [64 + (W - 128) * 0.25, 64 + (W - 128) * 0.75]
    row_cy = [345, 762]

    def place(img_path, cx, cy, ang, label):
        im = Image.open(img_path).convert('RGB')
        im = im.resize((card_w, int(im.height * card_w / im.width)), Image.LANCZOS)
        m = Image.new('L', im.size, 0)
        ImageDraw.Draw(m).rounded_rectangle([0, 0, im.width - 1, im.height - 1],
                                            int(im.width * 0.034), fill=255)
        im.putalpha(m)
        c = im.rotate(ang, expand=True, resample=Image.BICUBIC)
        # soft flat-lay shadow
        a = c.getchannel('A').point(lambda v: v * 130 // 255)
        sh = Image.new('RGBA', scene.size, (0, 0, 0, 0))
        blk = Image.new('RGBA', c.size, (10, 8, 5, 255))
        blk.putalpha(a)
        sh.paste(blk, (int(cx - c.width // 2 + 10), int(cy - c.height // 2 + 18)), blk)
        scene.alpha_composite(sh.filter(ImageFilter.GaussianBlur(13)))
        scene.alpha_composite(c, (int(cx - c.width // 2), int(cy - c.height // 2)))
        dd = ImageDraw.Draw(scene)
        lw = dd.textlength(label, font=F(22))
        dd.rounded_rectangle([cx - lw / 2 - 16, cy + c.height // 2 + 10,
                              cx + lw / 2 + 16, cy + c.height // 2 + 44], 17,
                             fill=(10, 10, 10, 130), outline=accent + (90,), width=1)
        dd.text((cx, cy + c.height // 2 + 26), label, font=F(22), fill=label_rgb, anchor="lm")

    (front, back, name, af, ab) = cards[0]
    place(front, col_cx[0], row_cy[0], af, f"{name} — FRONT")
    place(back,  col_cx[1], row_cy[0], ab, f"{name} — BACK")
    (front, back, name, af, ab) = cards[1]
    place(front, col_cx[0], row_cy[1], af, f"{name} — FRONT")
    place(back,  col_cx[1], row_cy[1], ab, f"{name} — BACK")
    scene.convert('RGB').save(out, quality=92)

# ---------------- Spruce Lights (pine + black)
sheet(f'{OUT}/plate_sl_top.png', f'{OUT}/SL_card_front_back.jpg',
      "SPRUCE LIGHTS", "business card · front & back · 3.5×2 in + bleed · 300 DPI",
      [(f'{OUT}/SL_card_FRONT.png', f'{OUT}/SL_card_BACK.png', 'PINE', -1.6, 1.4),
       (f'{OUT}/SL_card_black_FRONT.png', f'{OUT}/SL_card_black_BACK.png', 'BLACK', 1.8, -1.2)],
      label_rgb=(226, 214, 186), accent=(240, 176, 45))

# ---------------- Spruce Services (midnight + black)
sheet(f'{OUT}/plate_sp_top.png', f'{OUT}/SP_card_front_back.jpg',
      "SPRUCE SERVICES & SOLUTIONS", "business card · front & back · 3.5×2 in + bleed · 300 DPI",
      [(f'{OUT}/SP_card_midnight_FRONT.png', f'{OUT}/SP_card_midnight_BACK.png', 'MIDNIGHT', -1.6, 1.4),
       (f'{OUT}/SP_card_black_FRONT.png', f'{OUT}/SP_card_black_BACK.png', 'BLACK', 1.8, -1.2)],
      label_rgb=(196, 216, 220), accent=(28, 200, 208))
print('front/back sheets written')
