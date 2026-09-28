"""Spruce Lights videos v2 — non-overlapping layout zones + twinkle soundtrack."""
import sys, math, os
sys.path.insert(0, '/home/user/spruce')
import spruce_kit as _K
_K.TEAL = (7, 34, 22, 255); _K.TEAL_D = (4, 22, 15, 255); _K.TEAL_L = (16, 60, 38, 255)
_K.SCRIM_COLOR = (2, 14, 9); _K.FOOT_DARK = (2, 18, 12); _K.CINE_SHADOW = (0.0, 0.06, 0.030)
import templates as _T
for _n in ('TEAL', 'TEAL_D', 'TEAL_L'):
    setattr(_T, _n, getattr(_K, _n))
from vidkit import *

OUT = f'{ROOT}/videos/spruce_lights'
os.makedirs(OUT, exist_ok=True)
BG = f'{ROOT}/assets/bg'
ST, SQ = (1080, 1920), (1080, 1080)

LOGO_W = load_logo(SL, light_bg=False).crop(load_logo(SL, light_bg=False).getbbox())
LOGO_W.thumbnail((820, 900), Image.LANCZOS)

# ================================================================ 1. STING (5s)
def sting_frames(size=ST, dur=5.0):
    W, H = size
    n = int(dur * FPS)
    base = vgrad(size, TEAL, TEAL_D)
    base.alpha_composite(radial_glow(size, (W/2, 800), W*0.72, CYAN, peak=55))
    sp = sparkle_field_layer(size, 12, n=16, ymax_frac=0.92)
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
            d.line([(W/2 - uw/2, uy), (W/2 + uw/2, uy)], fill=CYAN[:3] + (ua,), width=5)
            tl, _ = text_layer(size, "HOLIDAY & EVENTS", 'SemiBold', 38,
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
                        (CYAN if k % 2 else LIME)[:3] + (int(200*ba),), ratio=.45, spread=.2)
        draw_sparkle_field(img, sp, t + 2.0)
        yield img

chime = None
twinkle_wav('/tmp/sl_sting.wav', 5.0, key=523.25, seed=3,
            accents=[(1.7, 1046.5), (2.9, 784.0), (3.6, 1318.5)])
encode(sting_frames(ST), ST, f'{OUT}/SL_logo_sting_reel.mp4', audio_wav='/tmp/sl_sting.wav')
print('✓ sting')

