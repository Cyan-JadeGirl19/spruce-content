"""SPRUCE LIGHTS templates — 'Holiday Card' edition:
deep pine canvas + soft warm-white paper panels with pine-green typography.
Spruce Pro keeps the teal glass system in templates.py."""
from spruce_kit import *

SQ = (1080, 1080)
ST = (1080, 1920)

PAPER  = (247, 243, 233, 255)   # soft warm white
PAPER2 = (255, 255, 255, 255)   # row white
INK    = (24, 44, 30, 255)      # pine ink
INK2   = (96, 106, 94, 255)     # muted body
PINE   = (31, 110, 58, 255)     # brand green (CTAs, numbers, name)
GOLDD  = (200, 168, 60, 255)    # gold divider

DEFAULT_BG = f'{ROOT}/assets/bg/sl_macro.jpg'

def _canvas_bg(size, bg_path, focus=0.5):
    W, H = size
    img = bg_photo(bg_path or DEFAULT_BG, W, H, focus=focus, blur=2.4, brighten=1.0, sat=1.05)
    img = cinema(img, strength=0.85)
    img = mist(img, TEAL, top=105, mid=46, bottom=170, focus_pt=0.44)
    return img

def _paper(img, box, r=44):
    sh = Image.new('RGBA', img.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([box[0] + 6, box[1] + 14, box[2] + 6, box[3] + 14], r, fill=(0, 0, 0, 110))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)))
    ov = Image.new('RGBA', img.size, (0, 0, 0, 0))
    ImageDraw.Draw(ov).rounded_rectangle(box, r, fill=PAPER)
    img.alpha_composite(ov)
    return img

def _paper_row(img, box, r=22):
    ov = Image.new('RGBA', img.size, (0, 0, 0, 0))
    ImageDraw.Draw(ov).rounded_rectangle(box, r, fill=PAPER2, outline=(20, 40, 25, 26), width=2)
    img.alpha_composite(ov)
    return img

def _cta_on_paper(img, cy, text="Get My Free Quote"):
    d = ImageDraw.Draw(img)
    f = F(41, "Bold")
    tw = d.textlength(text, font=f)
    pw = tw + 130
    sh = Image.new('RGBA', img.size, (0,0,0,0))
    ImageDraw.Draw(sh).rounded_rectangle([W_/2-pw/2+3, cy-44+7, W_/2+pw/2+3, cy+44+7], 44, fill=(20,60,35,90))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([W_/2-pw/2, cy-44, W_/2+pw/2, cy+44], 44, fill=PINE)
    d.text((W_/2, cy-2), text, font=f, fill=PAPER, anchor="mm")
    return img

W_ = 1080  # canvas width shorthand (all canvases are 1080 wide)

def _kicker_on_photo(img, y, text, color=LIME):
    d = ImageDraw.Draw(img)
    f = F(27, "Bold")
    d.text((W_/2, y), text.upper(), font=f, fill=color, anchor="mm",
           stroke_width=1, stroke_fill=(0, 24, 30, 140))
    return y + 52

def _title_on_photo(img, y, title, maxw=None, size=56):
    d = ImageDraw.Draw(img)
    maxw = maxw or (W_ - 150)
    ft = draw_fit(d, title, "Bold", maxw, size, 38)
    for ln in wrap_text(title, ft, maxw, d):
        d.text((W_/2, y), ln, font=ft, fill=CREAM, anchor="mm",
               stroke_width=2, stroke_fill=(0, 24, 30, 150))
        y += ft.size * 1.16
    return y

