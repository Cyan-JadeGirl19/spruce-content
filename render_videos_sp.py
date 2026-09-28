"""Spruce Pro videos: logo sting, promo reel (15s), promo feed (11s), before/after reel (8s)."""
import sys, math, os
sys.path.insert(0, '/home/user/spruce')
from vidkit import *

OUT = f'{ROOT}/videos/spruce_pro'
os.makedirs(OUT, exist_ok=True)
P = f'{ROOT}/assets/photos/sp_real'
ST, SQ = (1080, 1920), (1080, 1080)

LOGO_W = load_logo(SP, light_bg=False)
LOGO_W = LOGO_W.crop(LOGO_W.getbbox())
LOGO_W.thumbnail((820, 900), Image.LANCZOS)

# ================================================================ 1. STING (5s)
def sting_frames(size=ST, dur=5.0):
    W, H = size
    n = int(dur * FPS)
    base = vgrad(size, TEAL, TEAL_D)
    base.alpha_composite(radial_glow(size, (W/2, H/2), W*0.75, LIME, peak=42))
    sp = sparkle_field_layer(size, 21, n=14, ymax_frac=0.9)
    logo_y = H/2 - LOGO_W.height/2 - 30
    for i in range(n):
        t = i / FPS
        img = base.copy()
        e = backout(seg(t, 0.5, 1.7))
        a = seg(t, 0.5, 1.2)
        lg = LOGO_W.copy()
        if a > 0:
            la = lg.getchannel('A').point(lambda v: int(v * a))
            lg.putalpha(la)
            if t > 1.2: lg = sweep_logo(lg, t - 1.2, period=1.6)
            img.alpha_composite(lg, (int((W - lg.width)/2), int(logo_y + (1 - e) * 140)))
        te = ease(seg(t, 2.3, 3.0))
        if te > 0:
            d = ImageDraw.Draw(img)
            ua = int(255 * ease(seg(t, 2.6, 3.3)))
            uw = int(360 * ease(seg(t, 2.6, 3.4)))
            d.line([(W/2 - uw/2, logo_y + LOGO_W.height + 44), (W/2 + uw/2, logo_y + LOGO_W.height + 44)],
                   fill=LIME[:3] + (ua,), width=5)
            tl, _ = text_layer(size, "Services & Solutions", 'Medium', 40, color=(200, 222, 222, 255))
            al = tl.getchannel('A').point(lambda v: int(v * te))
            tl.putalpha(al)
            img.alpha_composite(tl, (0, int(46 * (1 - te))))
        if t > 3.4:
            ba = 1 - seg(t, 3.4, 4.0)
            d = ImageDraw.Draw(img)
            for k in range(10):
                ang = k / 10 * 2 * math.pi
                rr = 260 * ease(seg(t, 3.4, 4.3))
                sparkle(d, W/2 + math.cos(ang)*rr, H/2 + math.sin(ang)*rr*0.6, 16,
                        (LIME if k % 2 else CYAN)[:3] + (int(200*ba),), ratio=.45, spread=.2)
        draw_sparkle_field(img, sp, t + 2.0)
        yield img

chime_wav('/tmp/sp_sting.wav', twinkle_events([0.7, 1.4, 2.3, 2.9, 3.5, 4.1], base=440), 5.0)
encode(sting_frames(ST), ST, f'{OUT}/SP_logo_sting_reel.mp4', audio_wav='/tmp/sp_sting.wav')
print('✓ sting')

