"""Spruce Lights SHOWCASE videos v1 — real installation photos, upload-anywhere format.
5 variants x 1080x1350 (4:5), ~20s, quiet soothing music-box bed, brand chip burned in.
Scenes: residential / commercial / municipal / holiday nights / grand tour."""
import sys, math
sys.path.insert(0, '/home/user/spruce')
import spruce_kit as _K
_K.TEAL = (13, 27, 16, 255); _K.TEAL_D = (8, 18, 11, 255); _K.TEAL_L = (24, 44, 28, 255)
_K.SCRIM_COLOR = (2, 14, 8); _K.FOOT_DARK = (3, 20, 12); _K.CINE_SHADOW = (0.0, 0.05, 0.028)
from spruce_kit import *
from vidkit import encode, brand_chip_layer, FPS, sparkle_field_layer, draw_sparkle_field, brand_footer_layer
import audio_kit as AK
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = f'{ROOT}/videos/spruce_lights'
import os; os.makedirs(OUT, exist_ok=True)
SLR = f'{ROOT}/assets/photos/sl_real'
SPR = f'{ROOT}/assets/photos/sp_real2'
W, H = 1080, 1350
GOLD = (240, 176, 45, 255)
CREAM = (246, 240, 226, 255)
SAGE = (164, 178, 156, 255)
PINE = (13, 27, 16)
FONTS = f'{ROOT}/assets/fonts'

def F(s, w="Bold"):
    return ImageFont.truetype(f'{FONTS}/Poppins-{w}.ttf', s)
_SFC = {}
def SF(s, wght=760):
    k = (s, wght)
    if k not in _SFC:
        f = ImageFont.truetype(f'{FONTS}/PlayfairDisplay.ttf', s)
        try: f.set_variation_by_axes([wght])
        except Exception: pass
        _SFC[k] = f
    return _SFC[k]

LOGO_W = load_logo(SL, light_bg=False).crop(load_logo(SL, light_bg=False).getbbox())
LOGO_W.thumbnail((560, 620), Image.LANCZOS)

def cover(path, t=0.0, z0=1.06, z1=1.16, pan=0.0):
    """Ken-Burns cover crop, gentle horizontal pan (pan in -1..1)."""
    src = Image.open(path).convert('RGB')
    z = z0 + (z1 - z0) * t
    # gentle pan: shift crop window by pan*3% over time
    cover_h = int(min(src.width / (W / H), src.height) )
    cover_w = int(cover_h * (W / H))
    if cover_w > src.width:
        cover_w = src.width; cover_h = int(cover_w * (H / W))
    max_dx = src.width - cover_w
    dx = int(max_dx * 0.5 + max_dx * 0.5 * pan * 0.30)
    dy = int((src.height - cover_h) * 0.42)
    crop = src.crop((dx, dy, dx + cover_w, dy + cover_h)).resize((W, H), Image.LANCZOS)
    crop = crop.resize((int(W * z), int(H * z)), Image.LANCZOS)
    x0 = (crop.width - W) // 2; y0 = (crop.height - H) // 2
    frame = crop.crop((x0, y0, x0 + W, y0 + H))
    # cinematic grade + subtle vignette
    frame = cinema(frame.convert('RGBA'), strength=0.35)
    return frame

def seg(t, a, b):
    return max(0.0, min(1.0, (t - a) / (b - a))) if b > a else 1.0
def easeio(u):
    return u * u * (3 - 2 * u)

