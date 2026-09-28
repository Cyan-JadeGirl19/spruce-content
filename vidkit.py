"""SPRUCE MOTION KIT — branded MP4 motion graphics rendered frame-by-frame
with PIL + piped to ffmpeg (h264). 1080x1920 (reels/stories) & 1080x1080 (feed)."""
import math, os, subprocess, wave, array
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageEnhance
from spruce_kit import *

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
def encode(frames_iter, size, path, fps=FPS, audio_wav=None, crf=21):
    w, h = size
    cmd = [FF, '-y', '-f', 'rawvideo', '-vcodec', 'rawvideo',
           '-s', f'{w}x{h}', '-pix_fmt', 'rgb24', '-r', str(fps), '-i', '-']
    if audio_wav:
        cmd += ['-i', audio_wav, '-c:a', 'aac', '-b:a', '160k', '-shortest']
    cmd += ['-vcodec', 'libx264', '-preset', 'medium', '-crf', str(crf),
            '-pix_fmt', 'yuv420p', '-movflags', '+faststart', path]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE,
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    for im in frames_iter:
        p.stdin.write(im.convert('RGB').tobytes())
    p.stdin.close(); p.wait()
    return path

# ---------------------------------------------------------------- audio: soft chimes
def chime_wav(path, events, dur, rate=44100):
    """events: list of (t, freq, dur, amp) — gentle bell tones + soft pad"""
    n = int(dur * rate)
    buf = [0.0] * n
    for (t, f, d, a) in events:
        s0 = int(t * rate); s1 = min(n, s0 + int(d * rate))
        for i in range(s0, s1):
            x = (i - s0) / rate
            env = math.exp(-2.6 * x) * min(1, x * 220)
            v = (math.sin(2*math.pi*f*x) * 0.62 +
                 math.sin(2*math.pi*f*2*x) * 0.22 +
                 math.sin(2*math.pi*f*3.01*x) * 0.08)
            buf[i] += v * env * a
    # normalize & fade out tail
    m = max(1e-6, max(abs(v) for v in buf))
    fade = int(rate * 1.2)
    out = array.array('h')
    for i, v in enumerate(buf):
        g = 0.72 * v / m
        if i > n - fade: g *= (n - i) / fade
        out.append(int(max(-1, min(1, g)) * 32767))
    with wave.open(path, 'w') as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(rate)
        w.writeframes(out.tobytes())
    return path

def twinkle_events(times, base=523.25, amps=None):
    """C-major sparkle arpeggios at given times"""
    scale = [base, base*1.25, base*1.5, base*2, base*2.5, base*2*1.25]
    ev = []
    for k, t in enumerate(times):
        f = scale[k % len(scale)]
        ev.append((t, f, 1.6, (amps[k] if amps else 0.5)))
        ev.append((t + 0.06, f*1.5, 1.2, 0.18))
    return ev

# ---------------------------------------------------------------- pieces
def kb_frame(bg_path, size, t, z0=1.08, z1=1.22, pan=(0, 0), brighten=1.0):
    """ken-burns cover frame"""
    W, H = size
    im = bg_photo(bg_path, W, H, brighten=brighten, sat=1.05)
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

def slide_fade(base, layer, t, a, b, dy=60, dx=0):
    """paste layer with slide+fade between times a..b"""
    e = ease(seg(t, a, b))
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
