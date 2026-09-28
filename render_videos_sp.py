"""Spruce Pro videos v2 — non-overlapping layout zones + twinkle soundtrack."""
import sys, math, os
sys.path.insert(0, '/home/user/spruce')
import spruce_kit as _K
_K.TEAL = (0, 48, 60, 255); _K.TEAL_D = (0, 33, 42, 255); _K.TEAL_L = (10, 74, 88, 255)
_K.SCRIM_COLOR = (0, 20, 26); _K.FOOT_DARK = (0, 26, 33); _K.CINE_SHADOW = (0.00, 0.10, 0.13)
import templates as _T
for _n in ('TEAL', 'TEAL_D', 'TEAL_L'):
    setattr(_T, _n, getattr(_K, _n))
from vidkit import *

OUT = f'{ROOT}/videos/spruce_pro'
os.makedirs(OUT, exist_ok=True)
P = f'{ROOT}/assets/photos/sp_real2'
PP = f'{ROOT}/assets/photos/sp_real'
ST, SQ = (1080, 1920), (1080, 1080)

LOGO_W = load_logo(SP, light_bg=False).crop(load_logo(SP, light_bg=False).getbbox())
LOGO_W.thumbnail((820, 900), Image.LANCZOS)

# ================================================================ 1. STING (5s)
def sting_frames(size=ST, dur=5.0):
    W, H = size
    n = int(dur * FPS)
    base = vgrad(size, TEAL, TEAL_D)
    base.alpha_composite(radial_glow(size, (W/2, 800), W*0.72, LIME, peak=40))
    sp = sparkle_field_layer(size, 21, n=14, ymax_frac=0.92)
    lh = LOGO_W.height
    ly = 800 - lh // 2
    for i in range(n):
        t = i / FPS
        img = base.copy()
        e = backout(seg(t, 0.5, 1.7)); a = seg(t, 0.5, 1.2)
        lg = LOGO_W.copy()
        if a > 0:
            la = lg.getchannel('A').point(lambda v: int(v * a))
            lg.putalpha(la)
            if t > 1.2: lg = sweep_logo(lg, t - 1.2, period=1.6)
            img.alpha_composite(lg, (int((W - lg.width)/2), int(ly + (1 - e) * 140)))
        te = ease(seg(t, 2.4, 3.1))
        if te > 0:
            d = ImageDraw.Draw(img)
            uy = ly + lh + 70
            ua = int(255 * ease(seg(t, 2.6, 3.3)))
            uw = int(360 * ease(seg(t, 2.6, 3.4)))
            d.line([(W/2 - uw/2, uy), (W/2 + uw/2, uy)], fill=LIME[:3] + (ua,), width=5)
            tl, _ = text_layer(size, "SERVICES & SOLUTIONS", 'SemiBold', 38,
                               color=(205, 226, 226, 255), y_center=uy + 78)
            al = tl.getchannel('A').point(lambda v: int(v * te))
            tl.putalpha(al)
            img.alpha_composite(tl)
        if t > 3.4:
            ba = 1 - seg(t, 3.4, 4.0)
            d = ImageDraw.Draw(img)
            for k in range(10):
                ang = k / 10 * 2 * math.pi
                rr = 280 * ease(seg(t, 3.4, 4.3))
                sparkle(d, W/2 + math.cos(ang)*rr, 800 + math.sin(ang)*rr*0.6, 16,
                        (LIME if k % 2 else CYAN)[:3] + (int(200*ba),), ratio=.45, spread=.2)
        draw_sparkle_field(img, sp, t + 2.0)
        yield img

twinkle_wav('/tmp/sp_sting.wav', 5.0, key=466.16, seed=13,
            accents=[(1.7, 932.3), (2.9, 698.5), (3.6, 1174.7)])
encode(sting_frames(ST), ST, f'{OUT}/SP_logo_sting_reel.mp4', audio_wav='/tmp/sp_sting.wav')
print('✓ sting')

