"""Render Spruce Lights video set: logo sting, story promo, feed promo, before/after reel."""
import sys, math, os
sys.path.insert(0, '/home/user/spruce')
from vidkit import *
from templates import hero, review, before_after  # static fallbacks if needed

OUT = f'{ROOT}/videos/spruce_lights'
os.makedirs(OUT, exist_ok=True)
BG = f'{ROOT}/assets/bg'
ST, SQ = (1080, 1920), (1080, 1080)

LOGO_W = load_logo(SL, light_bg=False)          # winter-white wordmark, full color accents
LOGO_W = LOGO_W.crop(LOGO_W.getbbox())
LOGO_W.thumbnail((820, 900), Image.LANCZOS)

# ================================================================ 1. LOGO STING (5s)
def sting_frames(size=ST, dur=5.0):
    W, H = size
    n = int(dur * FPS)
    base = vgrad(size, TEAL, TEAL_D)
    glow = radial_glow(size, (W/2, H/2), W*0.75, CYAN, peak=60)
    base.alpha_composite(glow)
    sp = sparkle_field_layer(size, 12, n=16, ymax_frac=0.9)
    logo_y = H/2 - LOGO_W.height/2 - 30
    tag_f = F(40, 'Medium'); tag = "Holiday & Events"
    for i in range(n):
        t = i / FPS
        img = base.copy()
        draw_sparkle_field(img, sp, t)
        # sparkles pop in
        # logo: rises with overshoot + fades
        e = backout(seg(t, 0.5, 1.7))
        a = seg(t, 0.5, 1.2)
        lg = LOGO_W.copy()
        if a > 0:
            la = lg.getchannel('A').point(lambda v: int(v * a))
            lg.putalpha(la)
            if t > 1.2:  # sweep after arrival
                lg = sweep_logo(lg, t - 1.2, period=1.6)
            img.alpha_composite(lg, (int((W - lg.width)/2),
                                     int(logo_y + (1 - e) * 140)))
        # tagline + underline
        te = ease(seg(t, 2.3, 3.0))
        if te > 0:
            d = ImageDraw.Draw(img)
            ua = int(255 * ease(seg(t, 2.6, 3.3)))
            uw = int(360 * ease(seg(t, 2.6, 3.4)))
            d.line([(W/2 - uw/2, logo_y + LOGO_W.height + 44),
                    (W/2 + uw/2, logo_y + LOGO_W.height + 44)], fill=CYAN[:3] + (ua,), width=5)
            tl, _ = text_layer(size, tag, 'Medium', 40, color=(200, 222, 222, 255))
            alpha = tl.getchannel('A').point(lambda v: int(v * te))
            tl.putalpha(alpha)
            img.alpha_composite(tl, (0, int(46 * (1 - te))))
        # end sparkle burst
        if t > 3.4:
            ba = 1 - seg(t, 3.4, 4.0)
            d = ImageDraw.Draw(img)
            for k in range(10):
                ang = k / 10 * 2 * math.pi
                rr = 260 * ease(seg(t, 3.4, 4.3))
                sparkle(d, W/2 + math.cos(ang)*rr, H/2 + math.sin(ang)*rr*0.6,
                        16, (CYAN if k % 2 else LIME)[:3] + (int(200*ba),), ratio=.45, spread=.2)
        draw_sparkle_field(img, sp, t + 2.0, global_alpha=1.0)
        yield img

events = twinkle_events([0.7, 1.4, 2.3, 2.9, 3.5, 4.1])
chime_wav('/tmp/sl_sting.wav', events, 5.0)
encode(sting_frames(ST), ST, f'{OUT}/SL_logo_sting_reel.mp4', audio_wav='/tmp/sl_sting.wav')
print('✓ sting')

