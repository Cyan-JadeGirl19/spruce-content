#!/usr/bin/env python3
"""5 real-lights showcase videos for Spruce Lights — residential / commercial /
municipal + true before/after + grand tour. Feed (1:1) + Story (9:16) for each.
Soothing quiet music-box twinkle. Chip + footer + serif titles. Upload-safe MP4."""
import sys, math
sys.path.insert(0, '/home/user/spruce')
import spruce_kit as _K
_K.TEAL = (13, 27, 16, 255); _K.TEAL_D = (8, 18, 11, 255); _K.TEAL_L = (24, 44, 28, 255)
_K.SCRIM_COLOR = (2, 14, 8); _K.FOOT_DARK = (3, 20, 12); _K.CINE_SHADOW = (0.0, 0.05, 0.028)
import vidkit as _V
_V.CYAN = (240, 176, 45, 255); _V.LIME = (246, 240, 226, 255); _V.GOLD = (240, 176, 45, 255)
from vidkit import *
import audio_kit as AK
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os

OUT = f'{ROOT}/videos/spruce_lights/showcase'
os.makedirs(OUT, exist_ok=True)
BG = f'{ROOT}/assets/bg'
SLR = f'{ROOT}/assets/photos/sl_real'
SQ, ST = (1080, 1080), (1080, 1920)
CREAM = (246, 240, 226); GOLD = (240, 176, 45); SAGE = (164, 178, 156)

_SFC = {}
def SF(px, wght=800):
    k = (px, wght)
    if k not in _SFC:
        f = ImageFont.truetype(f'{FONTS}/PlayfairDisplay.ttf', px)
        try: f.set_variation_by_axes([wght])
        except Exception: pass
        _SFC[k] = f
    return _SFC[k]

def serif_layer(size, text, px, wght=800, color=CREAM, maxw_frac=0.84, y_center=None, lh=1.16):
    W, H = size
    layer = Image.new('RGBA', size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    f = SF(px, wght)
    lines = wrap_text(text, f, int(W * maxw_frac), d)
    th = len(lines) * px * lh
    y = ((H - th) / 2 if y_center is None else y_center - th / 2) + px * 0.1
    for ln in lines:
        w = d.textlength(ln, font=f)
        sh = Image.new('RGBA', size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).text(((W - w) / 2 + 3, y + 4), ln, font=f, fill=(0, 10, 6, 190))
        layer.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)))
        d.text(((W - w) / 2, y), ln, font=f, fill=color)
        y += px * lh
    return layer, th

