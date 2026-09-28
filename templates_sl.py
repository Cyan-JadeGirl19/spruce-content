"""SPRUCE LIGHTS templates — 'Website Edition' v3:
matches sprucelights.com exactly — dark pine surfaces, cream PLAYFAIR SERIF
headlines with gold highlight phrases, gold CTAs, sage body text.
Photo-first: cards sit in the lower third, photography owns the frame.
Spruce Pro keeps the teal glass system in templates.py."""
from spruce_kit import *

SQ = (1080, 1080)
ST = (1080, 1920)

# ---- website palette (sampled from sprucelights.com hero) ----
CARD   = (16, 29, 19, 246)      # dark pine card surface
ROW    = (26, 44, 30, 255)      # row surface (slightly lifted pine)
CREAM  = (246, 240, 226, 255)   # headline text
SAGE   = (164, 178, 156, 255)   # body / secondary text
GOLD   = (240, 176, 45, 255)    # site gold — CTAs, numbers, highlights
DK     = (13, 25, 15, 255)      # dark pine (text on gold)
GOLDD  = GOLD                   # legacy divider name

# legacy names kept so audits/renders keep working
PAPER  = CARD
PAPER2 = ROW
INK    = CREAM
INK2   = SAGE
PINE   = GOLD

DEFAULT_BG = f'{ROOT}/assets/bg/sl_macro.jpg'

# ---- serif system (Playfair Display, variable weight) ----
_SF_CACHE = {}
def SF(size, wght=700):
    key = (size, wght)
    if key not in _SF_CACHE:
        f = ImageFont.truetype(f"{FONTS}/PlayfairDisplay.ttf", size)
        try: f.set_variation_by_axes([wght])
        except Exception: pass
        _SF_CACHE[key] = f
    return _SF_CACHE[key]

def _parse_gold(t):
    segs, cur, gold = [], '', False
    for ch in t:
        if ch == '*':
            if cur: segs.append((cur, gold)); cur = ''
            gold = not gold
        else:
            cur += ch
    if cur: segs.append((cur, gold))
    return [s for s in segs if s[0]]

def _serif_fit(d, text, maxw, size, min_size, wght=700, maxlines=3):
    plain = text.replace('*', '')
    s = size
    while s > min_size:
        f = SF(s, wght)
        lines = wrap_text(plain, f, maxw, d)
        if max(d.textlength(l, font=f) for l in lines) <= maxw and len(lines) <= maxlines:
            return s
        s -= 3
    return min_size

def _rich_center(d, cx, y, text, size, maxw, wght=700, lh=1.16,
                 base=CREAM, hi=GOLD, stroke=0):
    """Word-wrapped centered serif line; *starred* words render in gold."""
    f = SF(size, wght)
    words = []
    for s, gld in _parse_gold(text):
        for w in s.split(' '):
            if w: words.append((w, gld))
    sp = d.textlength(' ', font=f)
    lines, cur, curw = [], [], 0
    for w, gld in words:
        ww = d.textlength(w, font=f)
        add = ww if not cur else ww + sp
        if cur and curw + add > maxw:
            lines.append(cur); cur, curw = [(w, gld)], ww
        else:
            cur.append((w, gld)); curw += add
    if cur: lines.append(cur)
    for ln in lines:
        widths = [d.textlength(w, font=f) for w, _ in ln]
        x = cx - (sum(widths) + sp * (len(ln) - 1)) / 2
        for (w, gld), ww in zip(ln, widths):
            d.text((x, y), w, font=f, fill=(hi if gld else base), anchor="lm",
                   stroke_width=stroke, stroke_fill=(0, 22, 12, 170) if stroke else None)
            x += ww + sp
        y += size * lh
    return y

def _nlines(text, size, maxw, d, wght=700):
    f = SF(size, wght)
    words = [(w, g) for s, g in _parse_gold(text) for w in s.split(' ') if w]
    sp = d.textlength(' ', font=f)
    lines, curw, has = 1, 0, False
    for w, _ in words:
        ww = d.textlength(w, font=f)
        add = ww if not has else ww + sp
        if has and curw + add > maxw:
            lines += 1; curw = ww
        else:
            curw += add; has = True
    return lines

