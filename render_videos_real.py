"""5 real-lights Spruce Lights videos — residential / commercial / municipal /
crew / showcase. Exported in 1080x1920 (reels/stories/TikTok) and 1080x1350
(IG/FB feed). Website-Edition look, brand chip + footer, soothing soft twinkle."""
import sys, math
sys.path.insert(0, '/home/user/spruce')
import spruce_kit as _K
_K.TEAL = (13, 27, 16, 255); _K.TEAL_D = (8, 18, 11, 255); _K.TEAL_L = (24, 44, 28, 255)
_K.SCRIM_COLOR = (2, 14, 8); _K.FOOT_DARK = (3, 20, 12); _K.CINE_SHADOW = (0.0, 0.05, 0.028)
import templates as _T
for _n in ('TEAL', 'TEAL_D', 'TEAL_L'):
    setattr(_T, _n, getattr(_K, _n))
from vidkit import *
import audio_kit as _AK
from spruce_kit import FONTS
from PIL import ImageFont, ImageFilter
import numpy as np

OUT = f'{ROOT}/videos/spruce_lights_real'
os.makedirs(OUT, exist_ok=True)
BG = f'{ROOT}/assets/bg'
SLR = f'{ROOT}/assets/photos/sl_real'
ST, SQ4 = (1080, 1920), (1080, 1350)

_GOLD = (240, 176, 45, 255); _CREAM = (246, 240, 226, 255)
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
    W, Hh = size
    layer = Image.new('RGBA', size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    f = SF(px, wght)
    lines = wrap_text(text, f, int(W * maxw_frac), d)
    th = len(lines) * px * lh
    y = ((Hh - th) / 2 if y_center is None else y_center - th / 2) + px * 0.1
    for ln in lines:
        w = d.textlength(ln, font=f)
        sh = Image.new('RGBA', size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).text(((W - w) / 2 + 3, y + 4), ln, font=f, fill=(0, 10, 6, 190))
        layer.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)))
        d.text(((W - w) / 2, y), ln, font=f, fill=color)
        y += px * lh
    return layer, th

LOGO_W = load_logo(SL, light_bg=False)

