#!/usr/bin/env python3
"""Photorealistic business-card mockups v2 — exact homography warp (cv2)."""
import numpy as np, cv2
from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = '/home/user/spruce/business_card'
FONTS = '/home/user/spruce/assets/fonts'

def rounded_card(path, target_w, radius_frac=0.034):
    im = Image.open(path).convert('RGB')
    h = int(im.height * target_w / im.width)
    im = im.resize((target_w, h), Image.LANCZOS)
    m = Image.new('L', im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, im.width - 1, im.height - 1],
                                        int(im.width * radius_frac), fill=255)
    im.putalpha(m)
    return im

def place_card(scene, card, quad, light='tr', shadow_rgb=(15, 8, 3)):
    """quad = (TL, TR, BR, BL) in scene px. Exact perspective warp + shadows + light."""
    TL, TR, BR, BL = [np.array(p, np.float32) for p in quad]
    W0, H0 = card.size
    src = np.array([[0, 0], [W0, 0], [W0, H0], [0, H0]], np.float32)
    dst = np.array([TL, TR, BR, BL], np.float32)
    M = cv2.getPerspectiveTransform(src, dst)

    # ---- shadows ----
    for (dx, dy, blur, a) in [(20, 32, 26, 100), (6, 10, 8, 80)]:
        lay = Image.new('RGBA', scene.size, (0, 0, 0, 0))
        q = [tuple(p + np.array([dx, dy])) for p in (TL, TR, BR, BL)]
        ImageDraw.Draw(lay).polygon(q, fill=shadow_rgb + (a,))
        scene.alpha_composite(lay.filter(ImageFilter.GaussianBlur(blur)))

    # ---- directional light applied in card space (aligned to quad orientation) ----
    carr = np.asarray(card).astype(np.float32)
    hh, ww = H0, W0
    gx = np.linspace(0, 1, ww)[None, :].repeat(hh, 0)
    gy = np.linspace(0, 1, hh)[:, None].repeat(ww, 1)
    if light == 'tr':   gain = 0.88 + 0.26 * (0.55 * gx + 0.45 * (1 - gy))
    elif light == 'l':  gain = 0.88 + 0.26 * (0.72 * (1 - gx) + 0.28 * (1 - gy))
    else:               gain = np.ones((hh, ww), np.float32)
    carr[..., :3] = np.clip(carr[..., :3] * gain[..., None], 0, 255)

    # ---- exact warp with alpha ----
    warped = cv2.warpPerspective(carr.astype(np.uint8), M, (scene.width, scene.height),
                                 flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT,
                                 borderValue=(0, 0, 0, 0))
    layer = Image.fromarray(warped, 'RGBA')
    # subtle top-edge sheen along the light side (specular hint)
    scene.alpha_composite(layer)
    return scene

def caption(scene, text, rgb=(205, 195, 170)):
    f = ImageFont.truetype(f'{FONTS}/Poppins-SemiBold.ttf', 26)
    w = ImageDraw.Draw(scene).textlength(text, font=f)
    ov = Image.new('RGBA', scene.size, (0, 0, 0, 0))
    ImageDraw.Draw(ov).rectangle([0, scene.height - 76, scene.width, scene.height], fill=(8, 10, 8, 165))
    scene.alpha_composite(ov)
    ImageDraw.Draw(scene).text(((scene.width - w) / 2, scene.height - 50), text, font=f, fill=rgb, anchor="lm")
    return scene

# ================================================ SPRUCE LIGHTS scene
plate = Image.open(f'{OUT}/plate_sl.png').convert('RGBA')
back = rounded_card(f'{OUT}/SL_card_black_FRONT.png', 520)
front = rounded_card(f'{OUT}/SL_card_FRONT.png', 545)
place_card(plate, back, [(432, 438), (898, 418), (923, 782), (457, 802)],
           light='tr', shadow_rgb=(18, 9, 3))
place_card(plate, front, [(560, 582), (1042, 602), (1016, 946), (534, 926)],
           light='tr', shadow_rgb=(18, 9, 3))
caption(plate, "SPRUCE LIGHTS  ·  business card — pine & black editions  ·  holiday lighting & events")
plate.convert('RGB').save(f'{OUT}/SL_card_scene.jpg', quality=92)

# ================================================ SPRUCE SERVICES scene
plate = Image.open(f'{OUT}/plate_sp.png').convert('RGBA')
back = rounded_card(f'{OUT}/SP_card_midnight_FRONT.png', 520)
front = rounded_card(f'{OUT}/SP_card_black_FRONT.png', 545)
place_card(plate, back, [(688, 424), (1158, 408), (1184, 768), (714, 784)],
           light='l', shadow_rgb=(0, 8, 14))
place_card(plate, front, [(818, 566), (1306, 586), (1280, 936), (792, 916)],
           light='l', shadow_rgb=(0, 8, 14))
caption(plate, "SPRUCE SERVICES & SOLUTIONS  ·  business card — midnight & black editions  ·  exterior cleaning",
        rgb=(170, 200, 205))
plate.convert('RGB').save(f'{OUT}/SP_card_scene.jpg', quality=92)
print('scenes v2 written')