# ------------------------------------------------------------------ HERO
def hero(brand, size, bg_path, kicker, headline, sub=None, cta=True,
         focus=0.5, strand=False, brighten=1.0, badge=None):
    W, H = size
    img = bg_photo(bg_path, W, H, focus=focus, blur=1.4, brighten=brighten, sat=1.06)
    img = cinema(img, strength=0.8)
    img = scrim(img, strength=0.40, top_frac=0.16 if H > 1200 else 0.12,
                bottom_frac=0.30 if H > 1200 else 0.38)
    img = place_logo_top(img, brand, light_bg=False)
    if strand:
        s = bulb_strand(W, 10, 46, bulb=26 if H > 1200 else 20, seed=11)
        img.alpha_composite(s, (0, 240 if H > 1200 else 196))
    d = ImageDraw.Draw(img)
    # measure panel content
    hs = 92 if H > 1200 else 76
    while hs > 44:
        fh = F(hs, "ExtraBold")
        if max(d.textlength(l, font=fh) for l in wrap_text(headline, fh, W-260, d)) <= W-260 and \
           len(wrap_text(headline, fh, W-260, d)) <= (3 if H > 1200 else 2):
            break
        hs -= 4
    hlines = wrap_text(headline, fh, W-260, d)
    fs = F(31 if H > 1200 else 27, "Medium")
    slines = wrap_text(sub, fs, W-300, d)[:2] if sub else []
    ktop = (368 if H > 1200 else 300) if strand else (330 if H > 1200 else 272)
    panel_y0 = ktop + 10
    content = (66 if kicker else 0) + len(hlines) * hs * 1.14 \
            + ((18 + len(slines) * 44) if slines else 0) + (128 if cta else 40)
    panel_y1 = int(panel_y0 + 96 + content)
    px = 84 if H > 1200 else 96
    img = _paper(img, [px, panel_y0, W - px, panel_y1], 46)
    d = ImageDraw.Draw(img)
    y = panel_y0 + 52
    if kicker:
        kw = d.textlength(kicker.upper(), font=F(26, "Bold"))
        d.rounded_rectangle([W_/2-kw/2-24, y-24, W_/2+kw/2+24, y+24], 24, fill=PINE)
        d.text((W_/2, y-1), kicker.upper(), font=F(26, "Bold"), fill=PAPER, anchor="mm")
        y += 66
    for ln in hlines:
        d.text((W_/2, y), ln, font=fh, fill=INK, anchor="mm")
        y += hs * 1.14
    if slines:
        y += 18
        for ln in slines:
            d.text((W_/2, y), ln, font=fs, fill=INK2, anchor="mm")
            y += 44
    if cta:
        _cta_on_paper(img, panel_y1 - 84)
    img = footer_bar(img, brand)
    if badge:
        d = ImageDraw.Draw(img)
        fb = F(26, "Bold"); bw = d.textlength(badge, font=fb) + 56
        by0, by1 = (150, 208) if H > 1200 else (112, 168)
        pill(d, [W - bw - 30, by0, W - 30, by1], RED)
        d.text((W - 30 - bw/2, (by0+by1)/2 - 2), badge, font=fb, fill=WHITE, anchor="mm")
    return img

# ------------------------------------------------------------------ REVIEW
def review(brand, size, quote, name, detail, bg_path=None):
    W, H = size
    img = _canvas_bg(size, bg_path, focus=0.42)
    img = place_logo_top(img, brand, light_bg=False)
    d = ImageDraw.Draw(img)
    star_row(d, W/2, H * (0.315 if H > 1200 else 0.34), size=36 if H > 1200 else 28, gap=58)
    qs = 46 if H > 1200 else 40
    while qs > 30:
        fq = F(qs, "Bold")
        if len(wrap_text("“" + quote + "”", fq, W-280, d)) <= (5 if H > 1200 else 4): break
        qs -= 2
    qlines = wrap_text("“" + quote + "”", fq, W-280, d)
    panel_y0 = int(H * (0.375 if H > 1200 else 0.415))
    panel_y1 = int(panel_y0 + 120 + len(qlines) * qs * 1.32 + (150 if H > 1200 else 120))
    px = 84 if H > 1200 else 96
    img = _paper(img, [px, panel_y0, W - px, panel_y1], 46)
    d = ImageDraw.Draw(img)
    y = panel_y0 + 62
    for ln in qlines:
        d.text((W/2, y), ln, font=fq, fill=INK, anchor="mm")
        y += qs * 1.32
    y += 26
    d.line([(W/2 - 64, y), (W/2 + 64, y)], fill=GOLDD, width=6)
    y += 40
    d.text((W/2, y), name, font=F(42 if H > 1200 else 35, "ExtraBold"), fill=PINE, anchor="mm")
    d.text((W/2, y + 56), detail, font=F(27 if H > 1200 else 23, "SemiBold"), fill=INK2, anchor="mm")
    if H > 1200:
        s = bulb_strand(W, 8, 40, bulb=24, seed=4)
        img.alpha_composite(s, (0, H - 330))
    img = footer_bar(img, brand)
    if H <= 1200:
        img = _accent_arc(img, brand)
    return img