# ---- surfaces ----
def _canvas_bg(size, bg_path, focus=0.5):
    W, H = size
    img = bg_photo(bg_path or DEFAULT_BG, W, H, focus=focus, blur=2.4, brighten=1.0, sat=1.05)
    img = cinema(img, strength=0.85)
    img = mist(img, TEAL, top=105, mid=46, bottom=170, focus_pt=0.44)
    return img

def _paper(img, box, r=42):
    sh = Image.new('RGBA', img.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).rounded_rectangle([box[0] + 6, box[1] + 14, box[2] + 6, box[3] + 14], r, fill=(0, 0, 0, 130))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(18)))
    ov = Image.new('RGBA', img.size, (0, 0, 0, 0))
    dd = ImageDraw.Draw(ov)
    dd.rounded_rectangle(box, r, fill=CARD)
    dd.rounded_rectangle(box, r, outline=(240, 176, 45, 95), width=3)   # gold hairline
    img.alpha_composite(ov)
    return img

def _paper_row(img, box, r=20):
    ov = Image.new('RGBA', img.size, (0, 0, 0, 0))
    dd = ImageDraw.Draw(ov)
    dd.rounded_rectangle(box, r, fill=ROW)
    dd.rounded_rectangle(box, r, outline=(240, 176, 45, 55), width=2)
    img.alpha_composite(ov)
    return img

def _cta_on_paper(img, cy, text="Get My Free Quote"):
    d = ImageDraw.Draw(img)
    f = F(37, "Bold")
    tw = d.textlength(text, font=f)
    pw = tw + 116
    sh = Image.new('RGBA', img.size, (0,0,0,0))
    ImageDraw.Draw(sh).rounded_rectangle([W_/2-pw/2+3, cy-40+7, W_/2+pw/2+3, cy+40+7], 40, fill=(0,0,0,120))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([W_/2-pw/2, cy-40, W_/2+pw/2, cy+40], 40, fill=GOLD)
    d.text((W_/2, cy-2), text, font=f, fill=DK, anchor="mm")
    return img

W_ = 1080

def _px(H):  return 130 if H > 1200 else 140
def _ww(H):  return W_ - 2*_px(H) - 80

def _kicker_on_photo(img, y, text, color=GOLD):
    """Website-style badge: dark pill, gold hairline, gold dot + gold caps."""
    d = ImageDraw.Draw(img)
    f = F(25, "SemiBold")
    tw = d.textlength(text.upper(), font=f)
    x0, x1 = W_/2 - tw/2 - 56, W_/2 + tw/2 + 34
    ov = Image.new('RGBA', img.size, (0,0,0,0))
    do = ImageDraw.Draw(ov)
    do.rounded_rectangle([x0, y-27, x1, y+27], 27, fill=(13, 25, 15, 215),
                         outline=(240, 176, 45, 160), width=2)
    img.alpha_composite(ov)
    d = ImageDraw.Draw(img)
    d.ellipse([x0+26, y-6, x0+38, y+6], fill=GOLD)
    d.text((x0+56, y-1), text.upper(), font=f, fill=GOLD, anchor="lm")
    return y + 54

def _title_on_photo(img, y, title, maxw=None, size=58):
    d = ImageDraw.Draw(img)
    maxw = maxw or (W_ - 150)
    s = _serif_fit(d, title, maxw, size, 36)
    return _rich_center(d, W_/2, y + s*0.55, title, s, maxw, stroke=2) + s*0.12

