"""Full-canvas audit v2: per-image tracking of text/pill/logo collisions."""
import sys, os
sys.path.insert(0, '/home/user/spruce')
import PIL.ImageDraw as ID
import spruce_kit as K

REPORT = []
STATE = {'texts': [], 'logos': []}   # each entry: (im_id, box, label)

RealDraw = ID.ImageDraw
class AuditDraw(RealDraw):
    def text(self, xy, text, fill=None, font=None, anchor=None, **kw):
        try:
            box = self.textbbox(xy, text, font=font, anchor=anchor,
                                stroke_width=kw.get('stroke_width', 0))
            STATE['texts'].append((id(self.im), box, str(text)[:32]))
        except Exception:
            pass
        return super().text(xy, text, fill=fill, font=font, anchor=anchor, **kw)

def draw_proxy(im, mode=None):
    return AuditDraw(im, mode)
ID.Draw = draw_proxy

_orig_place = K.place_logo_top
def place_track(img, brand, light_bg=False, h=None, pad=44):
    out = _orig_place(img, brand, light_bg=light_bg, h=h, pad=pad)
    if K.LOGO_RECT:
        STATE['logos'].append((id(img), K.LOGO_RECT))
    return out
K.place_logo_top = place_track

def rects_intersect(a, b, margin=5):
    return not (a[2] < b[0]-margin or a[0] > b[2]+margin or a[3] < b[1]-margin or a[1] > b[3]+margin)

_orig_save = K.save
def save_track(img, path, q=90):
    W, H = img.size
    iid = id(img)
    issues = []
    logo = next((r for (l, r) in STATE['logos'] if l == iid), None)
    for (l, box, txt) in STATE['texts']:
        if l != iid: continue
        x0, y0, x1, y1 = box
        if logo and rects_intersect((x0, y0, x1, y1), logo):
            issues.append(f"TEXT×LOGO '{txt}' txt={tuple(int(v) for v in box)} logo={tuple(int(v) for v in logo)}")
        if x0 < 22 or x1 > W - 22:
            issues.append(f"EDGE '{txt}' box={tuple(int(v) for v in box)} W={W}")
        if y1 > H - 4:
            issues.append(f"BOTTOM '{txt}' y1={int(y1)} H={H}")
        if y0 < 8:
            issues.append(f"TOP '{txt}' y0={int(y0)}")
    STATE['texts'] = []; STATE['logos'] = []
    REPORT.append((path, issues))
    return _orig_save(img, path, q)
K.save = save_track

import templates as T
T.place_logo_top = place_track
T.save = save_track
_orig_cta = T.cta_card
def cta_track(brand, size, *a, **kw):
    out = _orig_cta(brand, size, *a, **kw)
    if K.LOGO_RECT:
        STATE['logos'].append((id(out), K.LOGO_RECT))
    return out
T.cta_card = cta_track

os.chdir('/home/user/spruce')
exec(open('render_sl.py').read())
exec(open('render_sp.py').read())

bad = 0
for path, issues in REPORT:
    if issues:
        bad += 1
        print('⚠', os.path.basename(path))
        for i in issues[:8]:
            print('   ', i)
print(f'\n==== {len(REPORT)} cards audited, {bad} with issues ====')
