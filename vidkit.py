"""SPRUCE MOTION KIT — branded MP4 motion graphics rendered frame-by-frame
with PIL + piped to ffmpeg (h264). 1080x1920 (reels/stories) & 1080x1080 (feed)."""
import math, os, subprocess, wave, array
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageEnhance
from spruce_kit import *
import spruce_kit

FPS = 30
FF = "/home/user/.local/bin/ffmpeg"

# ---------------------------------------------------------------- easing
def ease(t):        return 1 - (1 - t) ** 3          # easeOutCubic
def easeio(t):      return t*t*(3-2*t)               # smoothstep
def backout(t, s=1.6):
    t -= 1; return t*t*((s+1)*t + s) + 1
def clamp01(x):     return max(0.0, min(1.0, x))
def seg(t, a, b):   return clamp01((t - a) / (b - a))

# ---------------------------------------------------------------- encoder
def encode(frames_iter, size, path, fps=FPS, audio_wav=None, crf=21, chip_brand=None):
    w, h = size
    cmd = [FF, '-y', '-f', 'rawvideo', '-vcodec', 'rawvideo',
           '-s', f'{w}x{h}', '-pix_fmt', 'rgb24', '-r', str(fps), '-i', '-']
    if audio_wav:
        cmd += ['-i', audio_wav, '-c:a', 'aac', '-b:a', '160k', '-shortest']
    cmd += ['-vcodec', 'libx264', '-preset', 'medium', '-crf', str(crf),
            '-pix_fmt', 'yuv420p', '-movflags', '+faststart', path]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    chip = brand_chip_layer(size, chip_brand) if chip_brand is not None else None
    for im in frames_iter:
        im = im.convert('RGBA')
        if chip is not None:
            im.alpha_composite(chip)
        p.stdin.write(im.convert('RGB').tobytes())
    p.stdin.close(); p.wait()
    return path