def caps_layer(size, text, px, color=GOLD, y_center=None, tracking=6, pill=False):
    W, H = size
    layer = Image.new('RGBA', size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    f = ImageFont.truetype(f'{FONTS}/Poppins-Bold.ttf', px)
    tw = sum(d.textlength(c, font=f) + tracking for c in text) - tracking
    x = (W - tw) / 2; y = (H / 2 if y_center is None else y_center)
    if pill:
        d.rounded_rectangle([x - 34, y - px * 0.85, x + tw + 34, y + px * 0.85], 24,
                            fill=(13, 25, 15, 165), outline=(240, 176, 45, 120), width=2)
    for c in text:
        sh = Image.new('RGBA', size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((x + 2, y + 3), c, font=f, fill=(0, 10, 6, 170), anchor='lm')
        layer.alpha_composite(sh.filter(ImageFilter.GaussianBlur(4)))
        d.text((x, y), c, font=f, fill=color, anchor='lm')
        x += d.textlength(c, font=f) + tracking
    return layer

def gentle_wav(path, dur, seed, accents=None):
    """soothing: sparse, quiet music-box"""
    return AK.sl_track(path, dur, seed=seed, accents=accents or [], density=0.5,
                       fade=min(1.6, dur / 4), gain=0.42)

def chip(size):
    return brand_chip_layer(size, SL)

def footer(size):
    return brand_footer_layer(size, SL)

def shots_cycle(shots, size, dur, grade=0.62, zb=1.10, ze=1.22):
    """yield kb frames with a soft white-pop cut between shots"""
    n = len(shots); seg = dur / n
    for i in range(int(dur * FPS)):
        t = i / FPS
        idx = min(int(t / seg), n - 1)
        lt = (t - idx * seg) / seg
        img = kb_frame(shots[idx], size, lt, z0=zb, z1=ze, grade=grade)
        frac = t - idx * seg
        if frac < 0.14 and idx > 0:
            img.alpha_composite(Image.new('RGBA', size, (255, 255, 255, int(120 * (1 - frac / 0.14)))))
        yield img

def compose(size, shots, dur, kicker, title_lines, tagline, audio_seed, fn_story):
    """one video: photos + kicker + title + tagline + CTA; feed & story layouts"""
    W, H = size
    ch = chip(size); ft = footer(size)
    sp = sparkle_field_layer(size, 7, n=10, ymax_frac=0.24)
    kick_y = int(H * 0.14) if H > 1200 else int(H * 0.16)
    title_y = kick_y + 74 if H > 1200 else kick_y + 62
    tpx = 74 if H > 1200 else 56
    t_layers = [serif_layer(size, ln, tpx, 800, CREAM, 0.86, title_y + k * tpx * 1.16)
                for k, ln in enumerate(title_lines)]
    tag = caps_layer(size, kicker, 25, GOLD, kick_y - 6, tracking=7)
    cta_t, _ = serif_layer(size, tagline, 40, 700, CREAM, 0.8, int(H * 0.80))
    cta_pill_t = int(H * 0.80) + 120 if H > 1200 else int(H * 0.80) + 96

    def frames():
        base = shots_cycle(shots, size, dur)
        for i in range(int(dur * FPS)):
            t = i / FPS
            img = next(base)
            # gentle bottom gradient for legibility
            ov = vgrad(size, (13, 27, 16, 0), (13, 27, 16, 185))
            img.alpha_composite(ov.point(lambda v: int(v * 0.55)))
            e = ease(seg(t, 0.5, 1.4))
            if e > 0:
                tl = tag.getchannel('A').point(lambda v: int(v * e))
                img.alpha_composite(Image.new('RGBA', size, (0, 0, 0, 0)), (0, 0))
                img.alpha_composite(_apply(tag, e))
            for k, (lay, _) in enumerate(t_layers):
                e2 = ease(seg(t, 0.9 + k * 0.35, 1.8 + k * 0.35))
                if e2 > 0:
                    img.alpha_composite(_apply(lay, e2))
            e3 = ease(seg(t, dur - 4.2, dur - 3.4))
            if e3 > 0:
                img.alpha_composite(_apply(cta_t, e3))
                d = ImageDraw.Draw(img)
                pe = ease(seg(t, dur - 3.9, dur - 3.2))
                if pe > 0:
                    pw, ph = 560, 96
                    cy = int(cta_pill_t + (1 - pe) * 40)
                    d.rounded_rectangle([W/2 - pw/2, cy - ph/2, W/2 + pw/2, cy + ph/2], 48,
                                        fill=(240, 176, 45, int(255 * pe)))
                    d.text((W/2, cy - 2), "Get My Free Quote", font=ImageFont.truetype(
                        f'{FONTS}/Poppins-Bold.ttf', 40), fill=(13, 25, 15), anchor='mm')
            img.alpha_composite(ft)
            img.alpha_composite(ch)
            draw_sparkle_field(img, sp, t)
            yield img
    wav = f'/tmp/show_{audio_seed}.wav'
    gentle_wav(wav, dur, audio_seed)
    encode(frames(), size, fn_story, audio_wav=wav, crf=23)

def _apply(layer, e):
    a = layer.getchannel('A').point(lambda v: int(v * e))
    l2 = layer.copy(); l2.putalpha(a); return l2

# ================================================================ the 5 variants
V = [
    dict(name='showcase_residential', seed=101,
         kicker='RESIDENTIAL • GREENVILLE SC',
         title=['Homes That', 'Glow All Season'],
         tagline='Custom design for your home',
         shots=[f'{SLR}/sl_02_spruce-christmas-lighting.jpg',
                f'{SLR}/sl_07_nstallation-service-greenville-sc-1.jpg',
                f'{SLR}/sl_11_ghting-installation-greenville-sc-2.jpg']),
    dict(name='showcase_commercial', seed=202,
         kicker='COMMERCIAL PROPERTIES',
         title=['Storefronts &', 'Offices That Shine'],
         tagline='Commercial-grade displays, done for you',
         shots=[f'{SLR}/sl_04_nstallation-service-greenville-sc-2.jpg',
                f'{SLR}/sl_05_nstallation-service-greenville-sc-3.jpg']),
    dict(name='showcase_municipal', seed=303,
         kicker='MUNICIPAL & TOWN DISPLAYS',
         title=['Light Up the', 'Whole Town'],
         tagline='Plazas • parks • streetscapes',
         shots=[f'{SLR}/sl_03_nstallation-service-greenville-sc-1.jpg',
                f'{SLR}/sl_06_nstallation-service-greenville-sc-4.jpg',
                f'{SLR}/sl_16_hting-installation-municipalities-3.jpg']),
    dict(name='showcase_before_after', seed=404,
         kicker='BEFORE → AFTER • SAME HOME',
         title=['From Everyday', 'To Enchanting'],
         tagline='One call — we design, install, store',
         shots=[]),  # special wipe renderer below
    dict(name='showcase_tour', seed=505,
         kicker='RESIDENTIAL • COMMERCIAL • MUNICIPAL',
         title=['One Call.', 'Every Light.'],
         tagline='Free quote • free season-long service',
         shots=[f'{SLR}/sl_08_nstallation-service-greenville-sc-2.jpg',
                f'{SLR}/sl_04_nstallation-service-greenville-sc-2.jpg',
                f'{SLR}/sl_16_hting-installation-municipalities-3.jpg',
                f'{SLR}/sl_02_spruce-christmas-lighting.jpg']),
]

def ba_frames(size, dur):
    """true same-house wipe: day photo -> its real night version"""
    W, H = size
    ch = chip(size); ft = footer(size)
    A0 = bg_photo(f'{BG}/sl_house_day.jpg', W, H, focus=0.5, brighten=1.0)
    B0 = bg_photo(f'{BG}/sl_house_night_real.jpg', W, H, focus=0.5)
    lbl = caps_layer(size, 'SAME HOME — ONE AFTERNOON', 24, GOLD, int(H * 0.12), 6, pill=True)
    cap, _ = serif_layer(size, 'From Everyday To Enchanting', 58 if H > 1200 else 48, 800,
                         CREAM, 0.84, int(H * 0.80))
    def frames():
        n = int(dur * FPS)
        for i in range(n):
            t = i / FPS
            x = W * (0.5 + 0.46 * math.sin((t / dur) * 2 * math.pi - math.pi / 2))
            img = wipe(A0.copy(), B0.copy(), int(x))
            d = ImageDraw.Draw(img)
            d.line([(int(x), 0), (int(x), H)], fill=(246, 240, 226), width=5)
            e = ease(seg(t, 0.4, 1.2))
            if e > 0: img.alpha_composite(_apply(lbl, e))
            e2 = ease(seg(t, dur - 3.6, dur - 2.8))
            if e2 > 0: img.alpha_composite(_apply(cap, e2))
            img.alpha_composite(ft); img.alpha_composite(ch)
            yield img
    wav = '/tmp/show_ba.wav'
    gentle_wav(wav, dur, 404)
    encode(frames(), size, f'{OUT}/SL_showcase_before_after_{"story" if H > 1200 else "feed"}.mp4', audio_wav=wav, crf=23)

for v in V:
    dur = 12.0
    if v['name'] == 'showcase_before_after':
        dur = 10.0
        ba_frames(SQ, dur)
        ba_frames(ST, dur)
        print('✓ before/after (feed + story)')
        continue
    compose(SQ, v['shots'], dur, v['kicker'], v['title'], v['tagline'], v['seed'],
            f"{OUT}/SL_{v['name']}_feed.mp4")
    compose(ST, v['shots'], dur + 1.0, v['kicker'], v['title'], v['tagline'], v['seed'],
            f"{OUT}/SL_{v['name']}_story.mp4")
    print('✓', v['name'], '(feed + story)')
print('ALL 5 SHOWCASES DONE (10 files)')
