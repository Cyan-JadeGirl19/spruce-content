"""Spruce Lights — 5 REAL-LIGHTS showcase videos (1080x1080, upload anywhere).
Residential / Commercial / Municipal coverage from actual Spruce install photos.
Site palette (pine + gold + serif), brand chip on every frame, music-box audio."""
import sys, math, os
sys.path.insert(0, '/home/user/spruce')
import spruce_kit as _K
_K.TEAL = (13, 27, 16, 255); _K.TEAL_D = (8, 18, 11, 255); _K.TEAL_L = (24, 44, 28, 255)
_K.SCRIM_COLOR = (2, 14, 8); _K.FOOT_DARK = (3, 20, 12); _K.CINE_SHADOW = (0.0, 0.05, 0.028)
import vidkit as _V
from vidkit import *
from spruce_kit import FONTS
import spruce_kit
_GOLD = (240, 176, 45, 255); _CREAM = (246, 240, 226, 255); _SAGE = (164, 178, 156, 255)
_V.CYAN = _GOLD; _V.LIME = _CREAM; _V.GOLD = _GOLD
CYAN = _GOLD; LIME = _CREAM; GOLD = _GOLD
import audio_kit as _AK
from PIL import Image, ImageDraw, ImageFont
import numpy as np

OUT = f'{ROOT}/videos/spruce_lights'
os.makedirs(OUT, exist_ok=True)
SLR = f'{ROOT}/assets/photos/sl_real'
SQ = (1080, 1080)

LOGO_W = load_logo(SL, light_bg=False).crop(load_logo(SL, light_bg=False).getbbox())
LOGO_W.thumbnail((640, 700), Image.LANCZOS)

_SFONTS = {}
def SF(px, wght=800):
    k = (px, wght)
    if k not in _SFONTS:
        f = ImageFont.truetype(f'{FONTS}/PlayfairDisplay.ttf', px)
        try: f.set_variation_by_axes([wght])
        except Exception: pass
        _SFONTS[k] = f
    return _SFONTS[k]

def serif_layer(size, text, px, wght=800, color=_CREAM, maxw_frac=0.84, lh=1.14, y_center=None):
    """word-wrapped centered serif layer; *starred* words render in gold"""
    W, Hh = size
    layer = Image.new('RGBA', size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    f = SF(px, wght)
    words, gold = [], False
    for ch_seg in text.split('*'):
        for w_ in ch_seg.split(' '):
            if w_: words.append((w_, gold))
        gold = not gold
    spw = d.textlength(' ', font=f)
    lines, cur, curw = [], [], 0.0
    for w_, g in words:
        ww = d.textlength(w_, font=f)
        add = ww if not cur else ww + spw
        if cur and curw + add > int(W * maxw_frac):
            lines.append(cur); cur, curw = [(w_, g)], ww
        else:
            cur.append((w_, g)); curw += add
    if cur: lines.append(cur)
    th = len(lines) * px * lh
    y = ((Hh - th) / 2 if y_center is None else y_center - th / 2) + px * 0.1
    for ln in lines:
        widths = [d.textlength(w_, font=f) for w_, _ in ln]
        x = (W - (sum(widths) + spw * (len(ln) - 1))) / 2
        for (w_, g), ww in zip(ln, widths):
            sh = Image.new('RGBA', size, (0, 0, 0, 0))
            ImageDraw.Draw(sh).text((x + 3, y + 4), w_, font=f, fill=(0, 10, 6, 200))
            layer.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)))
            d.text((x, y), w_, font=f, fill=(_GOLD if g else color))
            x += ww + spw
        y += px * lh
    return layer, th