# ------------------------------------------------------------------ STEPS
def steps(brand, size, kicker, title, items, bg_path=None):
    W, H = size
    img = _canvas_bg(size, bg_path)
    img = place_logo_top(img, brand, light_bg=False)
    y = H * (0.245 if H > 1200 else 0.30)
    y = _kicker_on_photo(img, y, kicker)
    y = _title_on_photo(img, y + 4, title)
    y += 34
    n = len(items)
    bottom = H - (216 if H > 1200 else 178)
    px = 84 if H > 1200 else 96
    img = _paper(img, [px, int(y), W - px, bottom], 46)
    d = ImageDraw.Draw(img)
    row_h = (bottom - y - 56) / n
    ry = y + 28
    for i, (t, s) in enumerate(items):
        cy = ry + row_h / 2
        r = 34 if H > 1200 else 28
        d.ellipse([px + 46, cy - r, px + 46 + 2*r, cy + r], fill=PINE)
        d.text((px + 46 + r, cy - 2), str(i + 1), font=F(r, "ExtraBold"), fill=PAPER, anchor="mm")
        d.text((px + 46 + 2*r + 30, cy - row_h*0.20), t, font=F(35 if H > 1200 else 29, "Bold"), fill=INK, anchor="lm")
        d.text((px + 46 + 2*r + 30, cy + row_h*0.20), s, font=F(24 if H > 1200 else 20, "Regular"), fill=INK2, anchor="lm")
        ry += row_h
    img = footer_bar(img, brand)
    return _accent_arc(img, brand)