# ================================================================ 2. PROMO STORY (17s)
def promo_story():
    W, H = ST
    dur = 17.0; n = int(dur * FPS)
    foot = brand_footer_layer(ST, SL)
    t1, _ = text_layer(ST, "This December, your house could be the one they slow down for…", 'Bold', 62, maxw_frac=0.82, y_center=1360)
    t2, _ = text_layer(ST, "…without touching a single ladder, strand or timer.", 'Bold', 58, maxw_frac=0.82, y_center=1360)
    t3, _ = text_layer(ST, "Custom design • Pro install • Free season-long service • We store it all", 'Medium', 40, color=(218, 234, 234, 255), maxw_frac=0.8, y_center=1060)
    t4, _ = text_layer(ST, "Now booking October — prime slots fill first", 'ExtraBold', 52, color=GOLD, maxw_frac=0.85, y_center=1190)
    sp = sparkle_field_layer(ST, 9, n=12, ymax_frac=0.30)
    for i in range(n):
        t = i / FPS
        if t < 4.2:
            img = kb_frame(f'{BG}/sl_day.jpg', ST, t / 4.2, z0=1.05, z1=1.18, brighten=0.96, grade=0.75)
            img = slide_fade(img, t1, t, 0.6, 1.5, dy=70, out=(3.5, 4.05, -60))
        else:
            img = kb_frame(f'{BG}/sl_night.jpg', ST, (t - 4.2) / 6.8, z0=1.22, z1=1.06, pan=(0, -0.4), grade=0.75)
            img = slide_fade(img, t2, t, 4.5, 5.4, dy=70, out=(7.6, 8.1, -60))
        if 4.2 <= t < 4.35:
            img.alpha_composite(Image.new('RGBA', ST, (255, 255, 255, int(150 * (1 - (t-4.2)/0.15)))))
        if t >= 8.2:
            ov = vgrad(ST, TEAL[:3] + (0,), TEAL[:3] + (225,))
            e = seg(t, 8.2, 9.0)
            img.alpha_composite(ov.point(lambda v: int(v * e)))
            lg = LOGO_W.copy(); la = lg.getchannel('A').point(lambda v: int(v * ease(e)))
            lg.putalpha(la); img.alpha_composite(lg, ((W - lg.width)//2, int(H*0.24 + (1-ease(e))*80)))
            img = slide_fade(img, t3, t, 9.0, 9.7, dy=50)
            img = slide_fade(img, t4, t, 10.2, 10.9, dy=50)
            if t > 11.2:
                d = ImageDraw.Draw(img)
                e = ease(seg(t, 11.2, 11.8))
                pw, ph = 620, 108
                cy = int(1430 + (1 - e) * 60)
                pill(d, [W/2 - pw/2, cy - ph/2, W/2 + pw/2, cy + ph/2], LIME)
                d.text((W/2, cy - 2), "Get My Free Quote", font=F(44, 'Bold'), fill=TEAL_D, anchor='mm')
            img.alpha_composite(foot)
            draw_sparkle_field(img, sp, t)
        yield img

twinkle_wav('/tmp/sl_promo.wav', 17.0, key=523.25, seed=11,
            accents=[(4.4, 659.3), (9.2, 1046.5), (11.5, 1318.5), (13.2, 1568.0)])
encode(promo_story(), ST, f'{OUT}/SL_promo_reel.mp4', audio_wav='/tmp/sl_promo.wav')
print('✓ promo story')

# ================================================================ 3. PROMO FEED (12s)
def promo_feed():
    W, H = SQ
    dur = 12.0; n = int(dur * FPS)
    foot = brand_footer_layer(SQ, SL)
    lgo = LOGO_W.copy(); lgo.thumbnail((520, 560), Image.LANCZOS)
    t1, _ = text_layer(SQ, "Untangled. Undimmed. Done for you.", 'Bold', 54, maxw_frac=0.86, y_center=560)
    t2, _ = text_layer(SQ, "Custom design • Pro install • Free season-long service", 'Medium', 36, color=(218, 234, 234, 255), maxw_frac=0.86, y_center=520)
    for i in range(n):
        t = i / FPS
        if t < 5.5:
            img = kb_frame(f'{BG}/sl_tree.jpg', SQ, t / 5.5, z0=1.06, z1=1.2, grade=0.7)
            img = slide_fade(img, t1, t, 0.5, 1.3, dy=60, out=(4.6, 5.1, -50))
        else:
            img = kb_frame(f'{BG}/sl_roofline.jpg', SQ, (t - 5.5) / 6.5, z0=1.2, z1=1.05, grade=0.7)
            e = seg(t, 5.5, 6.1)
            ov = vgrad(SQ, TEAL[:3] + (0,), TEAL[:3] + (225,))
            img.alpha_composite(ov.point(lambda v: int(v * e)))
            lg = lgo.copy(); la = lg.getchannel('A').point(lambda v: int(v * ease(e)))
            lg.putalpha(la); img.alpha_composite(lg, ((W - lg.width)//2, int(120 + (1-ease(e))*60)))
            img = slide_fade(img, t2, t, 6.2, 6.9, dy=40)
            if t > 7.4:
                d = ImageDraw.Draw(img)
                e = ease(seg(t, 7.4, 8.0))
                cy = int(710 + (1 - e) * 50)
                pill(d, [W/2 - 290, cy - 52, W/2 + 290, cy + 52], LIME)
                d.text((W/2, cy - 2), "Get My Free Quote", font=F(42, 'Bold'), fill=TEAL_D, anchor='mm')
            img.alpha_composite(foot)
        if 5.5 <= t < 5.65:
            img.alpha_composite(Image.new('RGBA', SQ, (255, 255, 255, int(140 * (1 - (t-5.5)/0.15)))))
        yield img

twinkle_wav('/tmp/sl_feed.wav', 12.0, key=587.33, seed=5,
            accents=[(5.7, 880.0), (7.6, 1174.7), (9.6, 1046.5)])
encode(promo_feed(), SQ, f'{OUT}/SL_promo_feed.mp4', audio_wav='/tmp/sl_feed.wav')
print('✓ promo feed')

# ================================================================ 4. BEFORE/AFTER REEL (8s)
def ba_reel():
    W, H = ST
    dur = 8.0; n = int(dur * FPS)
    foot = brand_footer_layer(ST, SL)
    A0 = bg_photo(f'{BG}/sl_day.jpg', W, H, focus=0.5, brighten=0.97)
    B0 = bg_photo(f'{BG}/sl_night.jpg', W, H, focus=0.5)
    def side_label(txt, cx, color):
        lay = Image.new('RGBA', ST, (0,0,0,0))
        d = ImageDraw.Draw(lay)
        d.text((cx, H*0.78), txt, font=F(44, 'ExtraBold'), fill=color, anchor='mm',
               stroke_width=2, stroke_fill=(0, 20, 26, 200))
        return lay
    lbl_a = side_label("BEFORE", W*0.74, (215, 221, 221, 255))
    lbl_b = side_label("AFTER ✨", W*0.26, CYAN)
    cap, _ = text_layer(ST, "The Spruce Difference", 'Bold', 50, maxw_frac=0.8, y_center=272)
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
        d.text((W/2, 172), "SLIDE INTO THE SEASON", font=F(28, 'Bold'), fill=LIME, anchor='mm',
               stroke_width=1, stroke_fill=(0, 20, 26, 150))
        img.alpha_composite(cap)
        img.alpha_composite(foot)
        yield img

twinkle_wav('/tmp/sl_ba.wav', 8.0, key=659.25, seed=8, accents=[(0.5, 1046.5), (4.0, 1318.5), (7.2, 1568.0)])
encode(ba_reel(), ST, f'{OUT}/SL_before_after_reel.mp4', audio_wav='/tmp/sl_ba.wav')
print('✓ ba reel')
print('ALL SL VIDEOS DONE (v2)')