# ------------------------------------------------------------------ HERO
def hero(brand, size, bg_path, kicker, headline, sub=None, cta=True,
         focus=0.5, strand=False, brighten=1.0, badge=None):
    W, H = size
    img = bg_photo(bg_path, W, H, focus=focus, blur=1.4, brighten=brighten, sat=1.06)
    img = cinema(img, strength=0.8)
    img = scrim(img, strength=0.40, top_frac=0.16 if H > 1200 else 0.12,
                bottom_frac=0.34 if H > 1200 else 0.42)
    img = place_logo_top(img, brand, light_bg=False)
    if strand:
        s = bulb_strand(W, 10, 46, bulb=26 if H > 1200 else 20, seed=11)
        img.alpha_composite(s, (0, 240 if H > 1200 else 196))
    d = ImageDraw.Draw(img)
    px, ww = _px(H), _ww(H)
    hs = 78 if H > 1200 else 62
    hs = _serif_fit(d, headline, ww, hs, 40, wght=760, maxlines=3 if H > 1200 else 2)
    nl = _nlines(headline, hs, ww, d, wght=760)
    fs = F(27 if H > 1200 else 24, "Medium")
    slines = wrap_text(sub, fs, ww - 30, d)[:2] if sub else []
    ktop = (560 if H > 1200 else 440) if strand else (520 if H > 1200 else 408)
    panel_y0 = ktop + 8
    content = (58 if kicker else 0) + nl * hs * 1.16 \
            + ((16 + len(slines) * 40) if slines else 0) + (112 if cta else 36)
    panel_y1 = int(panel_y0 + 84 + content)
    img = _paper(img, [px, panel_y0, W - px, panel_y1], 42)
    d = ImageDraw.Draw(img)
    y = panel_y0 + 46
    if kicker:
        f = F(23, "SemiBold")
        kw = d.textlength(kicker.upper(), font=f)
        kx0, kx1 = W_/2 - kw/2 - 52, W_/2 + kw/2 + 32
        ov = Image.new('RGBA', img.size, (0,0,0,0))
        ImageDraw.Draw(ov).rounded_rectangle([kx0, y-24, kx1, y+24], 24,
            fill=(13, 25, 15, 235), outline=(240, 176, 45, 170), width=2)
        img.alpha_composite(ov)
        d = ImageDraw.Draw(img)
        d.ellipse([kx0+24, y-5, kx0+34, y+5], fill=GOLD)
        d.text((kx0+52, y-1), kicker.upper(), font=f, fill=GOLD, anchor="lm")
        y += 58
    y = _rich_center(d, W_/2, y + hs*0.55, headline, hs, ww, wght=760)
    if slines:
        y += 12
        for ln in slines:
            d.text((W_/2, y), ln, font=fs, fill=SAGE, anchor="mm")
            y += 40
    if cta:
        _cta_on_paper(img, panel_y1 - 76)
    img = footer_bar(img, brand)
    if badge:
        d = ImageDraw.Draw(img)
        fb = F(25, "Bold"); bw = d.textlength(badge, font=fb) + 52
        by0, by1 = (150, 206) if H > 1200 else (112, 166)
        pill(d, [W - bw - 30, by0, W - 30, by1], GOLD)
        d.text((W - 30 - bw/2, (by0+by1)/2 - 2), badge, font=fb, fill=DK, anchor="mm")
    return img