# ------------------------------------------------------------------ POLL
def poll(brand, size, kicker, title, options, bg_path=None, note=None):
    W, H = size
    img = _canvas_bg(size, bg_path)
    img = place_logo_top(img, brand, light_bg=False)
    y = H * (0.265 if H > 1200 else 0.30)
    y = _kicker_on_photo(img, y, kicker)
    y = _title_on_photo(img, y + 4, title, size=64 if H > 1200 else 54)
    y += 36
    bottom = H - (216 if H > 1200 else 178)
    px = 84 if H > 1200 else 96
    img = _paper(img, [px, int(y), W - px, bottom], 46)
    d = ImageDraw.Draw(img)
    n = len(options)
    row_h = (bottom - y - (110 if note else 56)) / n
    ry = y + 28
    for i, opt in enumerate(options):
        x0, x1 = px + 40, W - px - 40
        img = _paper_row(img, [x0, ry, x1, ry + row_h - 14], (row_h - 14) // 2)
        d = ImageDraw.Draw(img)
        fo = F(min(38 if H > 1200 else 32, int((row_h - 14) / 2.4)), "Bold")
        d.text((W/2, ry + (row_h - 14)/2 - 2), opt, font=fo, fill=INK, anchor="mm")
        ry += row_h
    if note:
        d = ImageDraw.Draw(img)
        d.text((W/2, bottom - 44), note, font=F(25, "SemiBold"), fill=INK2, anchor="mm")
    img = footer_bar(img, brand)
    return _accent_arc(img, brand)

# ------------------------------------------------------------------ STAT
def stat(brand, size, kicker, big, unit, sub, bg_path=None, cta=True, badge=None):
    W, H = size
    img = _canvas_bg(size, bg_path, focus=0.45)
    img = place_logo_top(img, brand, light_bg=False)
    y = H * (0.295 if H > 1200 else 0.33)
    y = _kicker_on_photo(img, y, kicker)
    panel_y0 = int(y + 20)
    big_sz  = 190 if H > 1200 else 128
    panel_y1 = int(panel_y0 + (620 if H > 1200 else 442))
    px = 84 if H > 1200 else 96
    img = _paper(img, [px, panel_y0, W - px, panel_y1], 46)
    d = ImageDraw.Draw(img)
    yy = panel_y0 + (112 if H > 1200 else 84)
    d.text((W/2, yy), big, font=F(big_sz, "ExtraBold"), fill=PINE, anchor="mm")
    d.text((W/2, yy + (128 if H > 1200 else 92)), unit.upper(), font=F(42, "Bold"), fill=INK, anchor="mm")
    yy += (196 if H > 1200 else 150)
    d.line([(W/2 - 70, yy), (W/2 + 70, yy)], fill=GOLDD, width=5)
    yy += (36 if H > 1200 else 28)
    fsu = F(29 if H > 1200 else 26, "Medium")
    for ln in wrap_text(sub, fsu, W - 2*(px+60), d)[:(3 if H > 1200 else 2)]:
        d.text((W/2, yy), ln, font=fsu, fill=INK2, anchor="mm"); yy += 42
    if cta:
        _cta_on_paper(img, panel_y1 - 82)
    img = footer_bar(img, brand)
    if badge:
        d = ImageDraw.Draw(img)
        fbx = F(26, "Bold"); bw = d.textlength(badge, font=fbx) + 56
        by0, by1 = (150, 208) if H > 1200 else (112, 168)
        pill(d, [W - bw - 30, by0, W - 30, by1], RED)
        d.text((W - 30 - bw/2, (by0+by1)/2 - 2), badge, font=fbx, fill=WHITE, anchor="mm")
    return _accent_arc(img, brand)

# ------------------------------------------------------------------ TIP
def tip(brand, size, kicker, title, body=None, bg_path=None, icon="bulb", bullets=None):
    W, H = size
    img = _canvas_bg(size, bg_path)
    img = place_logo_top(img, brand, light_bg=False)
    y = H * (0.245 if H > 1200 else 0.285)
    y = _kicker_on_photo(img, y, kicker)
    y = _title_on_photo(img, y + 4, title)
    y += 30
    bottom = H - (216 if H > 1200 else 178)
    px = 84 if H > 1200 else 96
    img = _paper(img, [px, int(y), W - px, bottom], 46)
    d = ImageDraw.Draw(img)
    ry = y + 40
    if body:
        fb = F(29 if H > 1200 else 26, "Medium")
        for ln in wrap_text(body, fb, W - 2*(px+60), d)[:2]:
            d.text((W/2, ry), ln, font=fb, fill=INK, anchor="mm"); ry += 44
        ry += 22
    if bullets:
        n = len(bullets)
        avail = (bottom - 40) - ry
        bh = min(84 if H > 1200 else 66, int((avail - (n - 1) * 16) / n))
        for i, b in enumerate(bullets):
            x0, x1 = px + 44, W - px - 44
            img = _paper_row(img, [x0, ry, x1, ry + bh], 18)
            d = ImageDraw.Draw(img)
            r = bh * 0.30
            cx = x0 + bh * 0.62
            d.ellipse([cx - r, ry + bh/2 - r, cx + r, ry + bh/2 + r], fill=PINE)
            d.line([(cx - r*0.45, ry + bh/2 + r*0.05), (cx - r*0.08, ry + bh/2 + r*0.42),
                    (cx + r*0.5, ry + bh/2 - r*0.4)], fill=PAPER, width=max(4, int(r*0.3)), joint="curve")
            d.text((cx + bh*0.62, ry + bh/2), b, font=F(29 if H > 1200 else 24, "SemiBold"),
                   fill=INK, anchor="lm")
            ry += bh + 16
    img = footer_bar(img, brand)
    return _accent_arc(img, brand)

# ------------------------------------------------------------------ SERVICES
def services(brand, size, kicker, title, items, bg_path=None, cta=True):
    W, H = size
    img = _canvas_bg(size, bg_path)
    img = place_logo_top(img, brand, light_bg=False)
    y = H * (0.245 if H > 1200 else 0.295)
    y = _kicker_on_photo(img, y, kicker)
    y = _title_on_photo(img, y + 4, title)
    y += 30
    bottom = H - (330 if H > 1200 else 262) if cta else H - (216 if H > 1200 else 178)
    px = 84 if H > 1200 else 96
    img = _paper(img, [px, int(y), W - px, int(bottom)], 46)
    d = ImageDraw.Draw(img)
    n = len(items)
    row_h = (bottom - y - (150 if cta else 48)) / n
    ry = y + 24
    for i, it in enumerate(items):
        x0, x1 = px + 40, W - px - 40
        img = _paper_row(img, [x0, ry, x1, ry + row_h - 12], (row_h - 12) // 2)
        d = ImageDraw.Draw(img)
        sparkle(d, x0 + 52, ry + (row_h - 12)/2, 15, PINE, ratio=0.42, spread=0.18)
        d.text((x0 + 92, ry + (row_h - 12)/2), it, font=F(31 if H > 1200 else 26, "SemiBold"),
               fill=INK, anchor="lm")
        ry += row_h
    if cta:
        _cta_on_paper(img, int(bottom) - 74)
    img = footer_bar(img, brand)
    return _accent_arc(img, brand)

# ------------------------------------------------------------------ COUNTDOWN
def countdown(brand, size, kicker, datebig, sub, bg_path=None, badge=None):
    W, H = size
    img = _canvas_bg(size, bg_path)
    img = place_logo_top(img, brand, light_bg=False)
    y = H * (0.315 if H > 1200 else 0.355)
    y = _kicker_on_photo(img, y, kicker)
    panel_y0 = int(y + 22)
    panel_y1 = int(panel_y0 + (560 if H > 1200 else 500))
    px = 84 if H > 1200 else 96
    img = _paper(img, [px, panel_y0, W - px, panel_y1], 46)
    d = ImageDraw.Draw(img)
    fd = draw_fit(d, datebig, "ExtraBold", W - 2*(px+50), 148 if H > 1200 else 118, 64)
    yy = panel_y0 + (130 if H > 1200 else 110)
    d.text((W/2, yy), datebig, font=fd, fill=PINE, anchor="mm")
    yy += fd.size * 0.98
    d.line([(W/2 - 80, yy), (W/2 + 80, yy)], fill=RED, width=7)
    yy += 40
    fsu = F(29 if H > 1200 else 26, "SemiBold")
    for ln in wrap_text(sub, fsu, W - 2*(px+50), d)[:3]:
        d.text((W/2, yy), ln, font=fsu, fill=INK2, anchor="mm"); yy += 42
    _cta_on_paper(img, panel_y1 - 84)
    img = footer_bar(img, brand)
    if badge:
        d = ImageDraw.Draw(img)
        fbx = F(26, "Bold"); bw = d.textlength(badge, font=fbx) + 56
        by0, by1 = (150, 208) if H > 1200 else (112, 168)
        pill(d, [W - bw - 30, by0, W - 30, by1], RED)
        d.text((W - 30 - bw/2, (by0+by1)/2 - 2), badge, font=fbx, fill=WHITE, anchor="mm")
    return _accent_arc(img, brand)

# ------------------------------------------------------------------ FINAL CTA
def cta_card(brand, size, headline, sub, bg_path=None, strand=True, phone_big=True):
    W, H = size
    img = _canvas_bg(size, bg_path, focus=0.45)
    d = ImageDraw.Draw(img)
    if strand:
        s = bulb_strand(W, 8, 44, bulb=24, seed=9)
        img.alpha_composite(s, (0, 20))
    img = place_logo_top(img, brand, light_bg=False)
    panel_y0 = int(H * (0.40 if H > 1200 else 0.44))
    panel_y1 = int(panel_y0 + (700 if H > 1200 else 560))
    px = 84 if H > 1200 else 96
    img = _paper(img, [px, panel_y0, W - px, panel_y1], 46)
    d = ImageDraw.Draw(img)
    ft = draw_fit(d, headline, "ExtraBold", W - 2*(px+40), 62 if H > 1200 else 54, 40)
    yy = panel_y0 + (86 if H > 1200 else 70)
    for ln in wrap_text(headline, ft, W - 2*(px+40), d):
        d.text((W/2, yy), ln, font=ft, fill=INK, anchor="mm"); yy += ft.size * 1.18
    yy += 22
    fs = F(29 if H > 1200 else 26, "Medium")
    for ln in wrap_text(sub, fs, W - 2*(px+60), d)[:2]:
        d.text((W/2, yy), ln, font=fs, fill=INK2, anchor="mm"); yy += 42
    if phone_big:
        fph = F(58 if H > 1200 else 46, "ExtraBold")
        yy += 26
        d.text((W/2, yy), brand["phone"], font=fph, fill=PINE, anchor="mm")
        yy += fph.size + 8
        d.text((W/2, yy), brand["site"], font=F(28, "SemiBold"), fill=GOLDD, anchor="mm")
    img = footer_bar(img, brand)
    return _accent_arc(img, brand)

# ------------------------------------------------------------------ BEFORE / AFTER (photo composition stays dark)
def before_after(brand, size, path_a, path_b, kicker, title, la="BEFORE", lb="AFTER", focus=0.55):
    from templates import before_after as _ba
    return _ba(brand, size, path_a, path_b, kicker, title, la, lb, focus)

def _accent_arc(img, brand, side="bottom"):
    d = ImageDraw.Draw(img)
    w, h = img.size
    y = h - (196 if h > 1200 else 164)
    d.line([(0, y), (w * 0.42, y)], fill=LIME, width=6)
    d.line([(w * 0.44, y), (w * 0.60, y)], fill=GOLDD, width=6)
    return img
