"""
SPRUCE DESIGN SYSTEM — brand kit for Spruce Holiday Lighting & Events
and Spruce Services & Solutions. Renders feed (1080x1080) + story (1080x1920)
social graphics using the companies' ACTUAL logos and exact brand colors.
"""
import math, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance

ROOT   = "/home/user/spruce"
BRAND  = f"{ROOT}/assets/brand"
FONTS  = f"{ROOT}/assets/fonts"
OUT    = f"{ROOT}/deliverables"

# ---------------------------------------------------------------- brand data
TEAL      = (0, 48, 60, 255)        # #00303C  deep spruce teal
TEAL_D    = (0, 33, 42, 255)        # darker
TEAL_L    = (10, 74, 88, 255)
CYAN      = (28, 200, 208, 255)     # #1CC8D0
LIME      = (144, 208, 0, 255)      # #90D000
RED       = (200, 32, 40, 255)      # #C82028  santa / urgency
CREAM     = (250, 247, 240, 255)    # warm white text
WHITE     = (255, 255, 255, 255)
BULBS     = [(200,32,40), (255,201,60), (76,175,62), (64,176,224), (240,128,40)]
GOLD      = (255, 201, 60, 255)
# switchable dark-tone globals (SL renders on Christmas green, SP on teal)
SCRIM_COLOR = (0, 20, 26)
FOOT_DARK   = (0, 26, 33)
CINE_SHADOW = (0.00, 0.10, 0.13)   # shadow-lift hue for cinema()

SL = dict(
    key="spruce_lights", name="Spruce Holiday Lighting & Events",
    handle="@spruceholidaylighting", phone="(864) 288-2459",
    site="sprucelights.com", cta="Get My Free Quote",
    logo=f"{BRAND}/sl_logo.png",
)
SP = dict(
    key="spruce_pro", name="Spruce Services & Solutions",
    handle="@spruce_pro", phone="(864) 483-4300",
    site="sprucepro.com", cta="Get My Free Quote",
    logo=f"{BRAND}/sp_logo_color.png",
)

# ---------------------------------------------------------------- fonts
_font_cache = {}
def F(size, weight="Bold", serif=False, italic=False):
    key = (size, weight, serif, italic)
    if key not in _font_cache:
        if serif:
            fn = f"{FONTS}/PlayfairDisplay-Italic.ttf" if italic else f"{FONTS}/PlayfairDisplay.ttf"
        else:
            fn = f"{FONTS}/Poppins-{weight}.ttf"
        _font_cache[key] = ImageFont.truetype(fn, size)
    return _font_cache[key]

# ---------------------------------------------------------------- logo prep
LOGO_RECT = None   # (x0,y0,x1,y1) of the most recently placed logo (audit/QA)

def load_logo(brand, light_bg=True, height=None):
    """Returns RGBA logo. For Spruce Lights on dark backgrounds the dark
    wordmark is recolored to warm white while keeping the bulbs/hat/sparkles
    in full color. Spruce Pro has an official white logo for dark backgrounds."""
    im = Image.open(brand["logo"]).convert("RGBA")
    if not light_bg:
        if brand["key"] == "spruce_pro":
            im = Image.open(f"{BRAND}/sp_logo_white.png").convert("RGBA")
        else:
            im = _winter_white(im)
    if height:
        w = int(im.width * height / im.height)
        im = im.resize((w, height), Image.LANCZOS)
    return im

def _winter_white(im):
    px = im.load()
    for y in range(im.height):
        for x in range(im.width):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            v = max(r, g, b); s = (v - min(r, g, b))
            if v < 140 or (s < 40 and v < 190):   # dark / grey-teal wordmark -> cream
                px[x, y] = (250, 247, 240, a)
    return im

# ---------------------------------------------------------------- helpers
def canvas(w, h, color=TEAL):
    return Image.new("RGBA", (w, h), color)

def vgrad(size, top, bottom):
    """vertical gradient RGBA"""
    w, h = size
    base = Image.new("RGB", (1, h))
    for y in range(h):
        t = y / max(h - 1, 1)
        base.putpixel((0, y), tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3)))
    return base.resize((w, h)).convert("RGBA")