# ---------------------------------------------------------------- brand chip
def brand_chip_layer(size, brand):
    """top-left category pill, same geometry as the statics"""
    W, H = size
    label, bg, fg = spruce_kit.BRAND_CHIP[brand["key"]]
    bg, fg = tuple(bg[:3]), tuple(fg[:3])
    layer = Image.new('RGBA', size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    f = F(27, "ExtraBold")
    tw = d.textlength(label, font=f)
    d.rounded_rectangle([56, 56, 56 + tw + 52, 116], 30, fill=bg + (255,))
    d.text((82 + tw / 2, 84), label, font=f, fill=fg, anchor='mm')
    return layer

# ---------------------------------------------------------------- pieces
def kb_frame(bg_path, size, t, z0=1.08, z1=1.22, pan=(0, 0), brighten=1.0, grade=0.0):
    """ken-burns cover frame, optional cinematic grade"""
    W, H = size
    im = bg_photo(bg_path, W, H, brighten=brighten, sat=1.05)
    if grade:
        im = cinema(im, strength=grade)
    z = z0 + (z1 - z0) * easeio(t)
    zw, zh = int(W * z), int(H * z)
    im = im.resize((zw, zh), Image.LANCZOS)
    cx = zw/2 + pan[0] * (zw - W) / 2 * (t - .5)
    cy = zh/2 + pan[1] * (zh - H) / 2 * (t - .5)
    x0 = int(max(0, min(zw - W, cx - W/2))); y0 = int(max(0, min(zh - H, cy - H/2)))
    return im.crop((x0, y0, x0 + W, y0 + H))

def text_layer(size, text, weight, px, color=CREAM, maxw_frac=0.84, lh=1.14, shadow=True, y_center=None):
    """pre-render centered wrapped text onto a transparent layer; returns RGBA + height"""
    W, H = size
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    f = F(px, weight)
    lines = wrap_text(text, f, int(W * maxw_frac), d)
    th = len(lines) * px * lh
    y = ((H - th) / 2 if y_center is None else y_center - th / 2) + px * 0.1
    for ln in lines:
        w = d.textlength(ln, font=f)
        if shadow:
            sh = Image.new('RGBA', (W, H), (0,0,0,0))
            ImageDraw.Draw(sh).text(((W - w)/2 + 3, y + 4), ln, font=f, fill=(0, 10, 14, 190))
            layer.alpha_composite(sh.filter(ImageFilter.GaussianBlur(6)))
        d.text(((W - w)/2, y), ln, font=f, fill=color)
        y += px * lh
    return layer, th

def slide_fade(base, layer, t, a, b, dy=60, dx=0, out=None):
    """slide+fade in at a..b; optional fade-out out=(t0,t1,dy)"""
    e = ease(seg(t, a, b))
    if out:
        o = 1 - ease(seg(t, out[0], out[1]))
        e = e * o
        if e <= 0: return base
        dy = dy + out[2] * (1 - o)
    if e <= 0: return base
    tmp = layer.copy()
    alpha = tmp.getchannel('A').point(lambda v: int(v * e))
    tmp.putalpha(alpha)
    base.alpha_composite(tmp, (int(dx * (1 - e)), int(dy * (1 - e))))
    return base

def wipe(base_a, base_b, x):
    """horizontal wipe: b over a up to x"""
    x = int(max(0, min(base_a.width, x)))
    if x <= 0: return base_a
    base_a.paste(base_b.crop((0, 0, x, base_a.height)), (0, 0))
    return base_a

def brand_footer_layer(size, brand):
    W, H = size
    layer = Image.new('RGBA', (W, H), (0,0,0,0))
    d = ImageDraw.Draw(layer)
    hh = 132 if H > 1200 else 112
    for i in range(hh):
        a = int(215 * (i / hh) ** 0.5)
        d.line([(0, H - hh + i), (W, H - hh + i)], fill=(0, 24, 30, min(a, 235)))
    d.text((W/2, H - hh*0.40), f"{brand['phone']}   •   {brand['site']}",
           font=F(32 if H > 1200 else 28, 'SemiBold'), fill=CREAM, anchor='mm')
    d.text((W/2, H - hh*0.76), brand['handle'],
           font=F(24 if H > 1200 else 21, 'Regular'), fill=CYAN, anchor='mm')
    return layer

def sweep_logo(logo, t, period=1.4, phase=0.0):
    """moving diagonal light sweep through logo alpha"""
    lw, lh = logo.size
    band_w = int(lw * 0.35)
    band = Image.new('L', (lw, lh), 0)
    bd = ImageDraw.Draw(band)
    prog = ((t / period) + phase) % 1.0
    cx = int((lw + band_w) * prog * 1.4 - band_w)
    for i in range(band_w):
        a = int(150 * (1 - abs(i - band_w/2) / (band_w/2)) ** 1.5)
        bd.line([(cx + i, 0), (cx + i, lh)], fill=a)
    white = Image.new('RGBA', (lw, lh), (255, 255, 255, 0))
    m = ImageChops.multiply(band, logo.getchannel('A'))
    white.putalpha(m)
    out = logo.copy()
    out.alpha_composite(white)
    return out

def sparkle_field_layer(size, seed, n=14, ymax_frac=1.0, colors=None):
    """prebuild sparkles with per-sparkle (x, y, r, phase, color)"""
    import random
    rnd = random.Random(seed)
    W, H = size
    sp = []
    for _ in range(n):
        sp.append((rnd.randint(40, W-40), rnd.randint(30, int(H*ymax_frac)),
                   rnd.randint(10, 30), rnd.random()*2*math.pi,
                   (colors or [CYAN, LIME, CREAM])[rnd.randint(0, 2)]))
    return sp

def draw_sparkle_field(base, sp, t, global_alpha=1.0):
    d = ImageDraw.Draw(base)
    for (x, y, r, ph, c) in sp:
        tw = (0.55 + 0.45 * math.sin(t*3.1 + ph)) * global_alpha
        if tw <= 0.03: continue
        sparkle(d, x, y, r * (0.8 + 0.25*tw), c[:3] + (int(200*tw),), ratio=0.42, spread=0.18)
    return base

def label_chip(img, text, cx, cy, fill, fg=WHITE):
    d = ImageDraw.Draw(img)
    f = F(38, 'ExtraBold')
    tw = d.textlength(text, font=f)
    box = [cx - tw/2 - 30, cy - 36, cx + tw/2 + 30, cy + 36]
    sh = Image.new('RGBA', img.size, (0,0,0,0))
    ImageDraw.Draw(sh).rounded_rectangle([box[0]+3, box[1]+7, box[2]+3, box[3]+7], 36, fill=(0,0,0,120))
    img.alpha_composite(sh.filter(ImageFilter.GaussianBlur(7)))
    pill(d, box, fill)
    d.text((cx, cy - 2), text, font=f, fill=fg, anchor='mm')
    return img

# ---------------------------------------------------------------- audio v2: twinkle soundtrack (stereo)
def _bell(freq, dur, amp, rate=44100):
    """music-box bell: inharmonic partials, exponential decay, soft attack"""
    n = int(dur * rate)
    out = [0.0] * n
    partials = [(1.0, 1.0), (2.756, 0.42), (5.404, 0.16), (8.93, 0.05)]
    tau = dur / 4.2
    for (m, w) in partials:
        f = freq * m
        for i in range(n):
            x = i / rate
            env = math.exp(-x / tau) * min(1.0, x / 0.004)
            out[i] += math.sin(2 * math.pi * f * x) * env * w
    m = max(abs(v) for v in out) or 1.0
    return [v / m * amp for v in out]

def _pad(freqs, dur, amp, rate=44100, att=1.1, rel=1.4):
    """warm slow pad: detuned sine pairs per note"""
    n = int(dur * rate)
    out = [0.0] * n
    for f in freqs:
        for det in (0.9985, 1.0015):
            ph = 0.0
            for i in range(n):
                x = i / rate
                env = min(1.0, x / att) * min(1.0, (dur - x) / rel)
                out[i] += math.sin(2 * math.pi * f * det * x) * env
    m = max(abs(v) for v in out) or 1.0
    return [v / m * amp for v in out]

def twinkle_wav(path, dur, key=523.25, seed=7, accents=None, fade=1.6, rate=44100):
    """Gentle twinkling music-box soundtrack: warm pad + bell arpeggios + shimmer dust."""
    import random
    rnd = random.Random(seed)
    n = int(dur * rate)
    L = [0.0] * n; R = [0.0] * n
    def mix(buf, sig, start, pan=0.5):
        s0 = int(start * rate)
        for i, v in enumerate(sig):
            j = s0 + i
            if j >= n: break
            buf[int(j + 0)] = buf[j]  # placeholder no-op (keeps shape clear)
    def add(sig, start, pan):
        s0 = int(start * rate)
        for i, v in enumerate(sig):
            j = s0 + i
            if 0 <= j < n:
                L[j] += v * (1 - pan)
                R[j] += v * pan
    # --- chord pad progression I–vi–IV–V (loop), one chord per 4s
    root = key
    chords = [
        [root, root*1.25, root*1.5, root*2.25],          # I add9-ish
        [root*0.75, root*1.1875, root*1.25*1.0, root*1.875],
        [root*0.8333*1.2, root*1.0416*1.2, root*1.25*1.2, root*1.875],
        [root*0.9375*1.2, root*1.1718*1.2, root*1.2483*1.2, root*1.875*1.0],
    ]
    tcur = 0.0; ci = 0
    while tcur < dur:
        d = min(4.0, dur - tcur + 0.6)
        if d < 1.0: break
        add(_pad([f/2 for f in chords[ci % 4]], d, 0.045, rate), max(0, tcur), 0.5)
        tcur += 4.0; ci += 1
    # --- pentatonic twinkles: gentle arpeggio with rests
    pent = [1.0, 1.125, 1.25, 1.5, 1.6875, 2.0, 2.25, 2.5, 3.0]
    t = 0.35
    while t < dur - 0.5:
        f = key * rnd.choice(pent) * rnd.choice([1, 1, 1, 2])
        d = rnd.uniform(1.4, 2.4)
        add(_bell(f, d, rnd.uniform(0.16, 0.30), rate), t, rnd.uniform(0.25, 0.75))
        t += rnd.choice([0.42, 0.5, 0.6, 0.75, 1.0])
        if rnd.random() < 0.14: t += 0.5   # breath
    # --- shimmer dust: tiny high pings
    t = 0.0
    while t < dur - 0.2:
        f = rnd.uniform(4200, 8600)
        add(_bell(f, 0.35, rnd.uniform(0.015, 0.045), rate), t, rnd.uniform(0.15, 0.85))
        t += rnd.uniform(0.09, 0.22)
    # --- accents (logo hits / CTA)
    for (ta, fa) in (accents or []):
        add(_bell(fa, 2.6, 0.42, rate), ta, 0.5)
        add(_bell(fa*1.5, 2.2, 0.20, rate), ta + 0.07, 0.62)
        add(_bell(fa*2, 1.8, 0.12, rate), ta + 0.14, 0.4)
    # --- master: soft-clip + fade out
    fadeN = int(fade * rate)
    peak = max(max(abs(v) for v in L), max(abs(v) for v in R)) or 1.0
    g = 0.82 / peak
    inter = array.array('h')
    for i in range(n):
        k = 1.0
        if i > n - fadeN: k = (n - i) / fadeN
        if i < int(0.25*rate): k *= i / (0.25*rate)
        lv = max(-0.98, min(0.98, L[i] * g)) * k
        rv = max(-0.98, min(0.98, R[i] * g)) * k
        # tanh soft clip for warmth
        lv = math.tanh(lv * 1.4) / math.tanh(1.4)
        rv = math.tanh(rv * 1.4) / math.tanh(1.4)
        inter.append(int(lv * 32767)); inter.append(int(rv * 32767))
    with wave.open(path, 'w') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(rate)
        w.writeframes(inter.tobytes())
    return path
