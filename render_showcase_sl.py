"""Spruce Lights SHOWCASE videos — real installs: residential, commercial, municipal.
5 concepts x 2 formats (feed 1080x1080, story 1080x1920). H.264 + music-box score.
Safe zones: chip top-left, labels bottom-left, end card center, footer strip."""
import sys, os, math
sys.path.insert(0, '/home/user/spruce')
import spruce_kit as _K
_K.TEAL = (13, 27, 16, 255); _K.TEAL_D = (8, 18, 11, 255); _K.TEAL_L = (24, 44, 28, 255)
_K.SCRIM_COLOR = (2, 14, 8); _K.FOOT_DARK = (3, 20, 12); _K.CINE_SHADOW = (0.0, 0.05, 0.028)
from vidkit import *
import vidkit as _V
from spruce_kit import FONTS
import audio_kit as AK
from PIL import Image, ImageDraw, ImageFilter, ImageFont
import wave

OUT = f'{ROOT}/videos/spruce_lights/showcase'
SQ, ST = (1080, 1080), (1080, 1920)
os.makedirs(OUT, exist_ok=True)
SLR = f'{ROOT}/assets/photos/sl_real'
GOLD = (240, 176, 45, 255); CREAM = (246, 240, 226, 255); SAGE = (164, 178, 156, 255)

_SFC = {}
def SF(px, wght=800):
    k = (px, wght)
    if k not in _SFC:
        f = ImageFont.truetype(f'{FONTS}/PlayfairDisplay.ttf', px)
        try: f.set_variation_by_axes([wght])
        except Exception: pass
        _SFC[k] = f
    return _SFC[k]

def serif_layer(size, text, px, wght=800, color=CREAM, maxw_frac=0.84, lh=1.16, y_center=None):
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

