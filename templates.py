"""SPRUCE TEMPLATE LIBRARY v2 — every card is photo-backed under a teal mist,
with soft local scrims so type stays crisp. Feed (1080x1080) + Story (1080x1920)."""
from spruce_kit import *

SQ = (1080, 1080)
ST = (1080, 1920)

DEFAULT_BG = {
    'spruce_lights': f'{ROOT}/assets/bg/sl_macro.jpg',
    'spruce_pro':    f'{ROOT}/assets/photos/sp_real/sp_pw_sq.jpg',
}

def _bg(brand, size, bg_path, focus=0.5, blur=2.6, brighten=0.97, mist_kw=None, text_zone=None):
    """blend v3: graded photo -> frosted text zone -> light teal mist."""
    W, H = size
    p = bg_path or DEFAULT_BG[brand['key']]
    img = bg_photo(p, W, H, focus=focus, blur=blur, brighten=brighten, sat=1.05)
    if text_zone:
        zc, zh = text_zone[0], text_zone[1]
        img = frost(img, W/2, zc, W - 110, zh + 90, blur=9, darken=0.86, feather=46)
    img = cinema(img, strength=1.0)
    mk = dict(top=118, mid=52, bottom=196, focus_pt=0.46)
    if mist_kw: mk.update(mist_kw)
    if H > 1200: mk['focus_pt'] = min(0.52, mk['focus_pt'] + 0.03)
    img = mist(img, TEAL, **mk)
    return img

def _accent_arc(img, brand, side="bottom"):
    d = ImageDraw.Draw(img)
    w, h = img.size
    y = h - (196 if h > 1200 else 164)   # raised: comfortable gap above footer
    a1, a2 = (LIME, GOLD) if brand["key"] == "spruce_lights" else (CYAN, LIME)
    d.line([(0, y), (w * 0.42, y)], fill=a1, width=6)
    d.line([(w * 0.44, y), (w * 0.60, y)], fill=a2, width=6)
    return img

def _head_shadow(d, xy, text, font, fill=CREAM, anchor="mm"):
    d.text(xy, text, font=font, fill=fill, anchor=anchor,
           stroke_width=2, stroke_fill=(0, 24, 30, 130))

# ------------------------------------------------------------------ HERO
def hero(brand, size, bg_path, kicker, headline, sub=None, cta=True,
         focus=0.5, strand=False, brighten=1.0, badge=None):
    W, H = size
    img = bg_photo(bg_path, W, H, focus=focus, blur=1.4, brighten=brighten, sat=1.06)
    img = cinema(img, strength=0.9)
    # feathered frost behind the text stack + whisper of global scrim
    img = scrim(img, strength=0.42, top_frac=0.16 if H > 1200 else 0.12,
                bottom_frac=0.34 if H > 1200 else 0.4)
    img = place_logo_top(img, brand, light_bg=False)
    if strand:
        s = bulb_strand(W, 10, 46, bulb=26 if H > 1200 else 20, seed=11)
        img.alpha_composite(s, (0, 240 if H > 1200 else 190))
    img = sparkle_scatter(img, seed=5, n=4 if H > 1200 else 3)

    d = ImageDraw.Draw(img)
    maxw = W - 150
    cta_y = H - (330 if H > 1200 else 260) if cta else H - (170 if H > 1200 else 140)
    fk = F(30 if H > 1200 else 27, "Bold")
    hs = 92 if H > 1200 else 78
    while hs > 44:
        fh = F(hs, "ExtraBold")
        hlines = wrap_text(headline, fh, maxw, d)
        if len(hlines) <= (3 if H > 1200 else 2) and max(d.textlength(l, font=fh) for l in hlines) <= maxw:
            break
        hs -= 4
    fs = F(34 if H > 1200 else 30, "Medium")
    slines = wrap_text(sub, fs, maxw - 100, d)[:2] if sub else []
    stack_h = 0
    if kicker: stack_h += 54 + (16 if H > 1200 else 10)
    stack_h += len(hlines) * hs * 1.12
    if slines: stack_h += 20 + len(slines) * 46
    y = cta_y - 46 - stack_h
    # never let the stack climb into the strand/logo zone
    min_y = (352 if H > 1200 else 292) if strand else (240 if H > 1200 else 232)
    if y < min_y: y = min_y
    # frosted-glass zone behind the text stack (blur, not a dark wall)
    img = frost(img, W/2, y + stack_h/2, W - 96, stack_h + 64, blur=10, darken=0.84, feather=48)
    d = ImageDraw.Draw(img)
    if kicker:
        kw = d.textlength(kicker.upper(), font=fk)
        pill(d, [W/2 - kw/2 - 24, y - 26, W/2 + kw/2 + 24, y + 26], CYAN)
        d.text((W/2, y - 1), kicker.upper(), font=fk, fill=TEAL_D, anchor="mm")
        y += 54 + (16 if H > 1200 else 10)
    for ln in hlines:
        _head_shadow(d, (W/2, y), ln, fh)
        y += hs * 1.12
    if slines:
        y += 20
        for ln in slines:
            d.text((W/2, y), ln, font=fs, fill=(238, 244, 244, 255), anchor="mm",
                   stroke_width=1, stroke_fill=(0, 24, 30, 110))
            y += 46
    if cta:
        img = cta_pill(img, brand, cta_y)
    img = footer_bar(img, brand)
    if badge:
        d = ImageDraw.Draw(img)
        fb = F(26, "Bold")
        bw = d.textlength(badge, font=fb) + 56
        by0, by1 = (150, 208) if H > 1200 else (112, 168)
        pill(d, [W - bw - 30, by0, W - 30, by1], RED)
        d.text((W - 30 - bw/2, (by0 + by1)/2 - 2), badge, font=fb, fill=WHITE, anchor="mm")
    return img