# ================================================================ 2. PROMO STORY (17s)
def promo_story():
    W, H = ST
    dur = 17.0; n = int(dur * FPS)
    foot = brand_footer_layer(ST, SL)
    # prebuild text layers
    t1, _ = text_layer(ST, "This December, your house could be the one they slow down for…", 'Bold', 64, maxw_frac=0.82)
    t2, _ = text_layer(ST, "…without touching a single ladder, strand or timer.", 'Bold', 60, maxw_frac=0.82)
    t3, _ = text_layer(ST, "Custom design • Pro install • Free season-long service • We store it all", 'Medium', 42, color=(214, 232, 232, 255), maxw_frac=0.8)
    t4, _ = text_layer(ST, "Now booking October — prime slots fill first", 'ExtraBold', 54, color=GOLD, maxw_frac=0.85)
    cta, _ = text_layer(ST, "Get My Free Quote", 'Bold', 46, color=TEAL_D, maxw_frac=1.0)
    sp = sparkle_field_layer(ST, 9, n=12, ymax_frac=0.35)
    for i in range(n):
        t = i / FPS
        # --- scene A: day house (0-4.2)
        if t < 4.2:
            img = kb_frame(f'{BG}/sl_day.jpg', ST, t / 4.2, z0=1.05, z1=1.18, brighten=0.96)
            img = slide_fade(img, t1, t, 0.6, 1.5, dy=70)
            img = slide_fade(img, t1, t, 3.5, 4.0, dy=-60)
        else:
            # --- scene B: night house (4.2-11)
            img = kb_frame(f'{BG}/sl_night.jpg', ST, (t - 4.2) / 6.8, z0=1.22, z1=1.06, pan=(0, -0.4))
            img = slide_fade(img, t2, t, 4.5, 5.4, dy=70)
            img = slide_fade(img, t2, t, 7.6, 8.1, dy=-60)
        # logo comes at 8.2
        if t >= 8.2:
            if img is not None and t < 8.35:
                img = kb_frame(f'{BG}/sl_night.jpg', ST, (t - 4.2) / 6.8, z0=1.22, z1=1.06, pan=(0, -0.4))
            ov = vgrad(ST, TEAL[:3] + (0,), TEAL[:3] + (235,))
            e = seg(t, 8.2, 9.0)
            img.alpha_composite(ov.point(lambda v: int(v * e)))
            lg = LOGO_W.copy(); la = lg.getchannel('A').point(lambda v: int(v * ease(e)))
            lg.putalpha(la); img.alpha_composite(lg, ((W - lg.width)//2, int(H*0.30 + (1-ease(e))*90)))
            if t > 9.0:
                img = slide_fade(img, t3, t, 9.0, 9.7, dy=50)
                img = slide_fade(img, t4, t, 10.2, 10.9, dy=50)
            if t > 11.2:
                # CTA pill
                e = ease(seg(t, 11.2, 11.8))
                d = ImageDraw.Draw(img)
                pw, ph = 620, 108
                cy = int(H * 0.72 + (1 - e) * 60)
                pill(d, [W/2 - pw/2, cy - ph/2, W/2 + pw/2, cy + ph/2], LIME)
                d.text((W/2, cy - 2), "Get My Free Quote", font=F(44, 'Bold'), fill=TEAL_D, anchor='mm')
            img.alpha_composite(foot)
            draw_sparkle_field(img, sp, t)
        # hard cut is fine; add quick white flash between A/B
        if 4.2 <= t < 4.35:
            fl = Image.new('RGBA', ST, (255, 255, 255, int(160 * (1 - (t-4.2)/0.15))))
            img.alpha_composite(fl)
        yield img

ev = twinkle_events([0.8, 4.4, 8.5, 9.2, 10.4, 11.4, 12.5], base=392)  # G major
ev += [(13.0, 784, 2.2, 0.5), (13.3, 987, 2.2, 0.4), (13.6, 1174, 2.6, 0.45)]
chime_wav('/tmp/sl_promo.wav', ev, 17.0)
encode(promo_story(), ST, f'{OUT}/SL_promo_reel.mp4', audio_wav='/tmp/sl_promo.wav')
print('✓ promo story')

# ================================================================ 3. PROMO FEED (12s, 1080x1080)
def promo_feed():
    W, H = SQ
    dur = 12.0; n = int(dur * FPS)
    foot = brand_footer_layer(SQ, SL)
    lgo = LOGO_W.copy(); lgo.thumbnail((560, 600), Image.LANCZOS)
    t1, _ = text_layer(SQ, "Untangled. Undimmed. Done for you.", 'Bold', 58, maxw_frac=0.86)
    t2, _ = text_layer(SQ, "Custom design • Pro install • Free season-long service", 'Medium', 38, color=(214, 232, 232, 255), maxw_frac=0.86, y_center=H*0.60)
    for i in range(n):
        t = i / FPS
        if t < 5.5:
            img = kb_frame(f'{BG}/sl_tree.jpg', SQ, t / 5.5, z0=1.06, z1=1.2)
            img = slide_fade(img, t1, t, 0.5, 1.3, dy=60)
            img = slide_fade(img, t1, t, 4.6, 5.1, dy=-60)
        else:
            img = kb_frame(f'{BG}/sl_roofline.jpg', SQ, (t - 5.5) / 6.5, z0=1.2, z1=1.05)
            e = seg(t, 5.5, 6.1)
            ov = vgrad(SQ, TEAL[:3] + (0,), TEAL[:3] + (240,))
            img.alpha_composite(ov.point(lambda v: int(v * e)))
            lg = lgo.copy(); la = lg.getchannel('A').point(lambda v: int(v * ease(e)))
            lg.putalpha(la); img.alpha_composite(lg, ((W - lg.width)//2, int(H*0.26 + (1-ease(e))*70)))
            if t > 6.2:
                img = slide_fade(img, t2, t, 6.2, 6.9, dy=40)
            if t > 7.4:
                e = ease(seg(t, 7.4, 8.0))
                d = ImageDraw.Draw(img)
                cy = int(H * 0.62 + (1 - e) * 50)
                pill(d, [W/2 - 290, cy - 52, W/2 + 290, cy + 52], LIME)
                d.text((W/2, cy - 2), "Get My Free Quote", font=F(42, 'Bold'), fill=TEAL_D, anchor='mm')
            img.alpha_composite(foot)
        if 5.5 <= t < 5.65:
            img.alpha_composite(Image.new('RGBA', SQ, (255, 255, 255, int(150 * (1 - (t-5.5)/0.15)))))
        yield img

ev = twinkle_events([0.6, 5.7, 6.5, 7.6, 9.0, 10.4], base=440)
chime_wav('/tmp/sl_feed.wav', ev, 12.0)
encode(promo_feed(), SQ, f'{OUT}/SL_promo_feed.mp4', audio_wav='/tmp/sl_feed.wav')
print('✓ promo feed')

# ================================================================ 4. BEFORE/AFTER REEL (8s)
def ba_reel():
    W, H = ST
    dur = 8.0; n = int(dur * FPS)
    foot = brand_footer_layer(ST, SL)
    A0 = bg_photo(f'{BG}/sl_day.jpg', W, H, focus=0.5, brighten=0.97)
    B0 = bg_photo(f'{BG}/sl_night.jpg', W, H, focus=0.5)
    def side_label(txt, color):
        lay = Image.new('RGBA', ST, (0,0,0,0))
        d = ImageDraw.Draw(lay)
        f = F(44, 'ExtraBold')
        d.text((txt[1], H*0.80), txt[0], font=f, fill=color, anchor='mm',
               stroke_width=2, stroke_fill=(0, 20, 26, 200))
        return lay
    lbl_a = side_label(("BEFORE", W*0.74), (215, 221, 221, 255))
    lbl_b = side_label(("AFTER ✨", W*0.26), CYAN)
    cap, _ = text_layer(ST, "The Spruce Difference", 'Bold', 52, maxw_frac=0.8)
    for i in range(n):
        t = i / FPS
        a = A0.copy(); b = B0.copy()
        # subtle opposite ken burns
        za = 1.05 + 0.06 * (t / dur); zb = 1.18 - 0.06 * (t / dur)
        a = a.resize((int(W*za), int(H*za)), Image.LANCZOS) if False else a
        x = W * (0.5 + 0.46 * math.sin((t / dur) * math.pi * 2 - math.pi/2))
        img = wipe(a.copy(), b.copy(), int(x))
        d = ImageDraw.Draw(img)
        d.line([(int(x), 0), (int(x), H)], fill=CREAM, width=6)
        # labels pinned
        if x < W*0.72: img.alpha_composite(lbl_a)
        if x > W*0.28: img.alpha_composite(lbl_b)
        img.alpha_composite(cap, (0, int(H*0.16)))
        d = ImageDraw.Draw(img)
        d.text((W/2, int(H*0.16 - 44)), "SLIDE INTO THE SEASON", font=F(28, 'Bold'), fill=LIME, anchor='mm')
        img.alpha_composite(foot)
        yield img

chime_wav('/tmp/sl_ba.wav', twinkle_events([0.4, 2.0, 4.0, 6.0, 7.4], base=523), 8.0)
encode(ba_reel(), ST, f'{OUT}/SL_before_after_reel.mp4', audio_wav='/tmp/sl_ba.wav')
print('✓ ba reel')
print('ALL SL VIDEOS DONE')
