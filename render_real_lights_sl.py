"""5 real-lights video posts for Spruce Lights — residential / commercial / municipal.
Actual photos from sprucelights.com, Website Edition styling, music-box soundtrack,
brand chip burned in. Rendered in 1:1 (feed) and 9:16 (reel/story) for any platform."""
import sys, math
sys.path.insert(0, '/home/user/spruce')
import spruce_kit as _K
_K.TEAL = (13, 27, 16, 255); _K.TEAL_D = (8, 18, 11, 255); _K.TEAL_L = (24, 44, 28, 255)
_K.SCRIM_COLOR = (2, 14, 8); _K.FOOT_DARK = (3, 20, 12); _K.CINE_SHADOW = (0.0, 0.05, 0.028)
from vidkit import *
from spruce_kit import FONTS
import vidkit as _V
_GOLD = (240, 176, 45, 255); _CREAM = (246, 240, 226, 255); _SAGE = (164, 178, 156, 255)
import audio_kit as _AK
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import os

OUT = f'{ROOT}/videos/spruce_lights'
os.makedirs(OUT, exist_ok=True)
BG = f'{ROOT}/assets/photos/sl_real'
ST, SQ = (1080, 1920), (1080, 1080)
LOGO = load_logo(SL, light_bg=False)
LOGO.thumbnail((760, 820), Image.LANCZOS)

_SFONTS = {}
def SF(px, wght=800):
    k = (px, wght)
    if k not in _SFONTS:
        f = ImageFont.truetype(f'{FONTS}/PlayfairDisplay.ttf', px)
        try: f.set_variation_by_axes([wght])
        except Exception: pass
        _SFONTS[k] = f
    return _SFONTS[k]

