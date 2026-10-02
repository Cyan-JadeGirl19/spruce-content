"""Spruce brand soundtracks — two distinct sonic identities.
SPRUCE LIGHTS  : warm music-box lullaby — celesta bells, 3/4 waltz, C major, magical.
SPRUCE SERVICES: clean crisp chime — bright plucks, 4/4, A minor, modern & professional.
Both gentle and twinkly; numpy DSP, soft-clip master, fades, stereo."""
import math, random, wave
import numpy as np

RATE = 44100

def _semis(base, st):
    return base * (2.0 ** (st / 12.0))

def _note(freq, dur, amp, partials, tau, att=0.004):
    n = int(dur * RATE)
    t = np.arange(n) / RATE
    env = np.exp(-t / tau) * np.minimum(1.0, t / att)
    out = np.zeros(n)
    for m, w in partials:
        out += np.sin(2 * np.pi * freq * m * t) * w
    out *= env
    peak = np.abs(out).max() or 1.0
    return out / peak * amp

def _pad(freqs, dur, amp, att=0.9, rel=1.2):
    n = int(dur * RATE)
    t = np.arange(n) / RATE
    env = np.minimum(1.0, t / att) * np.minimum(1.0, (dur - t) / rel)
    out = np.zeros(n)
    for f in freqs:
        for det in (0.9987, 1.0013):
            out += np.sin(2 * np.pi * f * det * t)
    out *= env
    peak = np.abs(out).max() or 1.0
    return out / peak * amp

def _echo(sig, level, time_s):
    d = int(time_s * RATE)
    out = sig.copy()
    rep = sig.copy()
    while level > 0.02 and d < len(sig):
        rep = np.concatenate([np.zeros(d), rep[:-d]]) if d < len(rep) else np.zeros(len(sig))
        out += rep * level
        level *= 0.45
    return out

def _add(busL, busR, sig, start, pan):
    s0 = int(start * RATE)
    j = min(len(busL), s0 + len(sig))
    if j <= s0:
        return
    seg = sig[: j - s0]
    busL[s0:j] += seg * (1 - pan)
    busR[s0:j] += seg * pan

def _lowpass(x, cutoff=4200):
    rc = 1.0 / (2 * 3.14159 * cutoff)
    dt = 1.0 / RATE
    al = dt / (rc + dt)
    y = np.empty_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc += al * (x[i] - acc)
        y[i] = acc
    return y

def _master(path, L, R, fade=1.6, gain=1.0, soft=False):
    if soft:
        L = _lowpass(L); R = _lowpass(R)
    n = len(L)
    peak = max(np.abs(L).max(), np.abs(R).max()) or 1.0
    g = (0.80 / peak) * gain
    t = np.arange(n) / RATE
    k = np.ones(n)
    k[:int(0.20 * RATE)] = np.linspace(0, 1, int(0.20 * RATE))
    k[-int(fade * RATE):] = np.linspace(1, 0, int(fade * RATE))
    L = np.tanh((L * g) * 1.35) / np.tanh(1.35) * k
    R = np.tanh((R * g) * 1.35) / np.tanh(1.35) * k
    inter = np.empty(2 * n, dtype=np.int16)
    inter[0::2] = (np.clip(L, -0.98, 0.98) * 32767).astype(np.int16)
    inter[1::2] = (np.clip(R, -0.98, 0.98) * 32767).astype(np.int16)
    with wave.open(path, 'w') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(RATE)
        w.writeframes(inter.tobytes())
    return path

def _shimmer(L, R, rnd, dur, dens=1.0, soft=False):
    if soft: dens *= 0.5
    t = 0.1
    while t < dur - 0.3:
        f = rnd.uniform(4200, 8200)
        _add(L, R, _note(f, 0.4, rnd.uniform(0.010, 0.030) * dens,
                         [(1, 1)], 0.10, att=0.001), t, rnd.uniform(0.12, 0.88))
        t += rnd.uniform(0.10, 0.26) / dens