# ------------------------------------------------------------------ REVIEW
def review(brand, size, quote, name, detail, bg_path=None):
    W, H = size
    img = _canvas_bg(size, bg_path, focus=0.42)
    img = place_logo_top(img, brand, light_bg=False)
    d = ImageDraw.Draw(img)
    px, ww = _px(H), _ww(H)
    star_row(d, W/2, H * (0.36 if H > 1200 else 0.40), size=34 if H > 1200 else 27, gap=54)
    qs = 42 if H > 1200 else 36
    while qs > 28:
        fq = F(qs, "Bold")
        if len(wrap_text("“" + quote + "”", fq, ww, d)) <= (5 if H > 1200 else 4): break
        qs -= 2
    qlines = wrap_text("“" + quote + "”", fq, ww, d)
    panel_y0 = int(H * (0.425 if H > 1200 else 0.465))
    panel_y1 = int(panel_y0 + 96 + len(qlines) * qs * 1.30 + (118 if H > 1200 else 100))
    img = _paper(img, [px, panel_y0, W - px, panel_y1], 42)
    d = ImageDraw.Draw(img)
    y = panel_y0 + 50
    for ln in qlines:
        d.text((W/2, y), ln, font=fq, fill=CREAM, anchor="mm")
        y += qs * 1.30
    y += 22
    d.line([(W/2 - 56, y), (W/2 + 56, y)], fill=GOLD, width=5)
    y += 34
    d.text((W/2, y), name, font=F(38 if H > 1200 else 32, "ExtraBold"), fill=GOLD, anchor="mm")
    d.text((W/2, y + (52 if H > 1200 else 44)), detail, font=F(25 if H > 1200 else 21, "SemiBold"), fill=SAGE, anchor="mm")
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
    px, ww = _px(H), _ww(H)
    y = H * (0.245 if H > 1200 else 0.30)
    y = _kicker_on_photo(img, y, kicker)
    y = _title_on_photo(img, y + 4, title, maxw=W - 280)
    y += 30
    n = len(items)
    bottom = H - (216 if H > 1200 else 178)
    img = _paper(img, [px, int(y), W - px, bottom], 42)
    d = ImageDraw.Draw(img)
    row_h = (bottom - y - 48) / n
    ry = y + 24
    for i, (t, s) in enumerate(items):
        cy = ry + row_h / 2
        r = 30 if H > 1200 else 26
        d.ellipse([px + 42, cy - r, px + 42 + 2*r, cy + r], fill=GOLD)
        d.text((px + 42 + r, cy - 2), str(i + 1), font=F(r, "ExtraBold"), fill=DK, anchor="mm")
        d.text((px + 42 + 2*r + 26, cy - row_h*0.20), t, font=F(32 if H > 1200 else 27, "Bold"), fill=CREAM, anchor="lm")
        d.text((px + 42 + 2*r + 26, cy + row_h*0.20), s, font=F(22 if H > 1200 else 19, "Regular"), fill=SAGE, anchor="lm")
        ry += row_h
    img = footer_bar(img, brand)
    return _accent_arc(img, brand)

