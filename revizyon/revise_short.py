"""CRISPR Shorts revizyonu: kesme + dinamik zoom + SFX + döngü + loudness.

Kullanım: python3 revise_short.py <girdi.mp4> <çıktı.mp4>

Zaman damgaları orijinal videonun ses zarfı ve kare farkı analizinden
çıkarıldı (bkz. ANALIZ.md).
"""
import subprocess
import sys

import numpy as np
from PIL import Image

W, H, FPS, SR = 1080, 1920, 30, 48000

# Kesilecek bölüm: "Approved in the UK and the US at the end of 2023"
# Görüntü 24.467 -> 29.133, ses 24.467 -> 29.100 ("Sometimes" başlangıcı korunur).
CUT_V = (734, 874)            # kare indeksleri [başlangıç, bitiş)
CUT_A = (24.467, 29.100)
# Kesimden sonraki 7 karede eski "approved" ekranının geçiş izi var;
# bunlar senkron bozulmasın diye ilk temiz kare (881) ile dolduruluyor.
HOLD_TO = 881
END_V = 1008                  # 33.6 sn: başlık kartı 0.5 sn görünür, sonra döngü
ZOOM_CENTER = (540, 880)

# Sahne geçişleri (orijinal zaman), kare-farkı tepe noktaları
SCENES = [0.0, 3.0, 6.73, 10.1, 14.27, 17.03, 20.3, 29.133, 33.13]
PUNCHES = {                  # zaman: (başlangıç zoom, hedef zoom, süre)
    0.0: (1.12, 1.00, 0.55),    # hook: zoom-out reveal
    9.10: (1.13, 1.10, 0.95),   # "It doesn't." vurgu
    20.3: (1.09, 1.00, 0.35),   # "Break the switch"
    31.47: (1.10, 1.07, 2.10),  # "It's turning on the backup"
}


def smooth(x):
    x = min(max(x, 0.0), 1.0)
    return x * x * (3 - 2 * x)


def zoom_at(t):
    for p0 in sorted(PUNCHES, reverse=True):
        z0, z1, d = PUNCHES[p0]
        if p0 <= t < p0 + d:
            return z0 + (z1 - z0) * smooth((t - p0) / d)
        if p0 <= t and p0 in (9.10, 31.47):
            # vurgu sonrası sahne bitene kadar sabit kal
            nxt = min(s for s in SCENES if s > p0)
            if t < nxt:
                return z1
    # Her sahnede yavaş push-in (statik ekranları canlandırır)
    start = max(s for s in SCENES if s <= t)
    nxt = min([s for s in SCENES if s > t] + [35.1])
    return 1.0 + 0.06 * smooth((t - start) / (nxt - start))


def transform(img, z):
    if abs(z - 1.0) < 1e-4:
        return img
    cx, cy = ZOOM_CENTER
    # çıktı (x,y) -> girdi (cx + (x-cx)/z, cy + (y-cy)/z)
    a = 1 / z
    return img.transform((W, H), Image.AFFINE,
                         (a, 0, cx - cx * a, 0, a, cy - cy * a),
                         resample=Image.BICUBIC)


# ---------- SFX sentezi ----------
rng = np.random.default_rng(7)


def env(n, attack, release):
    e = np.ones(n)
    a, r = int(attack * SR), int(release * SR)
    e[:a] = np.linspace(0, 1, a)
    e[-r:] *= np.exp(-np.linspace(0, 6, r))
    return e


def whoosh(dur=0.32, lo=300, hi=3500):
    n = int(dur * SR)
    noise = rng.standard_normal(n)
    spec = np.fft.rfft(noise)
    f = np.fft.rfftfreq(n, 1 / SR)
    spec[(f < lo) | (f > hi)] = 0
    x = np.fft.irfft(spec, n)
    shape = np.sin(np.linspace(0, np.pi, n)) ** 2
    return x / np.abs(x).max() * shape


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


def chime(dur=0.9):
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * f * t) * g for f, g in
            ((880, 1), (1318.5, 0.6), (1760, 0.3)))
    rise = whoosh(0.35, 800, 6000) * 0.5
    x = x * env(n, 0.01, dur * 0.85)
    x[:len(rise)] += rise
    return x


