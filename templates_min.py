"""PHOTO-FIRST templates — client directive: no blocks, no heavy writing.
Full-bleed photography, small logo + chip, ONE short headline line and a small
contact line over a soft bottom gradient. Brand-aware:
  Spruce Lights  -> Playfair serif, gold emphasis words
  Spruce Pro     -> Poppins bold, cyan emphasis words"""
import spruce_kit as K
from spruce_kit import (bg_photo, cinema, scrim, place_logo_top, save, ROOT,
                        FONTS, star_row, wrap_text, load_logo)
from PIL import Image, ImageDraw, ImageFilter, ImageFont

SQ = (1080, 1080)
ST = (1080, 1920)

CREAM = (250, 248, 242)
GOLD = (240, 176, 45)
CYAN = (95, 227, 234)
MUTED = (216, 220, 212)

_SFC = {}
def SF(size, wght=760):
    k = (size, wght)
    if k not in _SFC:
        f = ImageFont.truetype(f"{FONTS}/PlayfairDisplay.ttf", size)
        try: f.set_variation_by_axes([wght])
        except Exception: pass
        _SFC[k] = f
    return _SFC[k]

def _segs(text):
    """'foo *bar* baz' -> [(t, is_hi), ...]"""
    segs, cur, hi = [], '', False
    for ch in text:
        if ch == '*':
            if cur: segs.append((cur, hi)); cur = ''
            hi = not hi
        else:
            cur += ch
    if cur: segs.append((cur, hi))
    return segs

def _shadow_text(img, xy, text, font, fill, anchor="mm", blur=5, alpha=150):
    sh = Image.new('RGBA', img.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).text(xy, text, font=font, fill=(5, 12, 7, alpha), anchor=anchor)
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur)))
    ImageDraw.Draw(img).text(xy, text, font=font, fill=fill, anchor=anchor)

def _fit_lines(d, plain, font_fn, size, min_size, maxw, max_lines):
    s = size
    while s > min_size:
        f = font_fn(s)
        lines = wrap_text(plain, f, maxw, d)
        if len(lines) <= max_lines and max(d.textlength(l, font=f) for l in lines) <= maxw:
            return s, lines, f
        s -= 3
    f = font_fn(min_size)
    return min_size, wrap_text(plain, f, maxw, d)[:max_lines], f

def _headline(img, cy, text, serif, maxw=None, size=None):
    """1-2 line emphasis headline, centered, soft shadow. Returns bottom y."""
    W, H = img.size
    maxw = maxw or W - 150
    size = size or (64 if H > 1200 else 56)
    def font_fn(s):
        return SF(s, 800) if serif else ImageFont.truetype(f"{FONTS}/Poppins-Bold.ttf", s)
    d = ImageDraw.Draw(img)
    s, _, f = _fit_lines(d, text.replace('*', ''), font_fn, size, 34, maxw, 2)
    # wrap flagged words directly
    words = [(w, g) for seg, g in _segs(text) for w in seg.split(' ') if w]
    sp_w = d.textlength(' ', font=f)
    rows, cur_r, cur_w = [], [], 0
    for w, g in words:
        ww = d.textlength(w, font=f)
        add = ww if not cur_r else cur_w + sp_w + ww
        if cur_r and add > maxw:
            rows.append(cur_r); cur_r, cur_w = [(w, g)], ww
        else:
            cur_r.append((w, g)); cur_w = add
    if cur_r: rows.append(cur_r)
    lh = s * (1.16 if serif else 1.18)
    y = cy - (len(rows) - 1) * lh / 2
    for row in rows:
        x = W/2 - (sum(d.textlength(w, font=f) for w, _ in row) + sp_w * (len(row) - 1)) / 2
        for w, g in row:
            col = (GOLD if serif else CYAN) if g else CREAM
            _shadow_text(img, (x, y), w, f, col, anchor="lm")
            x += d.textlength(w, font=f) + sp_w
        y += lh
    return y

def _contact(img, brand):
    """small floating contact line, centered near the bottom edge"""
    W, H = img.size
    y = H - (56 if H > 1200 else 52)
    d = ImageDraw.Draw(img)
    f = ImageFont.truetype(f"{FONTS}/Poppins-SemiBold.ttf", 26 if H > 1200 else 24)
    txt = f'{brand["phone"]}   ·   {brand["site"]}'
    _shadow_text(img, (W/2, y), txt, f, (245, 243, 236), anchor="mm", blur=4, alpha=170)
    return img

def _base(img, brand, bottom=0.34):
    W, H = img.size
    img = cinema(img, strength=0.6)
    img = scrim(img, strength=0.5, top_frac=0.10, bottom_frac=bottom)
    img = place_logo_top(img, brand, light_bg=False)
    return img

