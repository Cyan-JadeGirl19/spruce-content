"""SP_21-24 'Did You Know?' series — flyer-inspired faceted design (user ref:
CLEAN GUTTERS, CLEAR FLOW): real photo up top, diamond seam, deep-teal fact
panel with dotted pattern, lime kicker, bold fact, checkmark points, footer."""
import sys; sys.path.insert(0, '/home/user/spruce')
import spruce_kit as _K
_K.TEAL = (0, 48, 60, 255); _K.TEAL_D = (0, 33, 42, 255); _K.TEAL_L = (10, 74, 88, 255)
from spruce_kit import (SP, F, TEAL, TEAL_D, TEAL_L, CYAN, LIME,
                        bg_photo, footer_bar, save, vgrad)
from templates_photo import _brand_chip, _logo_plate
from PIL import Image, ImageDraw
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
P = f'{ROOT}/assets/photos/sp_ai'
OUT = f'{ROOT}/deliverables/spruce_pro'

def _dots(img, x0, y0, cols, rows, color=(255, 255, 255, 44), r=4, gap=24):
    ov = Image.new('RGBA', img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    for i in range(cols):
        for j in range(rows):
            cx, cy = x0 + i * gap, y0 + j * gap
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=color)
    img.alpha_composite(ov)
    return img

def _diamond(img, cx, cy, s, color):
    d = ImageDraw.Draw(img)
    d.polygon([(cx, cy - s), (cx + s, cy), (cx, cy + s), (cx - s, cy)], fill=color)

def _check(d, x, y, s, color=LIME):
    d.ellipse([x, y, x + 2 * s, y + 2 * s], outline=color, width=max(3, s // 3))
    d.line([(x + 0.5 * s, y + 1.05 * s), (x + 0.9 * s, y + 1.45 * s), (x + 1.55 * s, y + 0.6 * s)],
           fill=color, width=max(3, s // 3), joint="curve")

def _wrap(d, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= maxw: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def dyk_post(brand, size, photo, fact, points, photo_h):
    W, H = size
    img = Image.new('RGBA', (W, H), TEAL_D)
    img.paste(bg_photo(photo, W, photo_h, focus=0.45, brighten=1.04, sat=1.06), (0, 0))
    seam = photo_h
    panel = vgrad((W, H - seam), (0, 56, 68, 255), TEAL_D)
    img.paste(panel, (0, seam))
    img = _dots(img, int(W * 0.858), seam + int(W * 0.042), 5, 4)
    # diamond seam cluster (flyer signature)
    _diamond(img, W // 2, seam, int(W * 0.052), tuple(LIME[:3]))
    _diamond(img, W // 2 + int(W * 0.115), seam, int(W * 0.026), tuple(CYAN[:3]))
    _diamond(img, W // 2 - int(W * 0.10), seam, int(W * 0.019), (250, 247, 240))
    d = ImageDraw.Draw(img)
    lx = int(W * 0.055)
    # kicker
    d.text((lx, seam + int(W * 0.038)), "DID YOU KNOW?", font=F(int(W * 0.036), "ExtraBold"),
           fill=tuple(LIME[:3]))
    # fact (fit to 3 lines max)
    fs = int(W * 0.0445)
    while fs > int(W * 0.032):
        ff = F(fs, "Bold")
        if len(_wrap(d, fact, ff, int(W * 0.90))) <= 3: break
        fs -= 2
    ff = F(fs, "Bold")
    lines = _wrap(d, fact, ff, int(W * 0.90))
    y = seam + int(W * 0.098)
    for ln in lines:
        d.text((lx, y), ln, font=ff, fill=(250, 247, 240))
        y += int(fs * 1.28)
    # check points, single column, clear of the footer
    ps = int(W * 0.0185)
    pf = F(int(W * 0.0265), "SemiBold")
    cy0 = y + int(W * 0.032)
    last_bottom = 0
    for i, ptext in enumerate(points):
        yy = cy0 + i * int(W * 0.0565)
        _check(d, lx, yy, ps)
        d.text((lx + int(ps * 2.6), yy + ps), ptext, font=pf, fill=(222, 234, 228), anchor="lm")
        last_bottom = yy + 2 * ps
    ft = int(min(W, H) * 0.14)  # footer height
    assert last_bottom <= H - ft - 18, f"panel overflows footer: {last_bottom} vs {H - ft - 18}"
    img = _brand_chip(img, brand)
    img = _logo_plate(img, brand, W)
    img = footer_bar(img, brand)
    return img.convert('RGB')

POSTS = [
 ("SP_21_dyk_gutters", f'{P}/sp21_gutter_overflow.jpg',
  "One inch of rain sheds about 500 gallons off your roof. Clogged gutters dump it beside your foundation.",
  ["Downspouts flushed and checked", "Debris hauled away, not left behind", "Free quote within 24 hours"]),
 ("SP_22_dyk_roof", f'{P}/sp22_roof_algae.jpg',
  "Those dark roof streaks are living algae feeding on your shingles. Rain does not wash them off.",
  ["SoftWash only, never pressure", "Kills the algae at the root", "Stays clean 4 to 5 times longer"]),
 ("SP_23_dyk_windows", f'{P}/sp23_hardwater_spots.jpg',
  "Sprinkler water can permanently etch glass. The longer spots sit, the less any cleaner can touch them.",
  ["Polishing restores the glass", "Sills and tracks included", "Screens cleaned with every wash"]),
 ("SP_24_dyk_drone", f'{P}/sp24_drone_facade.jpg',
  "Our drone rig clears gutters and rooflines up to five stories. No ladders leaning on your home.",
  ["Video inspection included", "Safer for your roof, faster for you", "Free quote with every flight"]),
]

if __name__ == '__main__':
    for name, photo, fact, points in POSTS:
        save(dyk_post(SP, (1080, 1080), photo, fact, points, 420), f'{OUT}/feed/{name}_feed.jpg')
        save(dyk_post(SP, (1080, 1920), photo, fact, points, 940), f'{OUT}/story/{name}_story.jpg')
        print('ok', name)
    print('DYK SERIES DONE')