# ------------------------------------------------------------------ REVIEW
def review(brand, size, quote, name, detail, bg_path=None):
    W, H = size
    tz = (H * 0.50, H * 0.38, 112) if H > 1200 else (H * 0.52, H * 0.32, 105)
    img = _bg(brand, size, bg_path, focus=0.42, blur=4, brighten=0.9, text_zone=tz)
    img = place_logo_top(img, brand, light_bg=False)
    d = ImageDraw.Draw(img)
    star_row(d, W/2, H * (0.335 if H > 1200 else 0.355), size=34 if H > 1200 else 27, gap=56)
    y = H * (0.42 if H > 1200 else 0.45)
    # house font (Poppins), bold — consistent with every other card
    qs = 54 if H > 1200 else 44
    while qs > 32:
        fq = F(qs, "Bold")
        lines = wrap_text("“" + quote + "”", fq, W - 200, d)
        if len(lines) <= (5 if H > 1200 else 4): break
        qs -= 2
    for ln in lines:
        d.text((W/2, y), ln, font=fq, fill=CREAM, anchor="mm",
               stroke_width=2, stroke_fill=(0, 24, 30, 150))
        y += qs * 1.34
    y += 34
    d.line([(W/2 - 64, y), (W/2 + 64, y)], fill=LIME, width=6)
    y += 40
    fn = F(42 if H > 1200 else 35, "ExtraBold")
    d.text((W/2, y), name, font=fn, fill=CYAN, anchor="mm",
           stroke_width=1, stroke_fill=(0, 24, 30, 130))
    fd = F(27 if H > 1200 else 23, "SemiBold")
    d.text((W/2, y + 56), detail, font=fd, fill=(228, 238, 238, 255), anchor="mm",
           stroke_width=1, stroke_fill=(0, 24, 30, 110))
    if H > 1200:
        s = bulb_strand(W, 8, 40, bulb=24, seed=4)
        img.alpha_composite(s, (0, H - 330))   # strand is the story accent — no arc
    img = footer_bar(img, brand)
    if H <= 1200:
        img = _accent_arc(img, brand)
    return img