# ==================================================================
# SPRUCE LIGHTS — "Warm Music Box Lullaby" (C major waltz, celesta)
# ==================================================================
BOX_P = [(1.0, 1.0), (2.0, 0.20), (2.756, 0.15), (5.404, 0.05)]
C4 = 261.6256
SL_CHORDS = [([0, 4, 7], 0), ([9, 12, 16], -12), ([5, 9, 12], 0), ([7, 11, 14], 0)]
SL_PHRASES = [
    [0, 4, 7, 12, 9, 7, 4, 2],
    [12, 9, 7, 4, 0, 2, 4, 7],
    [7, 9, 12, 16, 14, 12, 9, 7],
    [4, 7, 9, 12, 14, 12, 9, 4],
]

def sl_track(path, dur, seed=7, accents=None, density=1.0, fade=1.7, gain=0.55, soft=True):
    """Spruce Lights: magical music-box waltz in C."""
    rnd = random.Random(seed + 100)
    beat = 0.62; bar = 3 * beat
    n = int(dur * RATE)
    L = np.zeros(n); R = np.zeros(n)
    K = C4 * 2  # C5
    # soft pad, one chord per bar
    tcur, ci = 0.0, 0
    while tcur < dur - 0.5:
        ch, boct = SL_CHORDS[ci % 4]
        d = min(bar + 0.5, dur - tcur + 0.3)
        _add(L, R, _pad([_semis(C4, st - 12) for st in ch], d, 0.030 * density), tcur, 0.5)
        tcur += bar; ci += 1
    # waltz: bass on 1, triad plucks on 2 & 3
    nbars = int(dur / bar) + 1
    for b in range(nbars):
        tb = b * bar
        if tb > dur - 0.4: break
        ch, boct = SL_CHORDS[b % 4]
        root = _semis(C4, ch[0] - 12 + boct)
        _add(L, R, _note(root, 1.1, 0.16 * density, [(1, 1)], 0.5), tb, 0.42)
        for k in (1, 2):
            for st in ch:
                f = _semis(C4, st + boct)
                _add(L, R, _note(f, 0.8, 0.045 * density, BOX_P, 0.30), tb + k * beat + 0.012,
                     0.30 if st == ch[0] else 0.62)
    # melody: one pre-composed phrase per 2 bars, music-box lead (+octave shimmer)
    t = 0.30; pi = rnd.randrange(4); ni = 0
    while t < dur - 0.6:
        ph = SL_PHRASES[(pi) % 4]; pi += 1
        for k, st in enumerate(ph):
            if t > dur - 0.6: break
            f = _semis(K, st)
            amp = (0.30 if k % 3 == 0 else 0.22) * density
            sig = _note(f, 1.9, amp, BOX_P, 0.65)
            sig = _echo(sig, 0.24, beat * 1.5)
            _add(L, R, sig, t, 0.5 + 0.14 * math.sin(t * 0.9))
            if k == 0:  # octave sparkle on phrase starts
                _add(L, R, _note(f * 2, 1.4, 0.10 * density, BOX_P, 0.4), t + 0.05, 0.72)
            t += beat
        t += beat * rnd.choice([0, 0, 1])  # breath between phrases
    _shimmer(L, R, rnd, dur, 0.8 * density, soft=soft)
    # accents: music-box flourish (run up + low root)
    for (ta, fa) in (accents or []):
        run = [fa / 2, fa * 3 / 4, fa, fa * 1.25, fa * 1.5, fa * 2]
        for k, f in enumerate(run):
            _add(L, R, _note(f, 2.0, 0.26, BOX_P, 0.7), ta + k * 0.055, 0.5)
        _add(L, R, _note(fa / 4, 2.6, 0.20, [(1, 1)], 0.9), ta, 0.35)
    return _master(path, L, R, fade, gain=gain, soft=soft)