def intro_card(size, line1, line2):
    W, H = size
    img = vgrad(size, TEAL, TEAL_D)
    img.alpha_composite(radial_glow(size, (W/2, H*0.42), W*0.75, (240, 176, 45), peak=40))
    sp = sparkle_field_layer(size, 21, n=14, ymax_frac=0.9)
    draw_sparkle_field(img, sp, 1.0)
    lg = LOGO_W.copy(); lg.thumbnail((int(W*0.5), int(H*0.2)), Image.LANCZOS)
    img.alpha_composite(lg, ((W - lg.width)//2, int(H*0.22)))
    d = ImageDraw.Draw(img)
    t1, h1 = serif_layer(size, line1, 66 if H > 1400 else 56, 800, _CREAM, maxw_frac=0.86, y_center=H*0.62)
    t2, h2 = serif_layer(size, line2, 50 if H > 1400 else 44, 800, _GOLD, maxw_frac=0.8, y_center=H*0.62 + h1 + 8)
    img.alpha_composite(t1); img.alpha_composite(t2)
    return img

def cta_card(size):
    W, H = size
    img = vgrad(size, TEAL, TEAL_D)
    img.alpha_composite(radial_glow(size, (W/2, H*0.4), W*0.7, (240, 176, 45), peak=36))
    sp = sparkle_field_layer(size, 5, n=12, ymax_frac=0.85)
    draw_sparkle_field(img, sp, 3.0)
    lg = LOGO_W.copy(); lg.thumbnail((int(W*0.44), int(H*0.16)), Image.LANCZOS)
    img.alpha_composite(lg, ((W - lg.width)//2, int(H*0.30)))
    d = ImageDraw.Draw(img)
    pw = 520
    cy = int(H*0.62)
    d.rounded_rectangle([W/2 - pw/2, cy - 52, W/2 + pw/2, cy + 52], 52, fill=_GOLD)
    d.text((W/2, cy - 3), "Get My Free Quote", font=F(42, 'Bold'), fill=(13, 25, 15), anchor='mm')
    d.text((W/2, cy + 108), "(864) 288-2459  ·  sprucelights.com", font=F(30, 'SemiBold'),
           fill=(205, 220, 208, 255), anchor='mm')
    return img

def label_pill(size, text):
    W, H = size
    layer = Image.new('RGBA', size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    f = F(34, 'Bold')
    tw = d.textlength(text, font=f)
    x0, y0 = W/2 - tw/2 - 40, H*0.74
    d.rounded_rectangle([x0, y0, x0 + tw + 80, y0 + 74], 37, fill=(13, 25, 15, 205),
                        outline=(240, 176, 45, 200), width=3)
    d.text((W/2, y0 + 36), text, font=f, fill=_CREAM, anchor='mm')
    return layer

def photo_seg(size, path, t, dur, label):
    W, H = size
    img = kb_frame(path, size, t / dur, z0=1.06, z1=1.18, grade=0.55)
    img.alpha_composite(vgrad(size, (2, 10, 5, 0), (2, 10, 5, 170)).point(lambda v: int(v * 0.8)))
    img.alpha_composite(label_pill(size, label))
    return img

def real_video(size, photos, labels, line1, line2, cta_label="BOOK YOUR DESIGN SLOT"):
    """timeline: intro 2.0s — photos 2.6s each w/ 0.4 crossfades — CTA 2.6s"""
    W, H = size
    t_intro, t_photo, t_cta = 2.0, 2.6, 2.6
    dur = t_intro + len(photos) * t_photo + t_cta
    foot = brand_footer_layer(size, SL)
    intro = intro_card(size, line1, line2)
    cta = cta_card(size)
    segs = []
    for p, lab in zip(photos, labels):
        segs.append((photo_seg(size, p, 0, t_photo, lab), label_pill(size, lab)))
    n = int(dur * FPS)
    for i in range(n):
        t = i / FPS
        if t < t_intro:
            img = intro.copy()
            e = ease(seg(t, 0.15, 0.9))
            img.alpha_composite(Image.new('RGBA', size, (5, 10, 6, int(255 * (1 - e)))))
        elif t < t_intro + len(photos) * t_photo:
            k = (t - t_intro) / t_photo
            idx = min(int(k), len(photos) - 1)
            lt = k - idx
            base, lbl = segs[idx]
            img = photo_seg(size, photos[idx], lt * t_photo, t_photo, labels[idx])
            if idx > 0 and lt < 0.15:                     # crossfade from previous
                prev = photo_seg(size, photos[idx - 1], 1.0, t_photo, labels[idx - 1])
                img = Image.blend(prev, img, ease(lt / 0.15))
            e = ease(seg(lt, 0.08, 0.5)) * (1 - ease(seg(lt, 0.88, 1.0)))
            if e < 1:
                lp = label_pill(size, labels[idx]).point(lambda v: int(v * e))
                img.alpha_composite(lp)
        else:
            img = cta.copy()
            e = ease(seg(t, t_intro + len(photos) * t_photo, dur - 0.2))
            img.alpha_composite(Image.new('RGBA', size, (5, 10, 6, int(255 * (1 - e)))))
        img.alpha_composite(foot)
        yield img
    return dur

# ================================================================ the 5 variants
VIDS = [
    dict(name='V1_residential',
         photos=[f'{SLR}/sl_02_spruce-christmas-lighting.jpg',
                 f'{SLR}/sl_10_ghting-installation-greenville-sc-1.jpg',
                 f'{SLR}/sl_13_ghting-installation-greenville-sc-4.jpg',
                 f'{SLR}/sl_09_nstallation-service-greenville-sc-3.jpg'],
         labels=['RESIDENTIAL', 'RESIDENTIAL', 'RESIDENTIAL', 'RESIDENTIAL'],
         line1='Your Home,', line2='Aglow All Season'),
    dict(name='V2_commercial',
         photos=[f'{SLR}/sl_04_nstallation-service-greenville-sc-2.jpg',
                 f'{SLR}/sl_17_hting-installation-municipalities-4.jpg',
                 f'{SLR}/sl_03_nstallation-service-greenville-sc-1.jpg'],
         labels=['COMMERCIAL', 'COMMERCIAL', 'COMMERCIAL'],
         line1='Commercial Displays', line2='That Draw Crowds'),
    dict(name='V3_municipal',
         photos=[f'{SLR}/sl_05_nstallation-service-greenville-sc-3.jpg',
                 f'{SLR}/sl_16_hting-installation-municipalities-3.jpg',
                 f'{SLR}/sl_18_olumbia-myrtle-beach-sc-ashevill-nc.jpg',
                 f'{SLR}/sl_06_nstallation-service-greenville-sc-4.jpg'],
         labels=['MUNICIPAL', 'MUNICIPAL', 'MUNICIPAL', 'MUNICIPAL'],
         line1='Town & City', line2='Trees That Stop Traffic'),
    dict(name='V4_crew',
         photos=[f'{SLR}/sl_01_spruce-christmas-lighting-2.jpg',
                 f'{SLR}/sl_14_hting-installation-municipalities-1.jpg',
                 f'{SLR}/sl_12_ghting-installation-greenville-sc-3.jpg',
                 f'{SLR}/sl_15_hting-installation-municipalities-2.jpg'],
         labels=['INSTALLED BY HAND', 'CUSTOM-FIT', 'COMMERCIAL-GRADE', 'BUILT TO LAST'],
         line1='Real Crews.', line2='Real Lights.'),
    dict(name='V5_showcase',
         photos=[f'{SLR}/sl_02_spruce-christmas-lighting.jpg',
                 f'{SLR}/sl_04_nstallation-service-greenville-sc-2.jpg',
                 f'{SLR}/sl_05_nstallation-service-greenville-sc-3.jpg',
                 f'{SLR}/sl_10_ghting-installation-greenville-sc-1.jpg',
                 f'{SLR}/sl_16_hting-installation-municipalities-3.jpg'],
         labels=['RESIDENTIAL', 'COMMERCIAL', 'MUNICIPAL', 'RESIDENTIAL', 'TOWNS & CITIES'],
         line1='One Call', line2='Does It All'),
]

if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'all'
    fmt = sys.argv[2] if len(sys.argv) > 2 else 'both'
    sizes = []
    if fmt in ('st', 'both'): sizes.append(('9x16', ST))
    if fmt in ('sq', 'both'): sizes.append(('1x1', SQ4))
    for v in VIDS:
        if which != 'all' and which != v['name']:
            continue
        for sname, size in sizes:
            gen = real_video(size, v['photos'], v['labels'], v['line1'], v['line2'])
            dur = 2.0 + len(v['photos']) * 2.6 + 2.6
            wav = f'/tmp/real_{v["name"]}_{sname}.wav'
            _AK.sl_track(wav, dur, seed=3, accents=[(0.9, 1046.5), (dur - 2.2, 1318.5)],
                         density=0.62, fade=1.4)
            out = f'{OUT}/SL_real_{v["name"]}_{sname}.mp4'
            encode(gen, size, out, audio_wav=wav, crf=22, chip_brand=SL)
            print('OK', out.split("/")[-1], f'{dur:.1f}s')