# (çıktı zamanı, ses, seviye dBFS)
SFX = [
    (0.00, whoosh(0.25, 600, 6000), -30),
    (0.70, pop(1100), -27),             # T harfinin daire içine alınması
    (3.00, whoosh(), -31),
    (6.73, whoosh(), -31),
    (9.10, impact(), -21),              # "It doesn't."
    (10.10, whoosh(), -31),
    (14.27, pop(750), -29),             # kök hücre etiketi
    (17.03, whoosh(), -31),
    (20.30, impact(0.3), -24),          # "Break the switch"
    (24.467, whoosh(0.3, 400, 5000), -30),  # kesme noktası
    (25.13, pop(1300, 0.05), -29),      # kod bloğu
    (26.80, chime(), -27),              # "...the backup"
    (28.47, whoosh(0.3, 600, 6000), -31),   # başlığa dönüş / döngü
]


def build_audio(src, out_wav, total):
    raw = subprocess.run(['ffmpeg', '-loglevel', 'error', '-i', src, '-ac', '2',
                          '-ar', str(SR), '-f', 'f32le', '-'],
                         capture_output=True, check=True).stdout
    a = np.frombuffer(raw, np.float32).reshape(-1, 2).astype(np.float64)
    c0, c1 = int(CUT_A[0] * SR), int(CUT_A[1] * SR)
    fade = int(0.008 * SR)
    seg_a, seg_b = a[:c0].copy(), a[c1:].copy()
    seg_a[-fade:] *= np.linspace(1, 0, fade)[:, None]
    seg_b[:fade] *= np.linspace(0, 1, fade)[:, None]
    voice = np.concatenate([seg_a, seg_b])[:int(total * SR)]
    tail = int(0.04 * SR)
    voice[-tail:] *= np.linspace(1, 0, tail)[:, None]
    fx = np.zeros(len(voice))
    for t, snd, db in SFX:
        i = int(t * SR)
        snd = snd / np.abs(snd).max() * 10 ** (db / 20)
        j = min(len(fx), i + len(snd))
        fx[i:j] += snd[:j - i]
    mix = voice + fx[:, None]
    pcm = np.clip(mix, -1, 1).astype(np.float32).tobytes()
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'f32le', '-ar', str(SR),
                    '-ac', '2', '-i', '-', out_wav], input=pcm, check=True)


def main(src, dst):
    keep = [i for i in range(END_V) if not CUT_V[0] <= i < CUT_V[1]]
    total = len(keep) / FPS
    wav = dst + '.mix.wav'
    build_audio(src, wav, total)

    # loudness ölçümü (2 geçişli loudnorm, -14 LUFS / -1.5 dBTP)
    meas = subprocess.run(['ffmpeg', '-hide_banner', '-i', wav, '-af',
                           'loudnorm=I=-14:TP=-1.5:LRA=7:print_format=json',
                           '-f', 'null', '-'], capture_output=True, text=True).stderr
    import json
    m = json.loads(meas[meas.rindex('{'):meas.rindex('}') + 1])
    ln = ('loudnorm=I=-14:TP=-1.5:LRA=7:linear=true:'
          f"measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
          f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:"
          f"offset={m['target_offset']}")

    dec = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-i', src, '-f', 'rawvideo',
                            '-pix_fmt', 'rgb24', '-'], stdout=subprocess.PIPE)
    enc = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y',
                            '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}',
                            '-r', str(FPS), '-i', '-', '-i', wav,
                            '-af', ln + ',aresample=48000',
                            '-c:v', 'libx264', '-preset', 'slow', '-crf', '17',
                            '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k',
                            '-movflags', '+faststart', '-shortest', dst],
                           stdin=subprocess.PIPE)
    keep_set = set(keep)
    for i in range(END_V):
        buf = dec.stdout.read(W * H * 3)
        if not buf:
            break
        if i not in keep_set or CUT_V[1] <= i < HOLD_TO:
            continue
        img = Image.frombuffer('RGB', (W, H), buf)
        first = CUT_V[1] if i == HOLD_TO else i
        for k in range(first, i + 1):
            enc.stdin.write(transform(img, zoom_at(k / FPS)).tobytes())
    dec.stdout.close()
    dec.kill()
    enc.stdin.close()
    enc.wait()
    print(f'OK: {dst} ({total:.2f} sn)')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
