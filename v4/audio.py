"""v3 ses katmanı: orijinal anlatım + senkron SFX, -14 LUFS.

Kullanım: python3 audio.py <orijinal.mp4> <çıktı.wav> [müzik.mp3]

Anlatım düzeni (orijinal zaman):
  [0.15, 24.467]  -> konuşma ilk karede başlasın diye 0.15 sn kırpılır
  [29.10, 32.85]  -> "Approved in the UK and the US..." cümlesi çıkarılır
Toplam 28.5 sn; son 0.5 sn sessiz kalır ve video başa döner.
"""
import json
import subprocess
import sys

import numpy as np

SR, END = 48000, 28.5
SEGMENTS = [(0.15, 24.467), (29.10, 32.85)]
rng = np.random.default_rng(11)


def env(n, attack, release):
    e = np.ones(n)
    a, r = max(1, int(attack * SR)), max(1, int(release * SR))
    e[:a] = np.linspace(0, 1, a)
    e[-r:] *= np.exp(-np.linspace(0, 6, r))
    return e


def band_noise(n, lo, hi):
    spec = np.fft.rfft(rng.standard_normal(n))
    f = np.fft.rfftfreq(n, 1 / SR)
    spec[(f < lo) | (f > hi)] = 0
    x = np.fft.irfft(spec, n)
    return x / np.abs(x).max()


def whoosh(dur=0.3, lo=400, hi=5000):
    n = int(dur * SR)
    return band_noise(n, lo, hi) * np.sin(np.linspace(0, np.pi, n)) ** 2


def pop(freq=900, dur=0.07):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = freq * (1 + 0.6 * np.exp(-t * 60))
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, 0.002, dur * 0.9)


def impact(dur=0.45):
    n = int(dur * SR)
    t = np.arange(n) / SR
    body = np.sin(2 * np.pi * (55 + 60 * np.exp(-t * 25)) * t)
    click = rng.standard_normal(n) * np.exp(-t * 120)
    return (body * 0.9 + click * 0.25) * env(n, 0.002, dur * 0.95)


