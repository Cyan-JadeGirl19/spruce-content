"""Spruce Lights — 5 REAL-PHOTO video posts (residential / commercial / municipal).
Format: 1080x1350 (4:5) — uploads cleanly to FB/IG feed, LinkedIn, X, TikTok, YT Shorts.
Website-Edition look: pine surfaces, Playfair serif, gold accents, brand chip, soothing twinkle."""
import sys, math, os
sys.path.insert(0, '/home/user/spruce')
import spruce_kit as _K
_K.TEAL = (13, 27, 16, 255); _K.TEAL_D = (8, 18, 11, 255); _K.TEAL_L = (24, 44, 28, 255)
_K.SCRIM_COLOR = (2, 14, 8); _K.FOOT_DARK = (3, 20, 12); _K.CINE_SHADOW = (0.0, 0.05, 0.028)
from vidkit import *
from spruce_kit import FONTS
import vidkit as _V
_GOLD = (240, 176, 45, 255); _CREAM = (246, 240, 226, 255)
_V.CYAN = _GOLD; _V.LIME = _CREAM; _V.GOLD = _GOLD
CYAN = _GOLD; LIME = _CREAM; GOLD = _GOLD
from PIL import Image, ImageDraw, ImageFont
import audio_kit as _AK

def twinkle_wav(path, dur, key=None, seed=7, accents=None, fade=1.6, rate=44100):
    kind = 'promo' if dur > 9 else 'ba'
    return _AK.sl_track(path, dur, seed=seed, accents=accents,
                        density=_AK.PRESETS[kind], fade=1.4)

OUT = f'{ROOT}/videos/spruce_lights/real'
os.makedirs(OUT, exist_ok=True)
SLR = f'{ROOT}/assets/photos/sl_real'
SIZE = (1080, 1350)

LOGO_W = load_logo(SL, light_bg=False).crop(load_logo(SL, light_bg=False).getbbox())
LOGO_W.thumbnail((760, 560), Image.LANCZOS)

_SFC = {}
def SF(px, wght=800):
    k = (px, wght)
    if k not in _SFC:
        f = ImageFont.truetype(f'{FONTS}/PlayfairDisplay.ttf', px)
        try: f.set_variation_by_axes([wght])
        except Exception: pass
        _SFC[k] = f
    return _SFC[k]

def serif_layer(text, px, color=_CREAM, wght=800, y_center=200, maxw_frac=0.86):
    layer = Image.new('RGBA', SIZE, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    f = SF(px, wght)
    lines = wrap_text(text, f, int(1080 * maxw_frac), d)
    th = len(lines) * px * 1.16
    y = y_center - th / 2 + px * 0.1
    for ln in lines:
        w = d.textlength(ln, font=f)
        sh = Image.new('RGBA', SIZE, (0, 0, 0, 0))
        ImageDraw.Draw(sh).text(((1080 - w) / 2 + 3, y + 4), ln, font=f, fill=(0, 10, 6, 190))
        layer.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)))
        d.text(((1080 - w) / 2, y), ln, font=f, fill=color)
        y += px * 1.16
    return layer