# ================================================================ 2. PROMO REEL (15s)
def promo_reel():
    W, H = ST
    dur = 15.0; n = int(dur * FPS)
    foot = brand_footer_layer(ST, SP)
    scenes = [f'{P}/sp_20_solutions-square-pressure-washing-2.jpg',
              f'{P}/sp_22_house-washing-greenville-sc.jpg',
              f'{P}/sp_21_-solutions-square-window-cleaning-2.jpg']
    t1, _ = text_layer(ST, "Greenville's home exterior has a glow-up season — and it's NOW.", 'Bold', 56, maxw_frac=0.8, y_center=1360)
    t2, _ = text_layer(ST, "Driveways. Siding. Windows. Gutters.", 'Bold', 60, maxw_frac=0.82, y_center=1360)
    t3, _ = text_layer(ST, "One trusted local crew. Licensed & insured. 5-star rated since 2006.", 'Medium', 40, color=(218, 234, 234, 255), maxw_frac=0.8, y_center=1080)
    t4, _ = text_layer(ST, "Fall slots are filling fast", 'ExtraBold', 50, color=GOLD, maxw_frac=0.85, y_center=1210)
    sp = sparkle_field_layer(ST, 4, n=10, ymax_frac=0.28)
    seq = [(0.0, 3.4), (3.4, 6.8), (6.8, 9.4)]
    for i in range(n):
        t = i / FPS
        if t < 9.4:
            idx = next(k for k, (a, b) in enumerate(seq) if a <= t < b)
            a, b = seq[idx]
            img = kb_frame(scenes[idx], ST, (t - a) / (b - a), z0=1.18, z1=1.05, brighten=0.98, grade=0.7)
            if idx == 0:
                img = slide_fade(img, t1, t, 0.5, 1.3, dy=60, out=(2.8, 3.3, -50))
            elif idx == 1:
                img = slide_fade(img, t2, t, 3.7, 4.5, dy=60, out=(6.2, 6.7, -50))
            else:
                img = slide_fade(img, t2, t, 7.1, 7.9, dy=60, out=(8.9, 9.35, -50))
        else:
            img = kb_frame(f'{P}/sp_07_Spruce6-1-1-scaled-1.jpg', ST, (t - 9.4) / 5.6, z0=1.05, z1=1.2, grade=0.7)
            e = seg(t, 9.4, 10.1)
            ov = vgrad(ST, TEAL[:3] + (0,), TEAL[:3] + (225,))
            img.alpha_composite(ov.point(lambda v: int(v * e)))
            lg = LOGO_W.copy(); la = lg.getchannel('A').point(lambda v: int(v * ease(e)))
            lg.putalpha(la); img.alpha_composite(lg, ((W - lg.width)//2, int(H*0.24 + (1-ease(e))*80)))
            img = slide_fade(img, t3, t, 10.2, 10.9, dy=50)
            img = slide_fade(img, t4, t, 11.2, 11.9, dy=50)
            if t > 12.6:
                d = ImageDraw.Draw(img)
                e = ease(seg(t, 12.6, 13.2))
                pw, ph = 620, 108
                cy = int(1440 + (1 - e) * 60)
                pill(d, [W/2 - pw/2, cy - ph/2, W/2 + pw/2, cy + ph/2], LIME)
                d.text((W/2, cy - 2), "Get My Free Quote", font=F(44, 'Bold'), fill=TEAL_D, anchor='mm')
            img.alpha_composite(foot)
            draw_sparkle_field(img, sp, t)
        if any(abs(t - s) < 0.07 for s in (3.4, 6.8, 9.4)):
            img.alpha_composite(Image.new('RGBA', ST, (255, 255, 255, 110)))
        yield img

twinkle_wav('/tmp/sp_promo.wav', 15.0, key=440.0, seed=17,
            accents=[(3.6, 659.3), (7.0, 880.0), (9.6, 1108.7), (11.4, 1318.5), (13.0, 1568.0)])
encode(promo_reel(), ST, f'{OUT}/SP_promo_reel.mp4', audio_wav='/tmp/sp_promo.wav')
print('✓ promo reel')

# ================================================================ 3. PROMO FEED (11s)
def promo_feed():
    W, H = SQ
    dur = 11.0; n = int(dur * FPS)
    foot = brand_footer_layer(SQ, SP)
    lgo = LOGO_W.copy(); lgo.thumbnail((520, 560), Image.LANCZOS)
    t1, _ = text_layer(SQ, "Dirt, grime & algae don't stand a chance.", 'Bold', 52, maxw_frac=0.86, y_center=560)
    t2, _ = text_layer(SQ, "House wash • Windows • Gutters • Concrete", 'Medium', 36, color=(218, 234, 234, 255), maxw_frac=0.86, y_center=520)
    for i in range(n):
        t = i / FPS
        if t < 5.0:
            img = kb_frame(f'{P}/sp_22_house-washing-greenville-sc.jpg', SQ, t / 5.0, z0=1.06, z1=1.2, grade=0.7)
            img = slide_fade(img, t1, t, 0.5, 1.3, dy=60, out=(4.2, 4.7, -50))
        else:
            img = kb_frame(f'{P}/sp_20_solutions-square-pressure-washing-2.jpg', SQ, (t - 5.0) / 6.0, z0=1.2, z1=1.05, grade=0.7)
            e = seg(t, 5.0, 5.6)
            ov = vgrad(SQ, TEAL[:3] + (0,), TEAL[:3] + (225,))
            img.alpha_composite(ov.point(lambda v: int(v * e)))
            lg = lgo.copy(); la = lg.getchannel('A').point(lambda v: int(v * ease(e)))
            lg.putalpha(la); img.alpha_composite(lg, ((W - lg.width)//2, int(120 + (1-ease(e))*60)))
            img = slide_fade(img, t2, t, 5.8, 6.5, dy=40)
            if t > 7.2:
                d = ImageDraw.Draw(img)
                e = ease(seg(t, 7.2, 7.8))
                cy = int(710 + (1 - e) * 50)
                pill(d, [W/2 - 280, cy - 50, W/2 + 280, cy + 50], LIME)
                d.text((W/2, cy - 2), "Get My Free Quote", font=F(40, 'Bold'), fill=TEAL_D, anchor='mm')
            img.alpha_composite(foot)
        if 5.0 <= t < 5.15:
            img.alpha_composite(Image.new('RGBA', SQ, (255, 255, 255, int(140 * (1 - (t-5.0)/0.15)))))
        yield img

twinkle_wav('/tmp/sp_feed.wav', 11.0, key=493.88, seed=19,
            accents=[(5.2, 784.0), (7.4, 1046.5), (9.2, 1174.7)])
encode(promo_feed(), SQ, f'{OUT}/SP_promo_feed.mp4', audio_wav='/tmp/sp_feed.wav')
print('✓ promo feed')

# ================================================================ 4. BEFORE/AFTER REEL (8s)
def ba_reel():
    W, H = ST
    dur = 8.0; n = int(dur * FPS)
    foot = brand_footer_layer(ST, SP)
    A0 = bg_photo(f'{PP}/before_grime.jpg', W, H, focus=0.72, brighten=0.97)
    B0 = bg_photo(f'{P}/sp_07_Spruce6-1-1-scaled-1.jpg', W, H, focus=0.72)
    def side_label(txt, cx, color):
        lay = Image.new('RGBA', ST, (0,0,0,0))
        d = ImageDraw.Draw(lay)
        d.text((cx, H*0.78), txt, font=F(44, 'ExtraBold'), fill=color, anchor='mm',
               stroke_width=2, stroke_fill=(0, 20, 26, 200))
        return lay
    lbl_a = side_label("BEFORE", W*0.74, (215, 221, 221, 255))
    lbl_b = side_label("AFTER ✨", W*0.26, CYAN)
    cap, _ = text_layer(ST, "One Afternoon. Total Renewal.", 'Bold', 50, maxw_frac=0.8, y_center=272)
    for i in range(n):
        t = i / FPS
        a = A0.copy(); b = B0.copy()
        x = W * (0.5 + 0.46 * math.sin((t / dur) * math.pi * 2 - math.pi/2))
        img = wipe(a.copy(), b.copy(), int(x))
        d = ImageDraw.Draw(img)
        d.line([(int(x), 0), (int(x), H)], fill=CREAM, width=6)
        if x < W*0.72: img.alpha_composite(lbl_a)
        if x > W*0.28: img.alpha_composite(lbl_b)
        d = ImageDraw.Draw(img)
        d.text((W/2, 172), "WATCH THIS", font=F(28, 'Bold'), fill=LIME, anchor='mm',
               stroke_width=1, stroke_fill=(0, 20, 26, 150))
        img.alpha_composite(cap)
        img.alpha_composite(foot)
        yield img

twinkle_wav('/tmp/sp_ba.wav', 8.0, key=587.33, seed=23, accents=[(0.5, 932.3), (4.0, 1174.7), (7.2, 1396.9)])
encode(ba_reel(), ST, f'{OUT}/SP_before_after_reel.mp4', audio_wav='/tmp/sp_ba.wav')
print('✓ ba reel')
print('ALL SP VIDEOS DONE (v2)')