def radial_glow(size, center, radius, color, peak=140):
    """soft radial glow on transparent layer"""
    w, h = size
    layer = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(layer)
    steps = 28
    for i in range(steps, 0, -1):
        r = radius * i / steps
        a = int(peak * (1 - i / steps) ** 2)
        d.ellipse([center[0]-r, center[1]-r, center[0]+r, center[1]+r], fill=a)
    glow = Image.new("RGBA", (w, h), color[:3] + (0,))
    glow.putalpha(layer)
    return glow

def sparkle(d, cx, cy, r, color, ratio=0.32, spread=0.16):
    """4-point concave sparkle, matching the logo's star motif."""
    pts = []
    for i in range(4):
        ang = math.pi / 2 * i - math.pi / 2
        nx, ny = math.cos(ang), math.sin(ang)
        px, py = -ny, nx
        pts.append((cx + nx * r, cy + ny * r))
        pts.append((cx + px * r * spread + nx * r * ratio * 0.0, cy + py * r * spread))
        pts.append((cx + nx * r * ratio, cy + ny * r * ratio))
        pts.append((cx - px * r * spread, cy - py * r * spread))
    d.polygon(pts, fill=color)

def sparkle_img(r, color):
    s = int(r * 2.4)
    im = Image.new("RGBA", (s, s), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    sparkle(d, s / 2, s / 2, r, color)
    return im

def bulb_strand(w, y0, y1, droop=3, bulb=22, seed=7):
    """Catenary string of C9 bulbs in brand colors — mirrors the SL logo strand."""
    import random
    rnd = random.Random(seed)
    im = Image.new("RGBA", (w, int(abs(y1 - y0)) + bulb * 4), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    span = w
    sag = abs(y1 - y0)
    pts = []
    for x in range(0, span, 6):
        t = x / span
        y = (4 * sag) * t * (1 - t)          # parabola sag
        pts.append((x, y))
    d.line(pts, fill=(20, 40, 35, 255), width=5)
    n = max(4, span // 150)
    for i in range(1, n):
        t = i / n
        x = t * span
        y = (4 * sag) * t * (1 - t)
        c = BULBS[i % len(BULBS)]
        # socket
        d.rounded_rectangle([x - 6, y - 2, x + 6, y + 12], 4, fill=(30, 45, 40, 255))
        # bulb (C9 shape)
        d.ellipse([x - bulb * 0.42, y + 8, x + bulb * 0.42, y + 8 + bulb * 0.95], fill=c + (255,))
        hi = tuple(min(255, int(v * 1.55)) for v in c)
        d.ellipse([x - bulb * 0.2, y + 12, x + bulb * 0.05, y + 12 + bulb * 0.42], fill=hi + (200,))
    return im

def wrap_text(text, font, max_w, d):
    lines, cur = [], ""
    for word in text.split():
        test = (cur + " " + word).strip()
        if d.textlength(test, font=font) <= max_w:
            cur = test
        else:
            if cur: lines.append(cur)
            cur = word
    if cur: lines.append(cur)
    return lines

def draw_fit(d, text, font_path_w, max_w, start_size, min_size, weights=None):
    """find largest size that fits one line"""
    for s in range(start_size, min_size, -4):
        f = F(s, font_path_w)
        if d.textlength(text, font=f) <= max_w:
            return f
    return F(min_size, font_path_w)

def mist(img, color=TEAL, top=150, mid=92, bottom=210, focus_pt=0.5):
    """'mist' veil over a photo: stronger at top/bottom, lightest around the
    focus point so the photo stays clearly visible while text pops."""
    w, h = img.size
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    fp = focus_pt
    for y in range(h):
        t = y / (h - 1)
        if t < fp:
            a = top + (mid - top) * (t / fp) ** 0.9
        else:
            a = mid + (bottom - mid) * ((t - fp) / (1 - fp)) ** 1.15
        d.line([(0, y), (w, y)], fill=color[:3] + (int(max(0, min(255, a))),))
    return Image.alpha_composite(img, ov)

def text_scrim(img, cy, height, alpha=105, color=None, blur=34):
    color = color or SCRIM_COLOR
    """soft blurred dark band behind a text block — legibility without walls"""
    w, h = img.size
    lay = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(lay)
    y0, y1 = int(cy - height / 2), int(cy + height / 2)
    for y in range(max(0, y0), min(h, y1)):
        t = (y - y0) / max(1, (y1 - y0))
        d.line([(0, y), (w, y)], fill=int(alpha * (1 - abs(t - 0.5) * 2) ** 1.4))
    lay = lay.filter(ImageFilter.GaussianBlur(blur))
    ov = Image.new("RGBA", (w, h), color + (0,))
    ov.putalpha(lay)
    img.alpha_composite(ov)
    return img

# ---------------------------------------------------------------- blend v3: cinematic
def cinema(img, strength=1.0):
    """teal-lifted shadows, warm highlights, gentle S-curve, vignette, grain."""
    import numpy as np
    a = np.asarray(img.convert("RGB")).astype(np.float32) / 255.0
    luma = a.mean(axis=2, keepdims=True)
    sh_w = ((1 - luma) ** 2) * 0.34 * strength          # shadow weight (H,1)
    hi_w = (luma ** 1.6) * 0.10 * strength              # highlight weight
    teal = np.array(CINE_SHADOW, np.float32)            # shadow-lift hue
    warm = np.array([0.05, 0.025, 0.00], np.float32)    # highlights warm up
    a = a * (1 - sh_w) + teal.reshape(1, 1, 3) * sh_w * 0.9
    a = a * (1 + warm.reshape(1, 1, 3) * hi_w * 2.2)
    a = np.clip(a, 0, 1)
    a = a * a * (3 - 2 * a) * 0.22 + a * 0.78           # gentle S-curve
    out = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).convert("RGBA")
    out.alpha_composite(vignette(out.size, alpha=68 * strength))
    return grain(out, amt=3.2 * strength)

def vignette(size, alpha=60, spread=1.25):
    """soft dark corners"""
    import numpy as np
    w, h = size
    y, x = np.mgrid[0:h, 0:w]
    cx, cy = w / 2, h / 2
    r = np.sqrt(((x - cx) / (w / 2)) ** 2 + ((y - cy) / (h / 2)) ** 2) / spread
    m = (np.clip(r - 0.55, 0, 1) ** 1.6 * alpha).astype(np.uint8)
    ov = Image.new("RGBA", (w, h), (2, 16, 22, 0))
    ov.putalpha(Image.fromarray(m, "L"))
    return ov

def grain(img, amt=3.0):
    import numpy as np
    a = np.asarray(img).astype(np.int16)
    n = np.random.normal(0, amt, a.shape[:2])[..., np.newaxis].astype(np.int16)
    a = np.clip(a + n, 0, 255).astype(np.uint8)
    return Image.fromarray(a, "RGBA")

def frost(img, cx, cy, bw, bh, blur=9, darken=0.88, feather=42):
    """frosted-glass zone: blur + slight darken inside a feathered rounded box."""
    w, h = img.size
    mask = Image.new("L", (w, h), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        [cx - bw / 2, cy - bh / 2, cx + bw / 2, cy + bh / 2], 60, fill=235)
    mask = mask.filter(ImageFilter.GaussianBlur(feather))
    soft = img.filter(ImageFilter.GaussianBlur(blur))
    soft = ImageEnhance.Brightness(soft).enhance(darken)
    out = Image.composite(soft, img, mask)
    return out

def glass_round(img, box, radius, fill_a=26, outline=None, width=0):
    """draw a translucent glass panel WITH true alpha compositing"""
    ov = Image.new("RGBA", img.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    od.rounded_rectangle(box, radius, fill=(255, 255, 255, fill_a),
                         outline=outline, width=width)
    img.alpha_composite(ov)
    return img

def pill(d, box, fill, radius=None):
    x0, y0, x1, y1 = box
    r = radius if radius is not None else (y1 - y0) // 2
    d.rounded_rectangle(box, r, fill=fill)

def star_row(d, cx, y, n=5, size=26, gap=44, color=GOLD):
    start = cx - (n - 1) * gap / 2
    for i in range(n):
        sparkle(d, start + i * gap, y, size, color, ratio=0.42, spread=0.18)

def scrim(img, strength=0.82, bottom_frac=0.62, top_frac=0.30):
    """dark gradient from top and bottom for legibility"""
    w, h = img.size
    ov = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    th = int(h * top_frac)
    for y in range(th):
        a = int(150 * (1 - y / th) ** 1.4 * (strength + 0.15))
        d.line([(0, y), (w, y)], fill=SCRIM_COLOR + (min(a, 255),))
    bh = int(h * bottom_frac)
    for y in range(bh):
        a = int(230 * strength * (y / bh) ** 1.25)
        d.line([(0, h - bh + y), (w, h - bh + y)], fill=SCRIM_COLOR + (min(a, 255),))
    return Image.alpha_composite(img, ov)

def place_logo_top(img, brand, light_bg=False, h=None, pad=44):
    logo = load_logo(brand, light_bg=light_bg, height=h or 168)
    # trim transparent margins
    bbox = logo.getbbox()
    if bbox: logo = logo.crop(bbox)
    x = (img.width - logo.width) // 2
    img.alpha_composite(logo, (x, pad))
    global LOGO_RECT
    LOGO_RECT = (x, pad, x + logo.width, pad + logo.height)
    return img

def footer_bar(img, brand, light_text=True, h=None):
    """bottom brand bar: phone • website  + handle"""
    w, H = img.size
    hh = h or (150 if H > 1200 else 118)
    d = ImageDraw.Draw(img)
    top = H - hh
    for i in range(hh):
        a = int(210 * (i / hh) ** 0.5)
        d.line([(0, top + i), (w, top + i)], fill=(0, 26, 33, min(a, 235)))
    tc = CREAM if light_text else TEAL
    f1 = F(34 if H > 1200 else 30, "SemiBold")
    f2 = F(26 if H > 1200 else 23, "Regular")
    txt = f"{brand['phone']}   •   {brand['site']}"
    d.text((w // 2, top + hh * 0.38), txt, font=f1, fill=tc, anchor="mm")
    d.text((w // 2, top + hh * 0.76), brand["handle"], font=f2, fill=(CYAN if light_text else TEAL_L), anchor="mm")
    return img

def cta_pill(img, brand, cy, text=None, fill=LIME, fg=TEAL_D):
    d = ImageDraw.Draw(img)
    t = text or brand["cta"]
    f = F(40, "Bold")
    tw = d.textlength(t, font=f)
    pad = 46
    box = [img.width // 2 - tw / 2 - pad, cy - 38, img.width // 2 + tw / 2 + pad, cy + 38]
    # soft shadow
    sh = Image.new("RGBA", img.size, (0,0,0,0))
    ImageDraw.Draw(sh).rounded_rectangle([box[0]+4, box[1]+8, box[2]+4, box[3]+8], 38, fill=(0,0,0,110))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(8)))
    pill(d, box, fill)
    d.text((img.width // 2, cy - 2), t, font=f, fill=fg, anchor="mm")
    return img

def bg_photo(path, w, h, focus=0.5, brighten=1.0, sat=1.05, blur=0):
    """cover-fit a photo to exact canvas"""
    im = Image.open(path).convert("RGB")
    if blur: im = im.filter(ImageFilter.GaussianBlur(blur))
    if brighten != 1.0: im = ImageEnhance.Brightness(im).enhance(brighten)
    if sat != 1.0: im = ImageEnhance.Color(im).enhance(sat)
    r = max(w / im.width, h / im.height)
    nw, nh = int(im.width * r) + 1, int(im.height * r) + 1
    im = im.resize((nw, nh), Image.LANCZOS)
    x = (nw - w) // 2
    y = max(0, min(nh - h, int((nh - h) * focus)))
    return im.crop((x, y, x + w, y + h)).convert("RGBA")

def sparkle_scatter(img, seed=3, n=5, color=CYAN, region=None, rmax=34):
    """subtle sparkle accents; never inside the logo zone"""
    import random
    rnd = random.Random(seed)
    d = ImageDraw.Draw(img)
    c3 = color[:3]
    ytop = (region or (60, int(img.height * 0.28)))[0]
    ybot = (region or (0, int(img.height * 0.28)))[1]
    if LOGO_RECT:                       # keep sparkles off the logo
        ytop = max(ytop, LOGO_RECT[3] + 26)
        if ybot <= ytop:
            ybot = ytop + 10
    for _ in range(n):
        x = rnd.randint(60, img.width - 60)
        y = rnd.randint(ytop, ybot)
        sparkle(d, x, y, rnd.randint(12, rmax), c3 + (rnd.randint(90, 190),), ratio=0.4, spread=0.17)
    return img

def save(img, path, q=90):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    img.convert("RGB").save(path, quality=q, optimize=True)
    return path