def scribble(dur=0.4):
    """Kalem/marker çizgisi: hızlı genlik modülasyonlu tiz gürültü."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    am = 0.55 + 0.45 * np.sin(2 * np.pi * 14 * t) ** 2
    return band_noise(n, 1500, 7000) * am * env(n, 0.02, dur * 0.4)


def snip():
    """Makas: iki kısa metalik tık."""
    x = np.zeros(int(0.12 * SR))
    for off, f in ((0, 3200), (0.055, 2600)):
        c = pop(f, 0.035) + band_noise(int(0.035 * SR), 3000, 9000) * env(int(0.035 * SR), 0.001, 0.03) * 0.6
        i = int(off * SR)
        x[i:i + len(c)] += c
    return x


def ticks(count, spacing=0.06):
    """Klavye tıkırtısı."""
    x = np.zeros(int((count * spacing + 0.05) * SR))
    for k in range(count):
        c = band_noise(int(0.018 * SR), 2000, 8000) * env(int(0.018 * SR), 0.001, 0.016)
        i = int((k * spacing + rng.uniform(-0.008, 0.008)) * SR)
        i = max(i, 0)
        x[i:i + len(c)] += c * rng.uniform(0.6, 1.0)
    return x


def chime(dur=0.9):
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * f * t) * g for f, g in ((880, 1), (1318.5, 0.6), (1760, 0.3)))
    return x * env(n, 0.01, dur * 0.85)


def rise(dur=1.3):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = 220 * 2 ** (t / dur * 1.5)
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.5 + band_noise(n, 500, 4000) * 0.25
    return tone * np.linspace(0, 1, n) ** 1.5 * env(n, 0.01, 0.12)


# (zaman, ses, seviye dBFS) — zamanlar index.html ile aynı zaman çizgisinde
SFX = [
    (0.00, whoosh(0.22, 800, 7000), -32),
    (1.33, impact(0.3), -27),          # "doesn't fix" vurgu
    (1.85, scribble(0.4), -30),        # T etrafına daire
    (2.817, whoosh(), -31),
    (4.62, pop(700, 0.06), -27),       # harf dönmesi
    (5.62, pop(1200), -28),            # HBB etiketi
    (6.55, whoosh(), -31),
    (7.62, snip(), -24),               # makas
    (7.98, pop(900), -27),             # A düşüyor
    (8.95, impact(), -20),             # "It doesn't."
    (8.95, scribble(0.25), -28),
    (9.917, whoosh(), -31),
    (10.0, pop(1300, 0.05), -29),      # Casgevy etiketi
    (12.52, ticks(6, 0.07), -30),      # BCL11A yazılıyor
    (13.12, snip(), -24),
    (13.22, impact(0.3), -25),         # anahtar kırılıyor
    (13.65, whoosh(), -31),
    (13.7, pop(800), -29), (14.72, pop(950), -29), (16.05, pop(1100), -29),
    (16.3, chime(0.6), -33),           # no donor needed
    (16.85, whoosh(), -31),
    (17.88, pop(1500, 0.04), -28),     # anahtar tık
    (19.45, pop(1000), -27),           # bebek
    (20.117, snip(), -24),
    (20.22, impact(0.3), -24),         # break the switch
    (21.82, rise(1.4), -31),           # hemoglobin yükseliyor
    (23.58, chime(), -28),             # cells stop sickling
    (24.317, whoosh(), -31),
    (25.25, scribble(0.3), -29),       # fix(bug) çiziliyor
    (26.05, pop(1600, 0.04), -30),     # böcek
    (26.68, ticks(16, 0.042), -31),    # backup.enable()
    (27.35, chime(), -27),             # backup
    (28.0, whoosh(0.3, 800, 7000), -31),   # başa dönüş
]


MUSIC_START = 218.0          # "Lightless Dawn" 3:38 - en dolgun, dengeli bölüm
MUSIC_LUFS = -27.0           # konuşma yokken müzik seviyesi
DUCK_DB = -7.0               # konuşma sırasında müzik ne kadar kısılsın


def load(src, start=0.0, dur=None):
    cmd = ['ffmpeg', '-loglevel', 'error', '-ss', str(start), '-i', src]
    if dur:
        cmd += ['-t', str(dur)]
    raw = subprocess.run(cmd + ['-ac', '2', '-ar', str(SR), '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)


def lufs(x):
    p = subprocess.run(['ffmpeg', '-hide_banner', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', '-af', 'ebur128',
                        '-f', 'null', '-'], input=x.astype(np.float32).tobytes(), capture_output=True).stderr.decode()
    return float(p[p.rindex('I:'):].split()[1])


def music_bed(path, voice):
    m = load(path, MUSIC_START, END)
    m = np.pad(m, ((0, max(0, int(END * SR) - len(m))), (0, 0)))[:int(END * SR)]
    m *= 10 ** ((MUSIC_LUFS - lufs(m)) / 20)
    # konuşma zarfına göre ducking (atak 60 ms, bırakma 350 ms)
    hop = int(0.01 * SR)
    v = np.abs(voice).max(1)
    n = len(v) // hop
    act = (v[:n * hop].reshape(n, hop).max(1) > 10 ** (-38 / 20)).astype(float)
    g = np.ones(n)
    cur = 0.0
    for i in range(n):
        tgt = act[i]
        cur += (tgt - cur) * (1 - np.exp(-1 / (6 if tgt > cur else 35)))
        g[i] = 10 ** (DUCK_DB * cur / 20)
    gain = np.repeat(g, hop)
    gain = np.pad(gain, (0, len(m) - len(gain)), mode='edge')
    m *= gain[:, None]
    fi, fo = int(0.05 * SR), int(0.45 * SR)
    m[:fi] *= np.linspace(0, 1, fi)[:, None]
    m[-fo:] *= np.linspace(1, 0, fo)[:, None] ** 1.5
    return m


def main(src, dst, music=None):
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', src, '-ac', '2', '-ar', str(SR),
                          '-f', 'f32le', '-'], capture_output=True, check=True).stdout
    a = np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)
    fade = int(0.008 * SR)
    parts = []
    for s, e in SEGMENTS:
        seg = a[int(s * SR):int(e * SR)].copy()
        seg[:fade] *= np.linspace(0, 1, fade)[:, None]
        seg[-fade:] *= np.linspace(1, 0, fade)[:, None]
        parts.append(seg)
    voice = np.concatenate(parts)
    total = int(END * SR)
    mix = np.zeros((total, 2))
    mix[:min(total, len(voice))] = voice[:total]
    if music:
        mix += music_bed(music, mix.copy())
    for t, snd, db in SFX:
        i = int(t * SR)
        snd = snd / np.abs(snd).max() * 10 ** (db / 20)
        j = min(total, i + len(snd))
        mix[i:j] += snd[:j - i, None]
    tmp = dst + '.raw.wav'
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'f32le', '-ar', str(SR), '-ac', '2', '-i', '-', tmp],
                   input=np.clip(mix, -1, 1).astype(np.float32).tobytes(), check=True)
    meas = subprocess.run(['ffmpeg', '-hide_banner', '-i', tmp, '-af',
                           'loudnorm=I=-14:TP=-2.5:LRA=7:print_format=json', '-f', 'null', '-'],
                          capture_output=True, text=True).stderr
    m = json.loads(meas[meas.rindex('{'):meas.rindex('}') + 1])
    ln = ('loudnorm=I=-14:TP=-2.5:LRA=7:linear=true:'
          f"measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}:"
          f"measured_thresh={m['input_thresh']}:offset={m['target_offset']}")
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', tmp, '-af', ln + ',aresample=48000',
                    '-t', str(END), dst], check=True)
    subprocess.run(['rm', '-f', tmp])
    print('OK', dst)


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else None)