# ------------------------------------------------------------------ STEPS
def steps(brand, size, kicker, title, items, bg_path=None):
    W, H = size
    img = _bg(brand, size, bg_path, focus=0.5, blur=3, brighten=0.9,
              mist_kw=dict(top=155, mid=95, bottom=220),
              text_zone=(H * 0.30, H * 0.14, 100))
    img = place_logo_top(img, brand, light_bg=False)
    d = ImageDraw.Draw(img)
    y = H * (0.245 if H > 1200 else 0.315)
    fk = F(27, "Bold"); d.text((W/2, y), kicker.upper(), font=fk, fill=LIME, anchor="mm",
                               stroke_width=1, stroke_fill=(0, 24, 30, 120)); y += 52
    ft = draw_fit(d, title, "Bold", W - 160, 66 if H > 1200 else 56, 40)
    for ln in wrap_text(title, ft, W - 160, d):
        _head_shadow(d, (W/2, y), ln, ft); y += ft.size * 1.18
    y += 40 if H > 1200 else 20
    gap = (H - y - (210 if H > 1200 else 170)) / len(items)
    for i, (t, s) in enumerate(items):
        bx0, bx1 = 90, W - 90
        bh = min(gap - 18, 150 if H > 1200 else 118)
        img = glass_round(img, [bx0, int(y), bx1, int(y + bh)], 26, fill_a=30,
                          outline=(255, 255, 255, 70), width=2)
        d = ImageDraw.Draw(img)
        cy = y + bh / 2
        r = 44 if H > 1200 else 36
        d.ellipse([bx0 + 34, cy - r, bx0 + 34 + 2*r, cy + r], fill=CYAN)
        d.text((bx0 + 34 + r, cy - 2), str(i + 1), font=F(r, "ExtraBold"), fill=TEAL_D, anchor="mm")
        d.text((bx0 + 34 + 2*r + 34, cy - (bh*0.20)), t, font=F(36 if H > 1200 else 30, "Bold"),
               fill=CREAM, anchor="lm", stroke_width=1, stroke_fill=(0, 24, 30, 110))
        d.text((bx0 + 34 + 2*r + 34, cy + (bh*0.20)), s, font=F(25 if H > 1200 else 21, "Regular"),
               fill=(228, 240, 240, 255), anchor="lm", stroke_width=1, stroke_fill=(0, 24, 30, 90))
        y += gap
    img = footer_bar(img, brand)
    return _accent_arc(img, brand)