# ---------------------------------------------------------------- hero / line
def hero(brand, size, bg_path, caption=None, focus=0.5, brighten=1.0):
    W, H = size
    img = bg_photo(bg_path, W, H, focus=focus, blur=1.2, brighten=brighten, sat=1.05)
    img = _base(img, brand)
    if caption:
        serif = brand["key"] == "spruce_lights"
        _headline(img, H - (300 if H > 1200 else 268), caption, serif)
    img = _contact(img, brand)
    return img

def line(brand, size, text, bg_path, focus=0.5):
    return hero(brand, size, bg_path, caption=text, focus=focus)

# ---------------------------------------------------------------- review
def review(brand, size, quote, name, detail, bg_path=None, focus=0.42):
    W, H = size
    img = bg_photo(bg_path, W, H, focus=focus, blur=1.2, sat=1.05)
    img = _base(img, brand, bottom=0.42)
    d = ImageDraw.Draw(img)
    serif = brand["key"] == "spruce_lights"
    hi = GOLD if serif else CYAN
    y_top = H - (508 if H > 1200 else 420)
    star_row(d, W/2, y_top, size=26 if H > 1200 else 22, gap=44)
    fq_size = 40 if H > 1200 else 35
    def font_fn(s):
        return SF(s, 700) if serif else ImageFont.truetype(f"{FONTS}/Poppins-SemiBold.ttf", s)
    plain = '\u201c' + quote + '\u201d'
    s, lines, f = _fit_lines(d, plain, font_fn, fq_size, 26, W - 170, 3)
    y = y_top + 62
    for ln in lines:
        _shadow_text(img, (W/2, y), ln, f, CREAM, anchor="mm", blur=6)
        y += s * 1.24
    fn_ = ImageFont.truetype(f"{FONTS}/Poppins-Bold.ttf", 30 if H > 1200 else 26)
    _shadow_text(img, (W/2, y + 14), name, fn_, hi, anchor="mm")
    fd = ImageFont.truetype(f"{FONTS}/Poppins-Medium.ttf", 21 if H > 1200 else 19)
    _shadow_text(img, (W/2, y + 56), detail, fd, MUTED, anchor="mm", blur=4, alpha=130)
    return _contact(img, brand)

# ---------------------------------------------------------------- stat / number
def stat(brand, size, big, unit, bg_path=None, focus=0.45, cta=True, badge=None):
    W, H = size
    img = bg_photo(bg_path, W, H, focus=focus, blur=1.2, sat=1.05)
    img = _base(img, brand, bottom=0.40)
    d = ImageDraw.Draw(img)
    serif = brand["key"] == "spruce_lights"
    hi = GOLD if serif else CYAN
    fb = SF(170 if H > 1200 else 140, 820) if serif else ImageFont.truetype(f"{FONTS}/Poppins-ExtraBold.ttf", 150 if H > 1200 else 124)
    yb = H - (404 if H > 1200 else 356)
    _shadow_text(img, (W/2, yb), big, fb, hi, anchor="mm", blur=8)
    fu = ImageFont.truetype(f"{FONTS}/Poppins-Bold.ttf", 40 if H > 1200 else 34)
    _shadow_text(img, (W/2, yb + (108 if H > 1200 else 94)), unit.upper(), fu, CREAM, anchor="mm", blur=6)
    return _contact(img, brand)

# ---------------------------------------------------------------- poll
def poll(brand, size, kicker, title, options, bg_path=None, note=None):
    W, H = size
    img = bg_photo(bg_path, W, H, blur=1.2, sat=1.05)
    img = _base(img, brand, bottom=0.40)
    serif = brand["key"] == "spruce_lights"
    y = _headline(img, H - (420 if H > 1200 else 372), title, serif)
    d = ImageDraw.Draw(img)
    fo = ImageFont.truetype(f"{FONTS}/Poppins-SemiBold.ttf", 29 if H > 1200 else 26)
    opts = "   ·   ".join(o.replace(' — ', ' ') for o in options)
    fopt = ImageFont.truetype(f"{FONTS}/Poppins-Medium.ttf", 25 if H > 1200 else 22)
    lines = wrap_text(opts, fopt, W - 150, d)[:2]
    yy = y + 26
    for ln in lines:
        _shadow_text(img, (W/2, yy), ln, fopt, CREAM, anchor="mm", blur=5)
        yy += 36
    fnote = ImageFont.truetype(f"{FONTS}/Poppins-Medium.ttf", 23)
    _shadow_text(img, (W/2, yy + 22), note or "Vote in the comments", fnote,
                 GOLD if serif else CYAN, anchor="mm", blur=4)
    return _contact(img, brand)

# ---------------------------------------------------------------- before/after (photo composition, minimal text)
def before_after(brand, size, path_a, path_b, kicker, title, la="BEFORE", lb="AFTER", focus=0.55):
    import templates as _T
    return _T.before_after(brand, size, path_a, path_b, kicker, title, la, lb, focus)