# ================================================================ 2. PROMO REEL (15s)
def promo_reel():
    W, H = ST
    dur = 15.0; n = int(dur * FPS)
    foot = brand_footer_layer(ST, SP)
    scenes = [f'{P}/sp_pw_sq.jpg', f'{P}/house_wash_2026.jpg', f'{P}/sp_window_sq.jpg']
    t1, _ = text_layer(ST, "Greenville's home exterior has a glow-up season — and it's NOW.", 'Bold', 58, maxw_frac=0.8)
    t2, _ = text_layer(ST, "Driveways. Siding. Windows. Gutters.", 'Bold', 62, maxw_frac=0.82)
    t3, _ = text_layer(ST, "One trusted local crew. Licensed & insured. 5-star rated since 2006.", 'Medium', 42, color=(214, 232, 232, 255), maxw_frac=0.8)
    t4, _ = text_layer(ST, "Fall slots are filling fast", 'ExtraBold', 52, color=GOLD, maxw_frac=0.85)
    sp = sparkle_field_layer(ST, 4, n=10, ymax_frac=0.3)
    seq = [(0.0, 3.4), (3.4, 6.8), (6.8, 9.4)]
    for i in range(n):
        t = i / FPS
        if t < 9.4:
            idx = next(k for k, (a, b) in enumerate(seq) if a <= t < b)
            a, b = seq[idx]
            img = kb_frame(scenes[idx], ST, (t - a) / (b - a), z0=1.18, z1=1.05, brighten=0.98)
            if idx == 0:
                img = slide_fade(img, t1, t, 0.5, 1.3, dy=60)
                img = slide_fade(img, t1, t, 2.8, 3.3, dy=-50)
            elif idx == 1:
                img = slide_fade(img, t2, t, 3.7, 4.5, dy=60)
                img = slide_fade(img, t2, t, 6.2, 6.7, dy=-50)
            else:
                img = slide_fade(img, t2, t, 7.1, 7.9, dy=60)
                img = slide_fade(img, t2, t, 8.9, 9.35, dy=-50)
        else:
            img = kb_frame(f'{P}/sp6_stone_wash.jpg', ST, (t - 9.4) / 5.6, z0=1.05, z1=1.2)
            e = seg(t, 9.4, 10.1)
            ov = vgrad(ST, TEAL[:3] + (0,), TEAL[:3] + (238,))
            img.alpha_composite(ov.point(lambda v: int(v * e)))
            lg = LOGO_W.copy(); la = lg.getchannel('A').point(lambda v: int(v * ease(e)))
            lg.putalpha(la); img.alpha_composite(lg, ((W - lg.width)//2, int(H*0.27 + (1-ease(e))*90)))
            if t > 10.2: img = slide_fade(img, t3, t, 10.2, 10.9, dy=50)
            if t > 11.2: img = slide_fade(img, t4, t, 11.2, 11.9, dy=50)
            if t > 12.6:
                e = ease(seg(t, 12.6, 13.2))
                d = ImageDraw.Draw(img)
                pw, ph = 620, 108
                cy = int(H * 0.74 + (1 - e) * 60)
                pill(d, [W/2 - pw/2, cy - ph/2, W/2 + pw/2, cy + ph/2], LIME)
                d.text((W/2, cy - 2), "Get My Free Quote", font=F(44, 'Bold'), fill=TEAL_D, anchor='mm')
            img.alpha_composite(foot)
            draw_sparkle_field(img, sp, t)
        if any(abs(t - s) < 0.07 for s in (3.4, 6.8, 9.4)):
            img.alpha_composite(Image.new('RGBA', ST, (255, 255, 255, 120)))
        yield img

ev = twinkle_events([0.7, 3.6, 7.0, 9.6, 10.5, 11.5], base=392)
ev += [(12.8, 784, 2.0, 0.5), (13.1, 988, 2.2, 0.42)]
chime_wav('/tmp/sp_promo.wav', ev, 15.0)
encode(promo_reel(), ST, f'{OUT}/SP_promo_reel.mp4', audio_wav='/tmp/sp_promo.wav')
print('✓ promo reel')

# ================================================================ 3. PROMO FEED (11s)
def promo_feed():
    W, H = SQ
    dur = 11.0; n = int(dur * FPS)
    foot = brand_footer_layer(SQ, SP)
    lgo = LOGO_W.copy(); lgo.thumbnail((540, 580), Image.LANCZOS)
    t1, _ = text_layer(SQ, "Dirt, grime & algae don't stand a chance.", 'Bold', 54, maxw_frac=0.86)
    t2, _ = text_layer(SQ, "House wash • Windows • Gutters • Concrete", 'Medium', 36, color=(214, 232, 232, 255), maxw_frac=0.86, y_center=H*0.60)
    for i in range(n):
        t = i / FPS
        if t < 5.0:
            img = kb_frame(f'{P}/house_wash_2026.jpg', SQ, t / 5.0, z0=1.06, z1=1.2)
            img = slide_fade(img, t1, t, 0.5, 1.3, dy=60)
            img = slide_fade(img, t1, t, 4.2, 4.7, dy=-50)
        else:
            img = kb_frame(f'{P}/sp_pw_sq.jpg', SQ, (t - 5.0) / 6.0, z0=1.2, z1=1.05)
            e = seg(t, 5.0, 5.6)
            ov = vgrad(SQ, TEAL[:3] + (0,), TEAL[:3] + (240,))
            img.alpha_composite(ov.point(lambda v: int(v * e)))
            lg = lgo.copy(); la = lg.getchannel('A').point(lambda v: int(v * ease(e)))
            lg.putalpha(la); img.alpha_composite(lg, ((W - lg.width)//2, int(H*0.26 + (1-ease(e))*70)))
            if t > 5.8: img = slide_fade(img, t2, t, 5.8, 6.5, dy=40)
            if t > 7.2:
                e = ease(seg(t, 7.2, 7.8))
                d = ImageDraw.Draw(img)
                cy = int(H * 0.70 + (1 - e) * 50)
                pill(d, [W/2 - 280, cy - 50, W/2 + 280, cy + 50], LIME)
                d.text((W/2, cy - 2), "Get My Free Quote", font=F(40, 'Bold'), fill=TEAL_D, anchor='mm')
            img.alpha_composite(foot)
        if 5.0 <= t < 5.15:
            img.alpha_composite(Image.new('RGBA', SQ, (255, 255, 255, int(150 * (1 - (t-5.0)/0.15)))))
        yield img

chime_wav('/tmp/sp_feed.wav', twinkle_events([0.6, 5.2, 6.0, 7.4, 8.8], base=466), 11.0)
encode(promo_feed(), SQ, f'{OUT}/SP_promo_feed.mp4', audio_wav='/tmp/sp_feed.wav')
print('✓ promo feed')

# ================================================================ 4. BEFORE/AFTER REEL (8s)
def ba_reel():
    from render_sp import grime  # reuse
    W, H = ST
    dur = 8.0; n = int(dur * FPS)
    foot = brand_footer_layer(ST, SP)
    A0 = bg_photo(f'{P}/before_grime.jpg', W, H, focus=0.72, brighten=0.97)
    B0 = bg_photo(f'{P}/sp6_stone_wash.jpg', W, H, focus=0.72)
    def side_label(txt, cx, color):
        lay = Image.new('RGBA', ST, (0,0,0,0))
        d = ImageDraw.Draw(lay)
        d.text((cx, H*0.80), txt, font=F(44, 'ExtraBold'), fill=color, anchor='mm',
               stroke_width=2, stroke_fill=(0, 20, 26, 200))
        return lay
    lbl_a = side_label("BEFORE", W*0.74, (215, 221, 221, 255))
    lbl_b = side_label("AFTER ✨", W*0.26, CYAN)
    cap, _ = text_layer(ST, "One Afternoon. Total Renewal.", 'Bold', 52, maxw_frac=0.8, y_center=H*0.17)
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
        d.text((W/2, int(H*0.17 - 96)), "WATCH THIS", font=F(28, 'Bold'), fill=LIME, anchor='mm')
        img.alpha_composite(cap)
        img.alpha_composite(foot)
        yield img

chime_wav('/tmp/sp_ba.wav', twinkle_events([0.4, 2.0, 4.0, 6.0, 7.4], base=523), 8.0)
encode(ba_reel(), ST, f'{OUT}/SP_before_after_reel.mp4', audio_wav='/tmp/sp_ba.wav')
print('✓ ba reel')
print('ALL SP VIDEOS DONE')