def kicker_layer(text, y):
    layer = Image.new('RGBA', SIZE, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    f = F(30, 'SemiBold')
    tw = d.textlength(text.upper(), font=f)
    x0, x1 = 540 - tw / 2 - 62, 540 + tw / 2 + 38
    d.rounded_rectangle([x0, y - 30, x1, y + 30], 30, fill=(13, 25, 15, 210),
                        outline=(240, 176, 45, 170), width=2)
    d.ellipse([x0 + 28, y - 6, x0 + 40, y + 6], fill=GOLD)
    d.text((x0 + 58, y - 1), text.upper(), font=f, fill=GOLD, anchor='lm')
    return layer

def end_card(headline, sub='(864) 288-2459  •  sprucelights.com'):
    base = vgrad(SIZE, TEAL, TEAL_D)
    base.alpha_composite(radial_glow(SIZE, (540, 640), 700, (24, 44, 28), peak=70))
    img = base.copy()
    d = ImageDraw.Draw(img)
    d.line([(0, 1096), (454, 1096)], fill=GOLD, width=5)
    d.line([(462, 1096), (626, 1096)], fill=_CREAM[:3] + (230,), width=5)
    return img, headline, sub

def end_frames(img0, headline, sub, n):
    lg = LOGO_W.copy()
    lh = lg.height
    for i in range(n):
        t = i / FPS
        img = img0.copy()
        e = backout(seg(t, 0.25, 1.3)); a = seg(t, 0.25, 1.0)
        g = lg.copy()
        if a > 0:
            la = g.getchannel('A').point(lambda v: int(v * a))
            g.putalpha(la)
            img.alpha_composite(g, (int((1080 - g.width) / 2), int(560 - lh / 2 + (1 - e) * 110)))
        if t > 1.0:
            ea = ease(seg(t, 1.0, 1.7))
            tl = serif_layer(headline, 54, _CREAM, 760, y_center=880)
            la = tl.getchannel('A').point(lambda v: int(v * ea))
            tl.putalpha(la)
            img.alpha_composite(tl)
        if t > 1.5:
            ea = ease(seg(t, 1.5, 2.1))
            ts, _ = text_layer(SIZE, sub, 'SemiBold', 40, color=(196, 176, 120, 255), y_center=1000)
            la = ts.getchannel('A').point(lambda v: int(v * ea))
            ts.putalpha(la)
            img.alpha_composite(ts)
        if t > 2.1:
            d = ImageDraw.Draw(img)
            e = ease(seg(t, 2.1, 2.7))
            pw, ph = 560, 104
            cy = int(1180 + (1 - e) * 50)
            pill(d, [540 - pw / 2, cy - ph / 2, 540 + pw / 2, cy + ph / 2], GOLD)
            d.text((540, cy - 2), "Get My Free Quote", font=F(42, 'Bold'), fill=(13, 25, 15), anchor='mm')
        yield img

def cap_footer(img, label):
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([40, 1196, 40 + 20 + d.textlength(label.upper(), font=F(26, 'SemiBold')) + 60, 1196 + 62],
                        31, fill=(13, 25, 15, 205), outline=(240, 176, 45, 160), width=2)
    d.ellipse([70, 1219, 82, 1231], fill=GOLD)
    d.text((94, 1226), label.upper(), font=F(26, 'SemiBold'), fill=GOLD, anchor='lm')
    return img

def kb(photo, t, z0=1.10, z1=1.20, pan=(0, 0), brighten=1.02):
    return kb_frame(f'{SLR}/{photo}', SIZE, t, z0=z0, z1=z1, pan=pan, brighten=brighten, grade=0.42)

def dur_of(n_notes):  # helper not used
    return n_notes

# ================================================ 1. RESIDENTIAL (10.5s)
def v_resi_full():
    dur = 12.0; n = int(dur * FPS)
    kicks = kicker_layer('Residential', 150)
    img0, h, s = end_card('Aglow All Season Long', '(864) 288-2459  •  sprucelights.com')
    end = list(end_frames(img0, h, s, int(3.6 * FPS)))
    slides = ['sl_02_spruce-christmas-lighting.jpg',
              'sl_09_nstallation-service-greenville-sc-3.jpg',
              'sl_11_griswold' if False else 'sl_08_nstallation-service-greenville-sc-2.jpg']
    heads = [('Your home,', '*aglow* all season.'), ('Rooflines,', 'trees & garlands,'), ('installed, serviced,', 'stored — done for you.')]
    for i in range(n):
        t = i / FPS
        if t >= 8.4:
            yield end[i - int(8.4 * FPS)]
            continue
        seg_i = min(2, int(t // 2.8))
        tt = (t - seg_i * 2.8) / 2.8
        img = kb(slides[seg_i], tt, z0=1.12 if seg_i % 2 else 1.04,
                 z1=1.04 if seg_i % 2 else 1.12)
        img.alpha_composite(kicks)
        h1, h2 = heads[seg_i]
        if seg_i == 0:
            img.alpha_composite(serif_layer(h1, 58, _CREAM, 780, y_center=1084, maxw_frac=0.86))
            img.alpha_composite(serif_layer(h2, 58, (240, 176, 45, 255), 780, y_center=1152, maxw_frac=0.86))
        else:
            img.alpha_composite(serif_layer(h1, 52, _CREAM, 780, y_center=1088, maxw_frac=0.86))
            img.alpha_composite(serif_layer(h2, 52, (240, 176, 45, 255), 780, y_center=1154, maxw_frac=0.86))
        img = cap_footer(img, 'residential holiday lighting')
        yield img

# ================================================ 2. COMMERCIAL (12s)
def v_commercial():
    dur = 12.0; n = int(dur * FPS)
    kicks = kicker_layer('Commercial', 150)
    img0, h, s = end_card('Businesses That Glow', '(864) 288-2459  •  sprucelights.com')
    end = list(end_frames(img0, h, s, int(3.6 * FPS)))
    slides = ['sl_04_nstallation-service-greenville-sc-2.jpg' if os.path.exists(f'{SLR}/sl_04_nstallation-service-greenville-sc-2.jpg') else 'sl_04_nstallation-service-greenville-sc-2.jpg',
              'sl_06_nstallation-service-greenville-sc-4.jpg',
              'sl_07_nstallation-service-greenville-sc-1.jpg']
    heads = [('Storefronts, offices', '& commercial plazas,'), ('lit to welcome', 'every customer,'), ('installed around', 'your business hours.')]
    for i in range(n):
        t = i / FPS
        if t >= 8.4:
            yield end[i - int(8.4 * FPS)]
            continue
        seg_i = min(2, int(t // 2.8))
        tt = (t - seg_i * 2.8) / 2.8
        img = kb(slides[seg_i], tt, z0=1.06, z1=1.14, pan=(0.2, 0) if seg_i == 1 else (0, 0))
        img.alpha_composite(kicks)
        h1, h2 = heads[seg_i]
        img.alpha_composite(serif_layer(h1, 50, _CREAM, 780, y_center=1088, maxw_frac=0.88))
        img.alpha_composite(serif_layer(h2, 50, (240, 176, 45, 255), 780, y_center=1154, maxw_frac=0.88))
        img = cap_footer(img, 'commercial holiday lighting')
        yield img

# ================================================ 3. MUNICIPAL (12s)
def v_municipal():
    dur = 12.0; n = int(dur * FPS)
    kicks = kicker_layer('Municipal', 150)
    img0, h, s = end_card('Light Up Your Town', '(864) 288-2459  •  sprucelights.com')
    end = list(end_frames(img0, h, s, int(3.6 * FPS)))
    slides = ['sl_03_nstallation-service-greenville-sc-1.jpg',
              'sl_05_nstallation-service-greenville-sc-3.jpg',
              'sl_16_hting-installation-municipalities-3.jpg']
    heads = [('City trees, parks', '& downtown streets,'), ('festival-grade displays', 'your town will love,'), ('from design to takedown —', 'all handled.')]
    for i in range(n):
        t = i / FPS
        if t >= 8.4:
            yield end[i - int(8.4 * FPS)]
            continue
        seg_i = min(2, int(t // 2.8))
        tt = (t - seg_i * 2.8) / 2.8
        img = kb(slides[seg_i], tt, z0=1.08, z1=1.16, pan=(-0.2, 0) if seg_i == 2 else (0.15, 0))
        img.alpha_composite(kicks)
        h1, h2 = heads[seg_i]
        img.alpha_composite(serif_layer(h1, 50, _CREAM, 780, y_center=1088, maxw_frac=0.88))
        img.alpha_composite(serif_layer(h2, 50, (240, 176, 45, 255), 780, y_center=1154, maxw_frac=0.88))
        img = cap_footer(img, 'municipal & HOA displays')
        yield img

# ================================================ 4. BEFORE / AFTER — REAL SAME-SCENE (12s)
def v_before_after():
    dur = 12.0; n = int(dur * FPS)
    A0 = bg_photo(f'{SLR}/sl_17_hting-installation-municipalities-4.jpg', 1080, 1350, focus=0.5, brighten=1.0)
    B0 = bg_photo(f'{ROOT}/assets/bg/sl17_night.jpg', 1080, 1350, focus=0.5)
    img0, h, s = end_card('The Spruce Difference', '(864) 288-2459  •  sprucelights.com')
    end = list(end_frames(img0, h, s, int(3.6 * FPS)))
    lbl_a = side_label('BEFORE', 810, (225, 228, 228, 255))
    lbl_b = side_label('AFTER ✨', 270, (240, 176, 45, 255))
    for i in range(n):
        t = i / FPS
        if t >= 8.4:
            yield end[i - int(8.4 * FPS)]
            continue
        if t < 7.0:
            a = A0.copy(); b = B0.copy()
            x = 1080 * (0.5 + 0.46 * math.sin((t / 7.0) * math.pi * 2 - math.pi / 2))
            img = wipe(a, b, int(x))
            d = ImageDraw.Draw(img)
            d.line([(int(x), 0), (int(x), 1350)], fill=CREAM, width=6)
            if x < 810: img.alpha_composite(lbl_a)
            if x > 270: img.alpha_composite(lbl_b)
        else:
            img = kb_frame(f'{ROOT}/assets/bg/sl17_night.jpg', SIZE, (t - 7.0) / 1.4, z0=1.0, z1=1.06, grade=0.25)
        img = cap_footer(img, 'same property — before & after')
        yield img

def side_label(txt, cy, color):
    lay = Image.new('RGBA', SIZE, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.text((540, cy), txt, font=F(52, 'ExtraBold'), fill=color, anchor='mm',
           stroke_width=2, stroke_fill=(0, 18, 10, 210))
    return lay

# ================================================ 5. MIXED REEL (15s)
def v_mixed():
    dur = 15.0; n = int(dur * FPS)
    img0, h, s = end_card('Every Property Glows', '(864) 288-2459  •  sprucelights.com')
    end = list(end_frames(img0, h, s, int(3.8 * FPS)))
    shots = [('sl_02_spruce-christmas-lighting.jpg', 'homes'), ('sl_04_nstallation-service-greenville-sc-2.jpg' if os.path.exists(f'{SLR}/sl_04_nstallation-service-greenville-sc-2.jpg') else 'sl_05_nstallation-service-greenville-sc-3.jpg', 'businesses'), ('sl_03_nstallation-service-greenville-sc-1.jpg', 'whole towns')]
    heads = [('Homes', 'that stop traffic.'), ('Businesses', 'that welcome.'), ('Towns', 'that celebrate.')]
    seg_dur = 3.6
    for i in range(n):
        t = i / FPS
        if t >= 11.2:
            yield end[i - int(11.2 * FPS)]
            continue
        seg_i = min(2, int(t // seg_dur))
        tt = (t - seg_i * seg_dur) / seg_dur
        img = kb(shots[seg_i][0], tt, z0=1.06 + 0.05 * seg_i, z1=1.16 + 0.03 * seg_i)
        h1, h2 = heads[seg_i]
        img.alpha_composite(serif_layer(h1, 60, _CREAM, 800, y_center=1078, maxw_frac=0.86))
        img.alpha_composite(serif_layer(h2, 60, (240, 176, 45, 255), 800, y_center=1148, maxw_frac=0.86))
        img = cap_footer(img, f'{shots[seg_i][1]} — spruce holiday lighting')
        yield img

# ================================================ render all 5
def acc_at(end_start):
    return [(end_start + 0.6, 1046.5), (end_start + 1.6, 1318.5)]

print('residential...'); twinkle_wav('/tmp/r1.wav', 12.0, seed=31, accents=acc_at(8.4))
encode(v_resi_full(), SIZE, f'{OUT}/SL_real_residential.mp4', chip_brand=SL, audio_wav='/tmp/r1.wav'); print('ok 1/5')
print('commercial...');  twinkle_wav('/tmp/r2.wav', 12.0, seed=37, accents=acc_at(8.4))
encode(v_commercial(), SIZE, f'{OUT}/SL_real_commercial.mp4', chip_brand=SL, audio_wav='/tmp/r2.wav'); print('ok 2/5')
print('municipal...');   twinkle_wav('/tmp/r3.wav', 12.0, seed=41, accents=acc_at(8.4))
encode(v_municipal(), SIZE, f'{OUT}/SL_real_municipal.mp4', chip_brand=SL, audio_wav='/tmp/r3.wav'); print('ok 3/5')
print('before/after...'); twinkle_wav('/tmp/r4.wav', 12.0, seed=43, accents=acc_at(8.4))
encode(v_before_after(), SIZE, f'{OUT}/SL_real_before_after.mp4', chip_brand=SL, audio_wav='/tmp/r4.wav'); print('ok 4/5')
print('mixed reel...');  twinkle_wav('/tmp/r5.wav', 15.0, seed=47, accents=[(11.8, 1046.5), (12.8, 1318.5)])
encode(v_mixed(), SIZE, f'{OUT}/SL_real_all_properties.mp4', chip_brand=SL, audio_wav='/tmp/r5.wav'); print('ok 5/5')
print('ALL 5 REAL-PHOTO VIDEOS DONE')