def text_pill(scene, text, y, size, fill, weight="SemiBold", serif=False, pad=34, ph=None):
    d = ImageDraw.Draw(scene)
    f = SF(size, 800) if serif else F(size, weight)
    tw = d.textlength(text, font=f)
    h = ph or int(size * 1.7)
    ov = Image.new('RGBA', scene.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(ov)
    od.rounded_rectangle([W/2 - tw/2 - pad, y - h/2, W/2 + tw/2 + pad, y + h/2],
                         h/2, fill=(13, 25, 15, 205), outline=(240, 176, 45, 170), width=2)
    scene.alpha_composite(ov)
    d = ImageDraw.Draw(scene)
    d.text((W/2, y - 2), text, font=f, fill=fill, anchor='mm')

def title_card(kicker, title, sub):
    img = Image.new('RGBA', (W, H), PINE + (255,))
    gr = Image.new('L', (1, H))
    for y in range(H):
        gr.putpixel((0, y), int(255 * (y / H) ** 1.3))
    img.paste(Image.new('RGB', (W, H), (7, 15, 9)), (0, 0), gr.resize((W, H)))
    img.alpha_composite(radial_glow((W, H), (W/2, 520), W*0.75, (24, 44, 28), peak=60))
    sp = sparkle_field_layer((W, H), 7, n=14, ymax_frac=0.95)
    draw_sparkle_field(img, sp, 0.6)
    d = ImageDraw.Draw(img)
    lg = LOGO_W.copy()
    img.alpha_composite(lg, ((W - lg.width)//2, 250))
    d = ImageDraw.Draw(img)
    d.text((W/2, 700), title, font=SF(64, 800), fill=CREAM, anchor='mm')
    d.line([(W/2 - 64, 762), (W/2 + 64, 762)], fill=GOLD, width=5)
    d.text((W/2, 830), sub, font=F(30, "Medium"), fill=SAGE, anchor='mm')
    return img

def end_card():
    img = Image.new('RGBA', (W, H), PINE + (255,))
    gr = Image.new('L', (1, H))
    for y in range(H):
        gr.putpixel((0, y), int(255 * (y / H) ** 1.3))
    img.paste(Image.new('RGB', (W, H), (7, 15, 9)), (0, 0), gr.resize((W, H)))
    sp = sparkle_field_layer((W, H), 9, n=16, ymax_frac=0.9)
    draw_sparkle_field(img, sp, 1.0)
    d = ImageDraw.Draw(img)
    lg = LOGO_W.copy()
    img.alpha_composite(lg, ((W - lg.width)//2, 330))
    d = ImageDraw.Draw(img)
    d.text((W/2, 810), "Residential • Commercial • Municipal", font=F(30, "SemiBold"), fill=CREAM, anchor='mm')
    d.text((W/2, 900), "(864) 288-2459", font=F(48, "ExtraBold"), fill=GOLD, anchor='mm')
    d.text((W/2, 968), "sprucelights.com", font=F(28, "SemiBold"), fill=SAGE, anchor='mm')
    return img

def _frames(name, kicker, title, sub, photos, labels):
    """3 acts: title / photos / end card with soft crossfades."""
    D_T, D_P, D_E = 3.6, 4.6, 4.4
    dur = D_T + len(photos) * D_P + D_E
    n = int(dur * FPS)
    X = 0.55  # crossfade seconds
    tc = title_card(kicker, title, sub)
    ec = end_card()
    ph_img = [cover(p, 0.0) for p in photos]
    foot = brand_footer_layer((W, H), SL)
    for i in range(n):
        t = i / FPS
        if t < D_T:
            img = tc.copy()
            e = easeio(seg(t, 0.15, 1.1))
            if e < 1:
                ov = Image.new('RGBA', (W, H), (7, 15, 9, int(255 * (1 - e))))
                img.alpha_composite(ov)
        elif t < D_T + len(photos) * D_P:
            u = t - D_T
            k = min(int(u / D_P), len(photos) - 1)
            local = u - k * D_P
            pan = (local / D_P) * 2 - 1
            img = cover(photos[k], local / D_P, pan=pan)
            # label
            if local > 0.5:
                e = easeio(seg(local, 0.5, 1.2))
                lab = labels[k]
                ov = Image.new('RGBA', (W, H), (0, 0, 0, 0))
                od = ImageDraw.Draw(ov)
                f = F(27, "SemiBold")
                tw = od.textlength(lab, font=f)
                od.rounded_rectangle([W/2 - tw/2 - 30, 1180 - 26, W/2 + tw/2 + 30, 1180 + 26],
                                     26, fill=(13, 25, 15, int(200 * e)),
                                     outline=(240, 176, 45, int(170 * e)), width=2)
                img.alpha_composite(ov)
                d = ImageDraw.Draw(img)
                d.text((W/2, 1178), lab, font=f,
                       fill=(240, 176, 45, int(255 * e)), anchor='mm')
            # crossfade to next photo
            if local > D_P - X and k < len(photos) - 1:
                u2 = (local - (D_P - X)) / X
                nxt = cover(photos[k + 1], 0.0, pan=-1)
                img = Image.blend(img, nxt, easeio(u2))
            # crossfade from title
            if k == 0 and local < X:
                prev = tc.copy()
                img = Image.blend(prev, img, easeio(local / X))
        else:
            u = t - D_T - len(photos) * D_P
            img = ec.copy()
            if u < X:
                last = cover(photos[-1], 1.0, pan=1)
                img = Image.blend(last, img, easeio(u / X))
        img.alpha_composite(foot)
        yield img

def showcase(name, kicker, title, sub, photos, labels):
    """driver: compose audio then encode frames."""
    D_T, D_P = 3.6, 4.6
    dur = D_T + len(photos) * D_P + 4.4
    # audio: quiet soothing bed with accents at act changes
    wavp = f'/tmp/{name}.wav'
    accs = []
    C = [523.25, 659.25, 783.99, 1046.5, 1318.5]
    for k in range(len(photos)):
        accs.append((D_T + k * D_P + 0.15, C[(k + 1) % len(C)]))
    accs.append((D_T + len(photos) * D_P + 0.2, 1046.5))
    AK.sl_track(wavp, dur, seed=hash(name) % 97, accents=accs, density=0.45, fade=1.8)
    import wave
    f = wave.open(wavp); nf = f.getnframes()
    x = np.frombuffer(f.readframes(nf), dtype=np.int16).reshape(-1, 2).astype(np.float32)
    f.close()
    x = AK.sooth(x) * 0.38
    m = max(1.0, np.abs(x).max())
    if m > 29000: x = x * (29000 / m)
    inter = np.empty(2 * nf, dtype=np.int16)
    inter[0::2] = x[:, 0].astype(np.int16); inter[1::2] = x[:, 1].astype(np.int16)
    f = wave.open(wavp, 'w'); f.setnchannels(2); f.setsampwidth(2); f.setframerate(44100)
    f.writeframes(inter.tobytes()); f.close()
    encode(_frames(name, kicker, title, sub, photos, labels), (W, H),
           f'{OUT}/{name}.mp4', chip_brand=SL, audio_wav=wavp)
    print('✓', name)

# ================================================================ the 5
showcase('SL_Showcase_Residential',
         'NOW BOOKING OCTOBER', 'Homes That Glow', 'Residential holiday lighting — done for you',
         [f'{SLR}/sl_02_spruce-christmas-lighting.jpg',
          f'{SLR}/sl_06_nstallation-service-greenville-sc-4.jpg',
          f'{SLR}/sl_10_ghting-installation-greenville-sc-1.jpg'],
         ['ROOFLINE GLOW', 'WALKWAY MAGIC', 'ESTATE LIGHTING'])

showcase('SL_Showcase_Commercial',
         'NOW BOOKING OCTOBER', 'Storefronts That Sell', 'Commercial displays that pull crowds',
         [f'{SPR}/sp_13_olutions-residential-background-190.jpg',
          f'{SPR}/sp_10_s-commercial-background-BMW-Zentrum.jpg',
          f'{SPR}/sp_14_Spruce64-1-scaled-1.jpg'],
         ['RETAIL CENTERS', 'SHOWROOMS & CAMPUS', 'STOREFRONTS'])

showcase('SL_Showcase_Municipal',
         'NOW BOOKING OCTOBER', 'Towns That Twinkle', 'Municipal & community displays',
         [f'{SLR}/sl_14_hting-installation-municipalities-1.jpg',
          f'{SLR}/sl_15_hting-installation-municipalities-2.jpg',
          f'{SLR}/sl_16_hting-installation-municipalities-3.jpg'],
         ['TREE WRAPPING', 'MAIN STREET', 'PARKS & PLAZAS'])

showcase('SL_Showcase_HolidayNights',
         'THE SPRUCE TOUCH', 'Nights to Remember', 'Evenings your neighbors talk about',
         [f'{SLR}/sl_08_nstallation-service-greenville-sc-2.jpg',
          f'{SLR}/sl_12_ghting-installation-greenville-sc-3.jpg'],
         ['HOLIDAY NIGHTS', 'COMMUNITY GLOW'])

showcase('SL_Showcase_GrandTour',
         'SPRUCE LIGHTS & EVENTS', 'The Grand Tour', 'Residential • Commercial • Municipal',
         [f'{SLR}/sl_18_olumbia-myrtle-beach-sc-ashevill-nc.jpg',
          f'{SLR}/sl_01_spruce-christmas-lighting-2.jpg',
          f'{SPR}/sp_09_-solutions-commercial-background-14.jpg'],
         ['WHOLE NEIGHBORHOODS', 'PRO INSTALL CREWS', 'GRAND SPACES'])

print('ALL SHOWCASE VIDEOS DONE')