# ==================================================================
# SPRUCE SERVICES — "Clean Chime" (A minor, bright plucks, modern)
# ==================================================================
PLK_P = [(1.0, 1.0), (2.0, 0.28), (3.01, 0.08)]
A3 = 220.0
SP_CHORDS = [([0, 3, 7], 0), ([-4, 0, 3], 0), ([-7, -4, 0], 0), ([-2, 2, 5], 0)]  # Am F C G (rel A)
SP_PHRASES = [
    [0, 3, 7, 12, 10, 7, 5, 3],
    [12, 10, 7, 5, 3, 5, 7, 10],
    [7, 10, 12, 15, 12, 10, 7, 5],
    [5, 7, 10, 12, 15, 12, 10, 7],
]
SP_REST = [[1, 0, 1, 1, 0, 1, 0, 1], [1, 1, 0, 1, 1, 0, 1, 0],
           [1, 0, 1, 0, 1, 1, 0, 1], [1, 0, 0, 1, 1, 0, 1, 1]]

def sp_track(path, dur, seed=7, accents=None, density=1.0, fade=1.6, gain=0.50, soft=True):
    """Spruce Services: crisp modern chime in A minor — clean, confident, fresh."""
    rnd = random.Random(seed + 900)
    beat = 0.50; bar = 4 * beat
    n = int(dur * RATE)
    L = np.zeros(n); R = np.zeros(n)
    K = A3 * 2  # A4
    # airy pad
    tcur, ci = 0.0, 0
    while tcur < dur - 0.5:
        ch, _ = SP_CHORDS[ci % 4]
        d = min(bar + 0.4, dur - tcur + 0.3)
        _add(L, R, _pad([_semis(A3, st) for st in ch], d, 0.024 * density, att=0.7, rel=1.0), tcur, 0.5)
        tcur += bar; ci += 1
    # gentle pulse: sub root on 1 & 3, chord pluck on 2 & 4
    nbars = int(dur / bar) + 1
    for b in range(nbars):
        tb = b * bar
        if tb > dur - 0.4: break
        ch, _ = SP_CHORDS[b % 4]
        for k in (0, 2):
            _add(L, R, _note(_semis(A3, ch[0] - 12), 0.7, 0.13 * density, [(1, 1)], 0.30, att=0.006),
                 tb + k * beat, 0.45)
        for k in (1, 3):
            for j, st in enumerate(ch):
                f = _semis(A3, st + 12)
                _add(L, R, _note(f, 0.55, 0.040 * density, PLK_P, 0.16, att=0.002),
                     tb + k * beat + j * 0.014, 0.32 if j == 0 else 0.66)
    # melody: eighth-note motif with rests, ping-pong echo
    e8 = beat / 2
    t = 0.25; pi = rnd.randrange(4); ni = 0
    pattern = SP_REST[pi % 4]
    while t < dur - 0.5:
        st = SP_PHRASES[pi % 4][ni % 8]
        if pattern[ni % 8]:
            f = _semis(K, st)
            amp = (0.24 if ni % 4 == 0 else 0.17) * density
            sig = _note(f, 0.9, amp, PLK_P, 0.28, att=0.002)
            side = 0.30 if (ni // 4) % 2 == 0 else 0.70
            _add(L, R, _echo(sig, 0.30, beat), t, side)
        ni += 1
        t += e8
        if ni % 16 == 0:
            pi += 1; pattern = SP_REST[pi % 4]
            t += e8 * 2  # small breath every 2 bars
    _shimmer(L, R, rnd, dur, 0.55 * density, soft=soft)
    # accents: clean two-note chime (root + fifth) — crisp logo hit
    for (ta, fa) in (accents or []):
        _add(L, R, _note(fa, 1.8, 0.30, PLK_P, 0.5, att=0.002), ta, 0.42)
        _add(L, R, _note(fa * 1.5, 1.8, 0.22, PLK_P, 0.5, att=0.002), ta + 0.12, 0.62)
        _add(L, R, _note(fa / 2, 1.4, 0.16, [(1, 1)], 0.4), ta + 0.02, 0.45)
    return _master(path, L, R, fade, gain=gain, soft=soft)

# --- convenience: per-video density presets -------------------------
PRESETS = {'sting': 0.55, 'promo': 1.0, 'feed': 0.8, 'ba': 0.7}