def label_pill(size, text, y, x=70):
    """pine glass segment label, bottom-left area"""
    W, H = size
    layer = Image.new('RGBA', size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    f = F(34 if H > 1200 else 30, 'SemiBold')
    tw = d.textlength(text.upper(), font=f)
    ph = 66 if H > 1200 else 58
    ov = Image.new('RGBA', size, (0, 0, 0, 0))
    ImageDraw.Draw(ov).rounded_rectangle([x, y - ph // 2, x + tw + 92, y + ph // 2], ph // 2,
                                         fill=(13, 27, 16, 205), outline=(240, 176, 45, 150), width=2)
    layer.alpha_composite(ov)
    d = ImageDraw.Draw(layer)
    d.ellipse([x + 26, y - 6, x + 38, y + 6], fill=GOLD)
    d.text((x + 58, y - 1), text.upper(), font=f, fill=CREAM, anchor='lm')
    return layer

def end_card(size, title, dur_total):
    """frames for the closing serif title card"""
    W, H = size
    n = int(dur_total * FPS)
    base = vgrad(size, TEAL, TEAL_D)
    base.alpha_composite(radial_glow(size, (W / 2, H * 0.44), W * 0.66, (200, 150, 40), peak=42))
    t1, h1 = serif_layer(size, title, 62 if H > 1200 else 54, 800, CREAM, maxw_frac=0.84,
                         y_center=H * 0.42)
    t2, _ = serif_layer(size, "sprucelights.com", 36 if H > 1200 else 32, 700, GOLD,
                        maxw_frac=0.8, y_center=H * 0.42 + h1 / 2 + (86 if H > 1200 else 74))
    t3, _ = text_layer(size, "Free quotes  •  (864) 288-2459", 'SemiBold',
                       30 if H > 1200 else 27, color=(205, 215, 200, 255), y_center=H * 0.42 + h1 / 2 + (150 if H > 1200 else 128))
    sp = sparkle_field_layer(size, 8, n=14, ymax_frac=0.9)
    for i in range(n):
        t = i / FPS
        img = base.copy()
        e = ease(seg(t, 0.15, 0.8))
        if e > 0:
            for (lay, a0, a1) in ((t1, 0.1, 0.7), (t2, 0.4, 1.0), (t3, 0.55, 1.15)):
                a = ease(seg(t, a0, a1))
                if a > 0:
                    l2 = lay.getchannel('A').point(lambda v: int(v * a))
                    l3 = lay.copy(); l3.putalpha(l2)
                    img.alpha_composite(l3)
        draw_sparkle_field(img, sp, t + 1.0)
        yield img

def showcase(name, shots, title, seed):
    """shots = [(photo_path, label, dur)]"""
    if os.path.exists(f'{OUT}/{name}_feed.mp4') and os.path.exists(f'{OUT}/{name}_story.mp4'):
        print(f'  ↷ {name} already done, skipping')
        return
    for fmt, size in (('feed', SQ), ('story', ST)):
        W, H = size
        dur = sum(d for _, _, d in shots) + 2.4
        n = int(dur * FPS)
        foot = brand_footer_layer(size, SL)
        top_scrim = vgrad((W, H // 3), (2, 14, 8, 120), (2, 14, 8, 0))
        # pre-render label layers
        labels = []
        y_lab = int(H * (0.845 if H > 1200 else 0.875))
        for (p, lab, dseg) in shots:
            labels.append(label_pill(size, lab, y_lab))
        def frame_gen():
            t_acc = 0.0
            for si, (photo, lab, dseg) in enumerate(shots):
                z_in = si % 2 == 0
                for k in range(int(dseg * FPS)):
                    t = k / FPS
                    tt = k / max(1, int(dseg * FPS) - 1)
                    img = kb_frame(photo, size, tt, z0=1.06 if z_in else 1.20,
                                   z1=1.20 if z_in else 1.06,
                                   pan=((0, -0.3) if si % 3 == 1 else (0, 0.3) if si % 3 == 2 else (0, 0)),
                                   brighten=1.02, grade=0.72)
                    # top scrim so chip stays readable
                    img.alpha_composite(top_scrim, (0, 0))
                    # label slide-fade in
                    e = ease(seg(t, 0.25, 0.8))
                    o = 1 - ease(seg(t, dseg - 0.45, dseg - 0.1))
                    ea = e * o
                    if ea > 0:
                        lay = labels[si]
                        la = lay.getchannel('A').point(lambda v: int(v * ea))
                        l2 = lay.copy(); l2.putalpha(la)
                        dy = int((1 - e) * 40)
                        img.alpha_composite(l2, (0, dy))
                    # cut flash
                    if k < 4 and si > 0:
                        img.alpha_composite(Image.new('RGBA', size, (255, 255, 255, int(120 * (1 - k / 4)))))
                    img.alpha_composite(foot)
                    yield img
            yield from end_card(size, title, 2.4)
        # audio
        wav = f'/tmp/{name}_{fmt}.wav'
        accents = [(sum(d for _, _, d in shots) + 0.4, 1046.5),
                   (dur - 0.8, 1318.5)]
        AK.sl_track(wav, dur, seed=seed, accents=accents, density=AK.PRESETS['promo'], fade=1.2)
        encode(frame_gen(), size, f'{OUT}/{name}_{fmt}.mp4', chip_brand=SL, audio_wav=wav)
        print(f'  ✓ {name}_{fmt}')

# ---------------- the 5 concepts ----------------
print('1/5 residential')
showcase('SL_residential', [
    (f'{SLR}/sl_11_ghting-installation-greenville-sc-2.jpg', 'Residential', 1.9),
    (f'{SLR}/sl_08_nstallation-service-greenville-sc-2.jpg', 'Residential', 1.9),
    (f'{SLR}/sl_02_spruce-christmas-lighting.jpg', 'Residential', 1.9),
    (f'{SLR}/sl_10_ghting-installation-greenville-sc-1.jpg', 'Residential', 1.9),
], "Your Home, Aglow All Season", 101)

print('2/5 commercial')
showcase('SL_commercial', [
    (f'{SLR}/sl_17_hting-installation-municipalities-4.jpg', 'Commercial', 1.9),
    (f'{SLR}/sl_03_nstallation-service-greenville-sc-1.jpg', 'Commercial', 1.9),
    (f'{SLR}/sl_04_nstallation-service-greenville-sc-2.jpg', 'Commercial', 1.9),
    (f'{SLR}/sl_16_hting-installation-municipalities-3.jpg', 'Commercial', 1.9),
], "Lights That Stop Traffic", 102)

print('3/5 municipal')
showcase('SL_municipal', [
    (f'{SLR}/sl_05_nstallation-service-greenville-sc-3.jpg', 'Municipal', 2.2),
    (f'{SLR}/sl_06_nstallation-service-greenville-sc-4.jpg', 'Municipal', 2.2),
    (f'{SLR}/sl_18_olumbia-myrtle-beach-sc-ashevill-nc.jpg', 'Municipal', 2.2),
], "Whole-Town Twinkle", 103)

print('4/5 full showcase')
showcase('SL_showcase', [
    (f'{SLR}/sl_02_spruce-christmas-lighting.jpg', 'Residential', 1.9),
    (f'{SLR}/sl_16_hting-installation-municipalities-3.jpg', 'Commercial', 1.9),
    (f'{SLR}/sl_05_nstallation-service-greenville-sc-3.jpg', 'Municipal', 1.9),
    (f'{SLR}/sl_09_nstallation-service-greenville-sc-3.jpg', 'Residential', 1.9),
    (f'{SLR}/sl_18_olumbia-myrtle-beach-sc-ashevill-nc.jpg', 'Municipal', 1.9),
], "One Call Does It All", 104)

print('5/5 process to glow')
showcase('SL_process_glow', [
    (f'{SLR}/sl_12_ghting-installation-greenville-sc-3.jpg', 'We Prepare', 2.0),
    (f'{SLR}/sl_14_hting-installation-municipalities-1.jpg', 'We Install', 2.0),
    (f'{SLR}/sl_01_spruce-christmas-lighting-2.jpg', 'We Perfect', 2.0),
    (f'{SLR}/sl_13_ghting-installation-greenville-sc-4.jpg', 'You Enjoy', 2.0),
], "From Our Shop to Your Rooftop", 105)

print('ALL SHOWCASE VIDEOS DONE')