# ------------------------------------------------------------------ BEFORE / AFTER
def before_after(brand, size, path_a, path_b, kicker, title, la="BEFORE", lb="AFTER", focus=0.55):
    W, H = size
    half = W // 2
    img = canvas(W, H, TEAL)
    top = int(H * (0.30 if H > 1200 else 0.26))
    a = bg_photo(path_a, half, H - top, focus=focus, brighten=0.94, sat=0.85)
    b = bg_photo(path_b, W - half, H - top, focus=focus, brighten=1.06, sat=1.08)
    img.paste(a, (0, top)); img.paste(b, (half, top))
    hdr = vgrad((W, top), TEAL, TEAL_D)
    img.alpha_composite(hdr, (0, 0))
    img = place_logo_top(img, brand, light_bg=False)
    d = ImageDraw.Draw(img)
    ft = draw_fit(d, title, "Bold", W - 140, 54 if H > 1200 else 46, 32)
    d.text((W/2, top - (118 if H > 1200 else 96)), title, font=ft, fill=CREAM, anchor="mm")
    d.text((W/2, top - (52 if H > 1200 else 42)), kicker.upper(), font=F(26, "Bold"), fill=LIME, anchor="mm")
    d.line([(half, top), (half, H)], fill=CREAM, width=8)
    fl = F(34, "ExtraBold")
    for cx, t, c in ((half//2, la, (165, 172, 172)), (half + half//2, lb, CYAN)):
        tw = d.textlength(t, font=fl)
        pill(d, [cx - tw/2 - 26, H - 250, cx + tw/2 + 26, H - 178], TEAL_D)
        d.text((cx, H - 216), t, font=fl, fill=c, anchor="mm")
    img = footer_bar(img, brand)
    return _accent_arc(img, brand)

# ------------------------------------------------------------------ POLL
def poll(brand, size, kicker, title, options, bg_path=None, note=None):
    W, H = size
    img = _bg(brand, size, bg_path, focus=0.5, blur=3, brighten=0.9,
              mist_kw=dict(top=150, mid=92, bottom=220),
              text_zone=(H * 0.36, H * 0.17, 108))
    img = place_logo_top(img, brand, light_bg=False)
    d = ImageDraw.Draw(img)
    y = H * (0.27 if H > 1200 else 0.31)
    d.text((W/2, y), kicker.upper(), font=F(27, "Bold"), fill=LIME, anchor="mm",
           stroke_width=1, stroke_fill=(0, 24, 30, 120)); y += 56
    ft = draw_fit(d, title, "ExtraBold", W - 140, 72 if H > 1200 else 58, 40)
    for ln in wrap_text(title, ft, W - 140, d):
        _head_shadow(d, (W/2, y), ln, ft); y += ft.size * 1.16
    y += 44 if H <= 1200 else 56
    n = len(options)
    if H <= 1200 and n >= 4:
        # 2x2 grid on square feed — bigger, cleaner tap targets
        gx, gy = 20, 20
        bw2 = (W - 220 - gx) // 2
        bh2 = 108
        for i, opt in enumerate(options):
            r_, c_ = divmod(i, 2)
            x0 = 110 + c_ * (bw2 + gx); y0 = y + r_ * (bh2 + gy)
            img = glass_round(img, [x0, y0, x0 + bw2, y0 + bh2], 26, fill_a=34,
                              outline=(CYAN if i % 2 == 0 else LIME), width=4)
            d = ImageDraw.Draw(img)
            fo = F(28, "Bold")
            lines = wrap_text(opt, fo, bw2 - 36, d)
            ty = y0 + bh2/2 - (len(lines)-1) * 17
            for ln in lines:
                d.text((x0 + bw2/2, ty), ln, font=fo, fill=CREAM, anchor="mm",
                       stroke_width=1, stroke_fill=(0, 24, 30, 110))
                ty += 34
        y += 2 * bh2 + gy
    else:
        avail = (H - (210 if H > 1200 else 170)) - y - (70 if note else 10)
        bh = min(132 if H > 1200 else 104, int((avail - (n - 1) * 24) / n))
        for i, opt in enumerate(options):
            x0, x1 = 110, W - 110
            img = glass_round(img, [x0, y, x1, y + bh], bh // 2, fill_a=34,
                              outline=(CYAN if i % 2 == 0 else LIME), width=4)
            d = ImageDraw.Draw(img)
            fo = F(min(40 if H > 1200 else 33, bh // 2 + 12), "Bold")
            d.text((W/2, y + bh/2 - 2), opt, font=fo, fill=CREAM, anchor="mm",
                   stroke_width=1, stroke_fill=(0, 24, 30, 110))
            y += bh + 24
    if note:
        d.text((W/2, y + 6), note, font=F(25, "Medium"), fill=(226, 238, 238, 255), anchor="mm",
               stroke_width=1, stroke_fill=(0, 24, 30, 110))
    img = footer_bar(img, brand)
    return _accent_arc(img, brand)

# ------------------------------------------------------------------ BIG STAT / URGENCY
def stat(brand, size, kicker, big, unit, sub, bg_path=None, cta=True, badge=None):
    W, H = size
    img = _bg(brand, size, bg_path, focus=0.45, blur=3, brighten=0.88,
              mist_kw=dict(top=150, mid=90, bottom=222),
              text_zone=(H * 0.50, H * 0.30, 110))
    img = place_logo_top(img, brand, light_bg=False)
    d = ImageDraw.Draw(img)
    y = H * (0.30 if H > 1200 else 0.33)
    d.text((W/2, y), kicker.upper(), font=F(28, "Bold"), fill=LIME, anchor="mm",
           stroke_width=1, stroke_fill=(0, 24, 30, 120))
    fb = F(230 if H > 1200 else 175, "ExtraBold")
    y = H * (0.44 if H > 1200 else 0.47)
    _head_shadow(d, (W/2, y), big, fb, fill=CYAN)
    d.text((W/2, y + (135 if H > 1200 else 105)), unit.upper(), font=F(44, "Bold"), fill=CREAM,
           anchor="mm", stroke_width=1, stroke_fill=(0, 24, 30, 110))
    y += (215 if H > 1200 else 175)
    fsu = F(33 if H > 1200 else 29, "Medium")
    for ln in wrap_text(sub, fsu, W - 220, d)[:3]:
        d.text((W/2, y), ln, font=fsu, fill=(234, 242, 242, 255), anchor="mm",
               stroke_width=1, stroke_fill=(0, 24, 30, 100)); y += 46
    if cta:
        img = cta_pill(img, brand, H - (330 if H > 1200 else 260))
    img = footer_bar(img, brand)
    if badge:
        d = ImageDraw.Draw(img)
        fbx = F(26, "Bold"); bw = d.textlength(badge, font=fbx) + 56
        by0, by1 = (150, 208) if H > 1200 else (112, 168)
        pill(d, [W - bw - 30, by0, W - 30, by1], RED)
        d.text((W - 30 - bw/2, (by0 + by1)/2 - 2), badge, font=fbx, fill=WHITE, anchor="mm")
    return _accent_arc(img, brand)

# ------------------------------------------------------------------ TIP / EDUCATION
def tip(brand, size, kicker, title, body=None, bg_path=None, icon="bulb", bullets=None):
    W, H = size
    img = _bg(brand, size, bg_path, focus=0.5, blur=3, brighten=0.88,
              mist_kw=dict(top=152, mid=94, bottom=222),
              text_zone=(H * 0.50, H * 0.44, 108))
    img = place_logo_top(img, brand, light_bg=False)
    d = ImageDraw.Draw(img)
    y = H * (0.255 if H > 1200 else 0.285)
    d.text((W/2, y), kicker.upper(), font=F(27, "Bold"), fill=LIME, anchor="mm",
           stroke_width=1, stroke_fill=(0, 24, 30, 120)); y += 58
    ft = draw_fit(d, title, "Bold", W - 150, 64 if H > 1200 else 54, 38)
    for ln in wrap_text(title, ft, W - 150, d):
        _head_shadow(d, (W/2, y), ln, ft); y += ft.size * 1.18
    y += 36
    if body:
        fbody = F(31 if H > 1200 else 27, "Medium")
        for ln in wrap_text(body, fbody, W - 240, d)[:3]:
            d.text((W/2, y), ln, font=fbody, fill=(236, 243, 243, 255), anchor="mm",
                   stroke_width=1, stroke_fill=(0, 24, 30, 100)); y += 45
        y += 40
    if bullets:
        n = len(bullets)
        avail = (H - (206 if H > 1200 else 172)) - y - 30
        bh = min(96 if H > 1200 else 76, int((avail - (n - 1) * 20) / n))
        for i, b in enumerate(bullets):
            img = glass_round(img, [140, int(y), W - 140, int(y + bh)], 20, fill_a=36,
                              outline=(255, 255, 255, 70), width=2)
            d = ImageDraw.Draw(img)
            r = bh * 0.30
            cx = 140 + bh * 0.62
            d.ellipse([cx - r, y + bh/2 - r, cx + r, y + bh/2 + r], fill=LIME)
            d.line([(cx - r*0.45, y + bh/2 + r*0.05), (cx - r*0.08, y + bh/2 + r*0.42),
                    (cx + r*0.5, y + bh/2 - r*0.4)], fill=TEAL_D, width=max(4, int(r*0.28)),
                   joint="curve")
            d.text((cx + bh*0.62, y + bh/2), b, font=F(31 if H > 1200 else 26, "SemiBold"),
                   fill=CREAM, anchor="lm", stroke_width=1, stroke_fill=(0, 24, 30, 110))
            y += bh + 20
    img = footer_bar(img, brand)
    return _accent_arc(img, brand)

# ------------------------------------------------------------------ SERVICE MENU
def services(brand, size, kicker, title, items, bg_path=None, cta=True):
    W, H = size
    img = _bg(brand, size, bg_path, focus=0.5, blur=3, brighten=0.88,
              mist_kw=dict(top=152, mid=94, bottom=224),
              text_zone=(H * 0.52, H * 0.34, 105))
    img = place_logo_top(img, brand, light_bg=False)
    d = ImageDraw.Draw(img)
    y = H * (0.26 if H > 1200 else 0.31)
    d.text((W/2, y), kicker.upper(), font=F(27, "Bold"), fill=LIME, anchor="mm",
           stroke_width=1, stroke_fill=(0, 24, 30, 120)); y += 52
    ft = draw_fit(d, title, "ExtraBold", W - 150, 64 if H > 1200 else 52, 38)
    _head_shadow(d, (W/2, y), title, ft); y += ft.size + 34
    rowh = (86 if H > 1200 else 74)
    for i, it in enumerate(items):
        img = glass_round(img, [150, y - 22, W - 150, y + 44], 33, fill_a=34,
                          outline=(255, 255, 255, 70), width=2)
        d = ImageDraw.Draw(img)
        sparkle(d, 196, y + 10, 16, CYAN if i % 2 else LIME, ratio=0.42, spread=0.18)
        d.text((232, y + 8), it, font=F(33 if H > 1200 else 28, "SemiBold"), fill=CREAM,
              anchor="lm", stroke_width=1, stroke_fill=(0, 24, 30, 100))
        y += rowh
    if cta:
        img = cta_pill(img, brand, H - (330 if H > 1200 else 250))
    img = footer_bar(img, brand)
    return _accent_arc(img, brand)

# ------------------------------------------------------------------ COUNTDOWN / DATE
def countdown(brand, size, kicker, datebig, sub, bg_path=None, badge=None):
    W, H = size
    img = _bg(brand, size, bg_path, focus=0.5, blur=3, brighten=0.88,
              mist_kw=dict(top=150, mid=90, bottom=222),
              text_zone=(H * 0.48, H * 0.26, 112))
    img = place_logo_top(img, brand, light_bg=False)
    d = ImageDraw.Draw(img)
    y = H * (0.32 if H > 1200 else 0.36)
    d.text((W/2, y), kicker.upper(), font=F(30, "Bold"), fill=LIME, anchor="mm",
           stroke_width=1, stroke_fill=(0, 24, 30, 120))
    fd = draw_fit(d, datebig, "ExtraBold", W - 140, 150 if H > 1200 else 116, 64)
    y += (150 if H > 1200 else 120)
    _head_shadow(d, (W/2, y), datebig, fd)
    y += fd.size * 0.95
    d.line([(W/2 - 90, y), (W/2 + 90, y)], fill=RED, width=8); y += 36
    fsu = F(34 if H > 1200 else 30, "SemiBold")
    for ln in wrap_text(sub, fsu, W - 200, d)[:3]:
        d.text((W/2, y), ln, font=fsu, fill=(234, 242, 242, 255), anchor="mm",
               stroke_width=1, stroke_fill=(0, 24, 30, 100)); y += 50
    img = cta_pill(img, brand, H - (330 if H > 1200 else 250))
    img = footer_bar(img, brand)
    if badge:
        d = ImageDraw.Draw(img)
        fbx = F(26, "Bold"); bw = d.textlength(badge, font=fbx) + 56
        by0, by1 = (150, 208) if H > 1200 else (112, 168)
        pill(d, [W - bw - 30, by0, W - 30, by1], RED)
        d.text((W - 30 - bw/2, (by0 + by1)/2 - 2), badge, font=fbx, fill=WHITE, anchor="mm")
    return _accent_arc(img, brand)

# ------------------------------------------------------------------ FINAL CTA
def cta_card(brand, size, headline, sub, bg_path=None, strand=True, phone_big=True):
    W, H = size
    img = _bg(brand, size, bg_path, focus=0.45, blur=3, brighten=0.9,
              mist_kw=dict(top=140, mid=86, bottom=220, focus_pt=0.34),
              text_zone=(H * 0.58, H * 0.34, 115))
    d = ImageDraw.Draw(img)
    if strand and brand["key"] == "spruce_lights":
        s = bulb_strand(W, 8, 44, bulb=24, seed=9)
        img.alpha_composite(s, (0, 20))
    import spruce_kit as _k
    _lh = 168          # SAME as every other card
    logo = load_logo(brand, light_bg=False, height=_lh)
    bbox = logo.getbbox(); logo = logo.crop(bbox)
    _ly = int(H * 0.285)
    _lx = (W - logo.width)//2
    img.alpha_composite(logo, (_lx, _ly))
    _k.LOGO_RECT = (_lx, _ly, _lx + logo.width, _ly + logo.height)
    from spruce_kit import BRAND_CHIP
    _clabel, _cbg, _cfg = BRAND_CHIP[brand["key"]]
    _cf = F(27, "ExtraBold")
    _cw = d.textlength(_clabel, font=_cf)
    pill(d, [56, 56, 56 + _cw + 52, 116], _cbg)
    d.text((56 + 26 + _cw / 2, 84), _clabel, font=_cf, fill=_cfg, anchor="mm")
    d = ImageDraw.Draw(img)
    y = _ly + logo.height + 70
    ft = draw_fit(d, headline, "ExtraBold", W - 150, 66 if H > 1200 else 56, 40)
    for ln in wrap_text(headline, ft, W - 150, d):
        _head_shadow(d, (W/2, y), ln, ft); y += ft.size * 1.18
    y += 26
    fs = F(32 if H > 1200 else 28, "Medium")
    for ln in wrap_text(sub, fs, W - 220, d)[:3]:
        d.text((W/2, y), ln, font=fs, fill=(232, 240, 240, 255), anchor="mm",
               stroke_width=1, stroke_fill=(0, 24, 30, 100)); y += 46
    if phone_big:
        fph = F(64 if H > 1200 else 52, "ExtraBold")
        y += 34
        _head_shadow(d, (W/2, y), brand["phone"], fph, fill=CYAN)
        y += fph.size + 4
        d.text((W/2, y), brand["site"], font=F(30, "SemiBold"), fill=LIME, anchor="mm",
               stroke_width=1, stroke_fill=(0, 24, 30, 110))
    img = footer_bar(img, brand)
    return _accent_arc(img, brand)