def serif_layer(size, text, px, wght=800, color=_CREAM, maxw_frac=0.86, lh=1.16, y_center=0):
    W, Hh = size
    layer = Image.new('RGBA', size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    f = SF(px, wght)
    lines = wrap_text(text, f, int(W * maxw_frac), d)
    th = len(lines) * px * lh
    y = y_center - th / 2 + px * 0.1
    for ln in lines:
        w = d.textlength(ln, font=f)
        sh = Image.new('RGBA', size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).text(((W - w) / 2 + 3, y + 4), ln, font=f, fill=(0, 10, 6, 200))
        layer.alpha_composite(sh.filter(ImageFilter.GaussianBlur(7)))
        d.text(((W - w) / 2, y), ln, font=f, fill=color)
        y += px * lh
    return layer, th

def badge_layer(size, text, y_center, accent=_GOLD[:3]):
    """site-style pill badge: dot + gold caps"""
    W, H = size
    lay = Image.new('RGBA', size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    f = F(26, 'SemiBold')
    tw = d.textlength(text.upper(), font=f)
    x0, x1 = W/2 - tw/2 - 54, W/2 + tw/2 + 32
    d.rounded_rectangle([x0, y_center - 27, x1, y_center + 27], 27,
                        fill=(13, 25, 15, 215), outline=accent + (170,), width=2)
    d.ellipse([x0 + 25, y_center - 6, x0 + 37, y_center + 6], fill=accent)
    d.text((x0 + 55, y_center - 1), text.upper(), font=f, fill=accent, anchor='lm')
    return lay

def sub_layer(size, text, px, y_center):
    W, H = size
    layer = Image.new('RGBA', size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    f = F(px, 'Medium')
    lines = wrap_text(text, f, int(W * 0.80), d)
    y = y_center - len(lines) * px * 1.2 / 2
    for ln in lines:
        w = d.textlength(ln, font=f)
        sh = Image.new('RGBA', size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).text(((W - w) / 2 + 2, y + 3), ln, font=f, fill=(0, 10, 6, 180))
        layer.alpha_composite(sh.filter(ImageFilter.GaussianBlur(5)))
        d.text(((W - w) / 2, y), ln, font=f, fill=(215, 224, 214, 255))
        y += px * 1.2
    return layer

_SCRIMS = {}
def _top_scrim(size):
    if size not in _SCRIMS:
        W, H = size
        g = Image.new('L', (1, H), 0)
        for y in range(H):
            f = y / H
            g.putpixel((0, y), int(125 * max(0.0, 1 - f / 0.46)) if f < 0.46 else 0)
        ov = Image.new('RGBA', size, (0, 0, 0, 0))
        ov.paste(Image.new('RGBA', size, (2, 10, 6, 255)), (0, 0), g.resize((W, H)))
        _SCRIMS[size] = ov
    return _SCRIMS[size]

def kb(seq_photos, size, t, scene_len):
    """ken-burns frame for current scene, gentle white flash on boundaries"""
    idx = min(int(t / scene_len), len(seq_photos) - 1)
    local = t - idx * scene_len
    p = seq_photos[idx]
    zoom_in = idx % 2 == 0
    if zoom_in:
        base = bg_photo(p, size[0], int(size[1] * 1.16), brighten=1.04, sat=1.06)
        z = 1.0 + 0.10 * easeio(min(local / scene_len, 1))
        pan = 0.02 * math.sin(idx * 2.1)
    else:
        base = bg_photo(p, size[0], int(size[1] * 1.16), brighten=1.04, sat=1.06)
        z = 1.10 - 0.10 * easeio(min(local / scene_len, 1))
        pan = -0.02 * math.sin(idx * 1.7)
    W, H = size
    bw, bh = base.size
    cw, ch = int(bw / z), int(bh / z)
    cx = int(bw / 2 + pan * bw / 2 - cw / 2)
    cy = max(0, min(bh - ch, int((bh - ch) * 0.42)))
    img = base.crop((cx, cy, cx + cw, cy + ch)).resize(size, Image.LANCZOS).convert('RGBA')
    img = cinema(img, strength=0.55)
    flash_t = 0.18
    if idx > 0 and local < flash_t:
        img.alpha_composite(Image.new('RGBA', size, (255, 252, 240, int(120 * (1 - local / flash_t)))))
    return img

def cta_card(size, title, dur=3.4):
    """closing pine card: logo / serif title / gold CTA / contact — no overlaps"""
    W, H = size
    feed = H <= 1200
    logo_h = 235
    lg0 = LOGO.resize((int(LOGO.width * logo_h / LOGO.height), logo_h), Image.LANCZOS)
    ly0    = int(H * (0.145 if feed else 0.165))
    y_tit  = int(H * (0.435 if feed else 0.370))
    y_cta  = int(H * (0.615 if feed else 0.545))
    y_pho  = int(H * (0.745 if feed else 0.660))
    for i in range(int(dur * FPS)):
        t = i / FPS
        e = ease(seg(t, 0.15, 0.8))
        img = vgrad(size, TEAL, TEAL_D)
        img.alpha_composite(radial_glow(size, (W/2, H*0.30), W*0.7, _GOLD[:3], peak=34))
        sp = sparkle_field_layer(size, 10, n=12, ymax_frac=0.9)
        lg = lg0.copy()
        la = lg.getchannel('A').point(lambda v: int(v * e))
        lg.putalpha(la)
        img.alpha_composite(lg, ((W - lg.width)//2, int(ly0 + (1 - e) * 46)))
        tt, _ = serif_layer(size, title, 54 if feed else 60, 800, _CREAM,
                            maxw_frac=0.86, y_center=y_tit)
        img.alpha_composite(tt.point(lambda v: int(v * ease(seg(t, 0.5, 1.1)))))
        if t > 0.9:
            d = ImageDraw.Draw(img)
            pe = ease(seg(t, 0.9, 1.4))
            f = F(42, 'Bold')
            pw = d.textlength("Get My Free Quote", font=f) + 120
            cy = int(y_cta + (1 - pe) * 40)
            pill(d, [W/2 - pw/2, cy - 52, W/2 + pw/2, cy + 52], GOLD)
            d.text((W/2, cy - 2), "Get My Free Quote", font=f, fill=(13, 25, 15), anchor='mm')
            ph, _ = text_layer(size, "(864) 288-2459  •  sprucelights.com", 'SemiBold', 33,
                               color=(226, 226, 220, 255), y_center=y_pho)
            img.alpha_composite(ph.point(lambda v: int(v * ease(seg(t, 1.2, 1.7)))))
        img.alpha_composite(brand_footer_layer(size, SL))
        draw_sparkle_field(img, sp, t + 3.0)
        yield img

def build(name, photos, kicker, title, sub, seed, dur, size, tag):
    W, H = size
    scene_len = (dur - 3.4) / len(photos)
    foot = brand_footer_layer(size, SL)
    text_in = 0.45
    bdg = badge_layer(size, kicker, int(H * (0.155 if H > 1200 else 0.145)))
    ttl, _ = serif_layer(size, title, 64 if H > 1200 else 58, 800, _CREAM,
                         maxw_frac=0.86, y_center=int(H * (0.245 if H > 1200 else 0.235)))
    sb = sub_layer(size, sub, 28 if H > 1200 else 26, int(H * (0.325 if H > 1200 else 0.315)))
    def frames():
        n = int(dur * FPS)
        for i in range(n):
            t = i / FPS
            if t < dur - 3.4:
                img = kb(photos, size, t, scene_len)
                sc = max(0.0, min(1.0, (t - text_in) / 0.5))
                if sc > 0:
                    b = bdg.point(lambda v: int(v * ease(sc)))
                    img.alpha_composite(b)
                    tl = ttl.point(lambda v: int(v * ease(seg(t, text_in, text_in + 0.55))))
                    img = slide_fade(img, tl, t, text_in, text_in + 0.6, dy=44)
                    sl = sb.point(lambda v: int(v * ease(seg(t, text_in + 0.25, text_in + 0.75))))
                    img = slide_fade(img, sl, t, text_in + 0.25, text_in + 0.8, dy=36)
                img.alpha_composite(foot)
            else:
                ct = t - (dur - 3.4)
                for cimg in _card_once(size, title, ct):
                    img = cimg
                    break
            yield img
    # reuse a generator for the closing card
    def frames2():
        n = int(dur * FPS)
        card_start = dur - 3.4
        card_gen = cta_card(size, title, 3.4)
        for i in range(n):
            t = i / FPS
            if t < card_start:
                img = kb(photos, size, t, scene_len)
                img.alpha_composite(_top_scrim(size))
                if t > text_in:
                    img.alpha_composite(bdg.point(lambda v: int(v * ease(seg(t, text_in, text_in + 0.5)))))
                    img = slide_fade(img, ttl, t, text_in, text_in + 0.6, dy=44)
                    img = slide_fade(img, sb, t, text_in + 0.25, text_in + 0.8, dy=36)
                img.alpha_composite(foot)
                yield img
            else:
                yield next(card_gen)
    wav = f'/tmp/{name}_{tag}.wav'
    accents = [(round((k + 0.5) * scene_len, 2), 1046.5 if k % 2 == 0 else 1318.5)
               for k in range(len(photos))]
    accents.append((round(dur - 3.4 + 0.9, 2), 1568.0))
    _AK.sl_track(wav, dur, seed=seed, accents=accents, density=0.85, fade=1.0)
    encode(frames2(), size, f'{OUT}/{name}_{tag}.mp4', audio_wav=wav, chip_brand=SL)
    print('✓', f'{name}_{tag}')

def _card_once(size, title, ct):
    yield next(cta_card(size, title, 3.4))

VARIANTS = [
    ('SL_real_residential', ['sl_02_spruce-christmas-lighting.jpg', 'sl_10_ghting-installation-greenville-sc-1.jpg',
                             'sl_08_nstallation-service-greenville-sc-2.jpg', 'sl_11_ghting-installation-greenville-sc-2.jpg'],
     'Residential', 'Homes That Glow All Season', 'Custom design • Pro install • We store them till next year', 31),
    ('SL_real_commercial', ['sl_03_nstallation-service-greenville-sc-1.jpg', 'sl_04_nstallation-service-greenville-sc-2.jpg',
                            'sl_16_hting-installation-municipalities-3.jpg'],
     'Commercial', 'Businesses That Shine Brighter', 'Storefronts • Offices • Properties — one crew, zero hassle', 37),
    ('SL_real_municipal', ['sl_05_nstallation-service-greenville-sc-3.jpg', 'sl_06_nstallation-service-greenville-sc-4.jpg',
                           'sl_18_olumbia-myrtle-beach-sc-ashevill-nc.jpg'],
     'Municipal & Events', 'Whole-Town Twinkle', 'City displays • Parks • Festivals — festival-grade at any scale', 41),
    ('SL_real_allthree', ['sl_02_spruce-christmas-lighting.jpg', 'sl_03_nstallation-service-greenville-sc-1.jpg',
                          'sl_06_nstallation-service-greenville-sc-4.jpg', 'sl_12_ghting-installation-greenville-sc-3.jpg'],
     'Residential • Commercial • Municipal', 'One Call Does It All', 'Homes, businesses and whole streets — all-inclusive pricing', 43),
    ('SL_real_process', ['sl_01_spruce-christmas-lighting-2.jpg', 'sl_14_hting-installation-municipalities-1.jpg',
                         'sl_15_hting-installation-municipalities-2.jpg', 'sl_13_ghting-installation-greenville-sc-4.jpg'],
     'The Spruce Process', 'You Never Touch a Ladder', 'We design, install, maintain and store — free season-long service', 47),
]

import sys
which = sys.argv[1] if len(sys.argv) > 1 else 'all'
for (name, photos, kicker, title, sub, seed) in VARIANTS:
    if which in ('all', name, 'feed'):
        build(name, [f'{BG}/{p}' for p in photos], kicker, title, sub, seed, 13.0, SQ, 'feed')
    if which in ('all', name, 'reel'):
        build(name, [f'{BG}/{p}' for p in photos], kicker, title, sub, seed, 15.0, ST, 'reel')
print('ALL REAL-LIGHTS VIDEOS DONE')