# ------------------------------------------------------------------ POLL
def poll(brand, size, kicker, title, options, bg_path=None, note=None):
    W, H = size
    img = _canvas_bg(size, bg_path)
    img = place_logo_top(img, brand, light_bg=False)
    px, ww = _px(H), _ww(H)
    y = H * (0.265 if H > 1200 else 0.315)
    y = _kicker_on_photo(img, y, kicker)
    y = _title_on_photo(img, y + 4, title, maxw=W - 280, size=62 if H > 1200 else 52)
    y += 32
    bottom = H - (216 if H > 1200 else 178)
    img = _paper(img, [px, int(y), W - px, bottom], 42)
    d = ImageDraw.Draw(img)
    n = len(options)
    row_h = (bottom - y - (104 if note else 48)) / n
    ry = y + 24
    for i, opt in enumerate(options):
        x0, x1 = px + 36, W - px - 36
        img = _paper_row(img, [x0, ry, x1, ry + row_h - 12], (row_h - 12) // 2)
        d = ImageDraw.Draw(img)
        fo = F(min(36 if H > 1200 else 30, int((row_h - 12) / 2.4)), "Bold")
        d.text((W/2, ry + (row_h - 12)/2 - 2), opt, font=fo, fill=CREAM, anchor="mm")
        ry += row_h
    if note:
        d = ImageDraw.Draw(img)
        d.text((W/2, bottom - 42), note, font=F(24, "SemiBold"), fill=SAGE, anchor="mm")
    img = footer_bar(img, brand)
    return _accent_arc(img, brand)

# ------------------------------------------------------------------ STAT
def stat(brand, size, kicker, big, unit, sub, bg_path=None, cta=True, badge=None):
    W, H = size
    img = _canvas_bg(size, bg_path, focus=0.45)
    img = place_logo_top(img, brand, light_bg=False)
    px, ww = _px(H), _ww(H)
    y = H * (0.375 if H > 1200 else 0.415)
    y = _kicker_on_photo(img, y, kicker)
    panel_y0 = int(y + 18)
    big_sz  = 150 if H > 1200 else 116
    panel_y1 = int(panel_y0 + (520 if H > 1200 else 402))
    img = _paper(img, [px, panel_y0, W - px, panel_y1], 42)
    d = ImageDraw.Draw(img)
    yy = panel_y0 + (92 if H > 1200 else 72)
    d.text((W/2, yy), big, font=SF(big_sz, 800), fill=GOLD, anchor="mm")
    d.text((W/2, yy + (104 if H > 1200 else 80)), unit.upper(), font=F(38, "Bold"), fill=CREAM, anchor="mm")
    yy += (172 if H > 1200 else 134)
    d.line([(W/2 - 62, yy), (W/2 + 62, yy)], fill=GOLD, width=5)
    yy += (32 if H > 1200 else 26)
    fsu = F(27 if H > 1200 else 24, "Medium")
    for ln in wrap_text(sub, fsu, ww, d)[:2]:
        d.text((W/2, yy), ln, font=fsu, fill=SAGE, anchor="mm"); yy += 40
    if cta:
        _cta_on_paper(img, panel_y1 - 74)
    img = footer_bar(img, brand)
    if badge:
        d = ImageDraw.Draw(img)
        fbx = F(25, "Bold"); bw = d.textlength(badge, font=fbx) + 52
        by0, by1 = (150, 206) if H > 1200 else (112, 166)
        pill(d, [W - bw - 30, by0, W - 30, by1], GOLD)
        d.text((W - 30 - bw/2, (by0+by1)/2 - 2), badge, font=fbx, fill=DK, anchor="mm")
    return _accent_arc(img, brand)

# ------------------------------------------------------------------ TIP
def tip(brand, size, kicker, title, body=None, bg_path=None, icon="bulb", bullets=None):
    W, H = size
    img = _canvas_bg(size, bg_path)
    img = place_logo_top(img, brand, light_bg=False)
    px, ww = _px(H), _ww(H)
    y = H * (0.245 if H > 1200 else 0.295)
    y = _kicker_on_photo(img, y, kicker)
    y = _title_on_photo(img, y + 4, title, maxw=W - 280)
    y += 28
    bottom = H - (216 if H > 1200 else 178)
    img = _paper(img, [px, int(y), W - px, bottom], 42)
    d = ImageDraw.Draw(img)
    ry = y + 34
    if body:
        fb = F(27 if H > 1200 else 24, "Medium")
        for ln in wrap_text(body, fb, ww, d)[:2]:
            d.text((W/2, ry), ln, font=fb, fill=CREAM, anchor="mm"); ry += 40
        ry += 18
    if bullets:
        n = len(bullets)
        avail = (bottom - 36) - ry
        bh = min(76 if H > 1200 else 62, int((avail - (n - 1) * 14) / n))
        for i, b in enumerate(bullets):
            x0, x1 = px + 40, W - px - 40
            img = _paper_row(img, [x0, ry, x1, ry + bh], 16)
            d = ImageDraw.Draw(img)
            r = bh * 0.30
            cx = x0 + bh * 0.62
            d.ellipse([cx - r, ry + bh/2 - r, cx + r, ry + bh/2 + r], fill=GOLD)
            d.line([(cx - r*0.45, ry + bh/2 + r*0.05), (cx - r*0.08, ry + bh/2 + r*0.42),
                    (cx + r*0.5, ry + bh/2 - r*0.4)], fill=DK, width=max(4, int(r*0.3)), joint="curve")
            d.text((cx + bh*0.60, ry + bh/2), b, font=F(27 if H > 1200 else 23, "SemiBold"),
                   fill=CREAM, anchor="lm")
            ry += bh + 14
    img = footer_bar(img, brand)
    return _accent_arc(img, brand)

# ------------------------------------------------------------------ SERVICES
def services(brand, size, kicker, title, items, bg_path=None, cta=True):
    W, H = size
    img = _canvas_bg(size, bg_path)
    img = place_logo_top(img, brand, light_bg=False)
    px, ww = _px(H), _ww(H)
    y = H * (0.245 if H > 1200 else 0.30)
    y = _kicker_on_photo(img, y, kicker)
    y = _title_on_photo(img, y + 4, title, maxw=W - 280)
    y += 28
    bottom = H - (330 if H > 1200 else 262) if cta else H - (216 if H > 1200 else 178)
    img = _paper(img, [px, int(y), W - px, int(bottom)], 42)
    d = ImageDraw.Draw(img)
    n = len(items)
    row_h = (bottom - y - (138 if cta else 44)) / n
    ry = y + 22
    for i, it in enumerate(items):
        x0, x1 = px + 36, W - px - 36
        img = _paper_row(img, [x0, ry, x1, ry + row_h - 12], (row_h - 12) // 2)
        d = ImageDraw.Draw(img)
        sparkle(d, x0 + 48, ry + (row_h - 12)/2, 14, GOLD, ratio=0.42, spread=0.18)
        d.text((x0 + 84, ry + (row_h - 12)/2), it, font=F(28 if H > 1200 else 24, "SemiBold"),
               fill=CREAM, anchor="lm")
        ry += row_h
    if cta:
        _cta_on_paper(img, int(bottom) - 70)
    img = footer_bar(img, brand)
    return _accent_arc(img, brand)

# ------------------------------------------------------------------ COUNTDOWN
def countdown(brand, size, kicker, datebig, sub, bg_path=None, badge=None):
    W, H = size
    img = _canvas_bg(size, bg_path)
    img = place_logo_top(img, brand, light_bg=False)
    px, ww = _px(H), _ww(H)
    y = H * (0.375 if H > 1200 else 0.42)
    y = _kicker_on_photo(img, y, kicker)
    panel_y0 = int(y + 20)
    panel_y1 = int(panel_y0 + (480 if H > 1200 else 412))
    img = _paper(img, [px, panel_y0, W - px, panel_y1], 42)
    d = ImageDraw.Draw(img)
    fd_sz = _serif_fit(d, datebig, ww, 140 if H > 1200 else 112, 60, wght=800)
    fd = SF(fd_sz, 800)
    yy = panel_y0 + (112 if H > 1200 else 92)
    d.text((W/2, yy), datebig, font=fd, fill=GOLD, anchor="mm")
    yy += fd_sz * 0.86
    d.line([(W/2 - 72, yy), (W/2 + 72, yy)], fill=GOLD, width=6)
    yy += 36
    fsu = F(27 if H > 1200 else 24, "SemiBold")
    for ln in wrap_text(sub, fsu, ww, d)[:2]:
        d.text((W/2, yy), ln, font=fsu, fill=SAGE, anchor="mm"); yy += 40
    _cta_on_paper(img, panel_y1 - 74)
    img = footer_bar(img, brand)
    if badge:
        d = ImageDraw.Draw(img)
        fbx = F(25, "Bold"); bw = d.textlength(badge, font=fbx) + 52
        by0, by1 = (150, 206) if H > 1200 else (112, 166)
        pill(d, [W - bw - 30, by0, W - 30, by1], GOLD)
        d.text((W - 30 - bw/2, (by0+by1)/2 - 2), badge, font=fbx, fill=DK, anchor="mm")
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
    px, ww = _px(H), _ww(H)
    panel_y0 = int(H * (0.46 if H > 1200 else 0.50))
    panel_y1 = int(panel_y0 + (620 if H > 1200 else 486))
    img = _paper(img, [px, panel_y0, W - px, panel_y1], 42)
    d = ImageDraw.Draw(img)
    ft_sz = _serif_fit(d, headline, ww, 62 if H > 1200 else 52, 38, wght=760)
    yy = panel_y0 + (76 if H > 1200 else 62)
    yy = _rich_center(d, W_/2, yy + ft_sz*0.55, headline, ft_sz, ww, wght=760)
    yy += 16
    fs = F(27 if H > 1200 else 24, "Medium")
    for ln in wrap_text(sub, fs, ww, d)[:2]:
        d.text((W/2, yy), ln, font=fs, fill=SAGE, anchor="mm"); yy += 40
    if phone_big:
        fph = F(52 if H > 1200 else 42, "ExtraBold")
        yy += 22
        d.text((W/2, yy), brand["phone"], font=fph, fill=GOLD, anchor="mm")
        yy += fph.size + 6
        d.text((W/2, yy), brand["site"], font=F(26, "SemiBold"), fill=SAGE, anchor="mm")
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
    d.line([(0, y), (w * 0.42, y)], fill=GOLD, width=6)
    d.line([(w * 0.44, y), (w * 0.60, y)], fill=CREAM, width=6)
    return img