def caps_layer(size, text, px, color=_GOLD, y_center=200, tracking=6):
    W, Hh = size
    layer = Image.new('RGBA', size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    f = F(px, "Bold")
    w = sum(d.textlength(c, font=f) + tracking for c in text) - tracking
    x = (W - w) / 2
    y = y_center
    for c in text:
        bb = d.textbbox((0, 0), c, font=f)
        ty = y - (bb[1] + bb[3]) / 2
        sh = Image.new('RGBA', size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((x + 2, ty + 3), c, font=f, fill=(0, 10, 6, 190))
        layer.alpha_composite(sh.filter(ImageFilter.GaussianBlur(4)))
        d.text((x, ty), c, font=f, fill=color)
        x += d.textlength(c, font=f) + tracking
    return layer

C_SET = [523.25, 587.33, 659.25, 783.99, 880.0, 1046.5, 1174.7, 1318.5, 1568.0, 2093.0]
def snap(fa):
    return min(C_SET, key=lambda a: abs(12 * math.log2(fa / a)))

def flash(img, t, t0):
    if t0 <= t < t0 + 0.16:
        img.alpha_composite(Image.new('RGBA', SQ, (255, 255, 255, int(150 * (1 - (t - t0) / 0.16)))))
    return img

def endcard(tagline, dur=3.6, seed=5, accent_t=1.4):
    """pine endcard: logo, serif tagline, gold CTA, footer"""
    W, H = SQ
    n = int(dur * FPS)
    base = vgrad(SQ, TEAL, TEAL_D)
    base.alpha_composite(radial_glow(SQ, (W/2, 520), W*0.7, TEAL_L, peak=40))
    sp = sparkle_field_layer(SQ, 10, n=14, ymax_frac=0.95)
    foot = brand_footer_layer(SQ, SL)
    t1, _ = serif_layer(SQ, tagline, 46, 800, _CREAM, maxw_frac=0.8, y_center=640)
    for i in range(n):
        t = i / FPS
        img = base.copy()
        e = backout(seg(t, 0.25, 1.2)); a = seg(t, 0.25, 0.9)
        lg = LOGO_W.copy()
        if a > 0:
            la = lg.getchannel('A').point(lambda v: int(v * a))
            lg.putalpha(la)
            img.alpha_composite(lg, (int((W - lg.width)/2), int(300 - lg.height/2 + (1 - e) * 60)))
        img = slide_fade(img, t1, t, 1.1, 1.8, dy=40)
        if t > 1.9:
            d = ImageDraw.Draw(img)
            e2 = ease(seg(t, 1.9, 2.5))
            cy = int(800 + (1 - e2) * 50)
            pw = 560
            pill(d, [W/2 - pw/2, cy - 52, W/2 + pw/2, cy + 52], GOLD)
            d.text((W/2, cy - 2), "Get My Free Quote", font=F(42, 'Bold'), fill=TEAL_D, anchor='mm')
        img.alpha_composite(foot)
        draw_sparkle_field(img, sp, t + seed)
        yield img

def montage(photos, kicker, headline, caption_map, dur, wav, tagline,
            seed=31, accents=None, caption_y=880):
    """photo montage: serif headline over photo 1, per-photo captions, endcard"""
    n = int((dur - 3.6) * FPS)          # photo segment only; endcard follows
    foot = brand_footer_layer(SQ, SL)
    n_photos = len(photos)
    seg_t = (dur - 3.6) / n_photos
    kick = caps_layer(SQ, kicker, 27, _GOLD, y_center=172)
    head, _ = serif_layer(SQ, headline, 62, 800, _CREAM, maxw_frac=0.82, y_center=268)
    cap_layers = []
    for cap in caption_map:
        cl, _ = serif_layer(SQ, cap, 38, 700, _CREAM, maxw_frac=0.8, y_center=caption_y)
        cap_layers.append(cl)
    for i in range(n):
        t = i / FPS
        idx = min(int(t / seg_t), n_photos - 1)
        local = t - idx * seg_t
        img = kb_frame(photos[idx], SQ, min(1.0, local / seg_t), z0=1.10, z1=1.22, grade=0.60, brighten=0.99)
        img = scrim(img, strength=0.42, top_frac=0.30, bottom_frac=0.22)
        img = cinema(img, strength=0.35)
        img.alpha_composite(kick)
        if idx == 0:
            img = slide_fade(img, head, t, 0.4, 1.2, dy=50, out=(seg_t - 0.7, seg_t - 0.2, -40))
        else:
            img = slide_fade(img, cap_layers[idx], t, idx * seg_t + 0.35, idx * seg_t + 0.95, dy=40,
                             out=(idx * seg_t + seg_t - 0.65, idx * seg_t + seg_t - 0.15, -30))
        if idx > 0:
            img = flash(img, t, idx * seg_t)
        img.alpha_composite(foot)
        yield img
    yield from endcard(tagline, seed=seed % 7, accent_t=None)

def make(name, photos, kicker, headline, caption_map, dur, tagline, seed, accent_times):
    wav = f'/tmp/{name}.wav'
    _AK.sl_track(wav, dur, seed=seed, accents=[(t, snap(f)) for t, f in accent_times],
                 density=0.9, fade=1.4)
    frames = montage(photos, kicker, headline, caption_map, dur, wav, tagline, seed=seed)
    encode(frames, SQ, f'{OUT}/{name}.mp4', audio_wav=wav, chip_brand=SL)
    print('✓', name)

# ================================================ 1. RESIDENTIAL
make('SL_showcase_residential',
     [f'{SLR}/sl_02_spruce-christmas-lighting.jpg', f'{SLR}/sl_10_ghting-installation-greenville-sc-1.jpg',
      f'{SLR}/sl_08_nstallation-service-greenville-sc-2.jpg', f'{SLR}/sl_09_nstallation-service-greenville-sc-3.jpg'],
     "RESIDENTIAL HOLIDAY LIGHTING", "Your Home, *Aglow*",
     ["Rooflines, trees & walkways", "Designed for YOUR home", "Safe. Clean. Breathtaking.", "Twinkle all season long"],
     13.6, "The Upstate's favorite home glow-up", 31,
     [(1.0, 1046.5), (2.5, 784.0), (4.0, 1046.5), (5.5, 1318.5), (7.0, 880.0), (10.0, 1568.0)])

# ================================================ 2. COMMERCIAL
make('SL_showcase_commercial',
     [f'{SLR}/sl_03_nstallation-service-greenville-sc-1.jpg', f'{SLR}/sl_18_olumbia-myrtle-beach-sc-ashevill-nc.jpg',
      f'{SLR}/sl_04_nstallation-service-greenville-sc-2.jpg'],
     "COMMERCIAL & PROPERTY LIGHTING", "Properties That *Draw Crowds*",
     ["Plazas, retail & storefronts", "Corridors that draw crowds", "Peace Center–grade polish"],
     12.6, "Light that brings customers in", 32,
     [(1.0, 880.0), (2.5, 1046.5), (4.0, 784.0), (5.5, 1174.7), (9.0, 1568.0)])

# ================================================ 3. MUNICIPAL
make('SL_showcase_municipal',
     [f'{SLR}/sl_14_hting-installation-municipalities-1.jpg', f'{SLR}/sl_16_hting-installation-municipalities-3.jpg',
      f'{SLR}/sl_05_nstallation-service-greenville-sc-3.jpg'],
     "MUNICIPAL & TOWN DISPLAYS", "Whole Towns, *Twinkling*",
     ["Crews on signature trees", "Plazas & streetscapes", "Crowd-pleasing displays"],
     12.6, "Make your town the destination", 33,
     [(1.0, 784.0), (2.5, 1046.5), (4.0, 1318.5), (5.5, 880.0), (9.0, 1568.0)])

# ================================================ 4. PORCHES TO MAIN STREET (all three)
make('SL_showcase_everywhere',
     [f'{SLR}/sl_02_spruce-christmas-lighting.jpg', f'{SLR}/sl_18_olumbia-myrtle-beach-sc-ashevill-nc.jpg',
      f'{SLR}/sl_16_hting-installation-municipalities-3.jpg'],
     "RESIDENTIAL • COMMERCIAL • MUNICIPAL", "From Front Porches to *Main Street*",
     ["Homes", "Businesses", "Whole towns"],
     12.6, "One call lights it all", 34,
     [(1.0, 1046.5), (2.5, 880.0), (4.0, 1318.5), (9.0, 1568.0)])

# ================================================ 5. BOOK OCTOBER (mix + urgency)
make('SL_showcase_book_october',
     [f'{SLR}/sl_07_nstallation-service-greenville-sc-1.jpg', f'{SLR}/sl_11_ghting-installation-greenville-sc-2.jpg',
      f'{SLR}/sl_13_ghting-installation-greenville-sc-4.jpg'],
     "NOW BOOKING OCTOBER", "Prime Slots *Fill First*",
     ["Best design dates go first", "Up before the family arrives", "Zero December scramble"],
     12.6, "Lock your October slot today", 35,
     [(1.0, 880.0), (2.5, 1318.5), (4.0, 1046.5), (9.0, 1568.0)])

print('ALL 5 SHOWCASE VIDEOS DONE')
