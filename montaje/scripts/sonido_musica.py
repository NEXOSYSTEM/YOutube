"""Música de fondo 100 % sintetizada (sin samples ni licencias): base documental de intriga.
- fondo-largo.wav: duración del vídeo largo (pads en La menor + pulso suave + marimba ocasional)
- fondo-short.wav: 45 s, algo más luminosa y con más pulso (para Shorts, muy baja)
Se exportan a −14 LUFS; el montaje las pone a ≈ −22 dB (largo) y ≈ −25 dB (Shorts) bajo la voz.
"""
import os
import json, subprocess, sys, wave
import numpy as np
import imageio_ffmpeg

RAIZ = os.environ.get("ALUCINATE_RAIZ") or os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = f"{RAIZ}/montaje/public/musica"
FF = imageio_ffmpeg.get_ffmpeg_exe()
SR = 48000
rng = np.random.default_rng(5)

def nota(n):  # n = semitonos desde La 220 Hz
    return 220.0 * 2 ** (n / 12)

def pad(f, d, gain):
    t = np.arange(int(d * SR), dtype=np.float32) / SR
    att, rel = min(2.0, d / 3), min(2.5, d / 3)
    env = np.minimum(t / att, 1) * np.minimum((d - t) / rel, 1)
    l = np.zeros_like(t); r = np.zeros_like(t)
    for h, a in [(1, 1), (2, 0.35), (3, 0.15), (4, 0.06)]:
        l += a * np.sin(2 * np.pi * f * h * 0.9985 * t)
        r += a * np.sin(2 * np.pi * f * h * 1.0015 * t + 0.7)
    lfo = 0.85 + 0.15 * np.sin(2 * np.pi * 0.15 * t)
    return np.stack([l, r], 1) * (env * lfo * gain)[:, None]

def marimba(f, gain, d=0.9):
    t = np.arange(int(d * SR), dtype=np.float32) / SR
    x = np.sin(2 * np.pi * f * t) * np.exp(-t * 6) + 0.3 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t * 28)
    x *= np.minimum(t / 0.003, 1) * gain
    return np.stack([x, x], 1)

def pulso(f, gain, d=0.6):
    t = np.arange(int(d * SR), dtype=np.float32) / SR
    x = np.sin(2 * np.pi * f * t * (1 - 0.2 * t)) * np.exp(-t * 7) * gain
    return np.stack([x, x], 1)

def mezcla(dur, brillo=False):
    N = int(dur * SR)
    m = np.zeros((N + SR * 4, 2), np.float32)
    def add(sig, t):
        i = int(t * SR); m[i:i + len(sig)] += sig[: len(m) - i]
    # progresión Am – F – Dm – E (acordes en semitonos desde La 220)
    prog = [[-12, 0, 3, 7], [-16, -4, 0, 3], [-19, -7, -2, 5], [-17, -5, -1, 2]]
    compas = 6.0 if brillo else 8.0
    t, k = 0.0, 0
    while t < dur:
        for n in prog[k % 4]:
            add(pad(nota(n), compas + 1.5, 0.11), t)
        # pulso suave en negras (como un latido de intriga)
        bpm = 96 if brillo else 80
        for b in range(int(compas * bpm / 60)):
            add(pulso(nota(prog[k % 4][0] - 12), 0.22 if b % 2 == 0 else 0.12), t + b * 60 / bpm)
        # marimba: arpegio en compases alternos (en los Shorts, siempre)
        if brillo or k % 2 == 1:
            arp = [prog[k % 4][1], prog[k % 4][2], prog[k % 4][3], prog[k % 4][2] + 12]
            paso = 60 / bpm / 2
            for j in range(int(compas / paso)):
                if rng.random() < (0.7 if brillo else 0.45):
                    add(marimba(nota(arp[j % 4] + 12), 0.1), t + j * paso)
        t += compas; k += 1
    m = m[:N]
    fade = np.minimum(np.arange(N) / (2 * SR), 1) * np.minimum((N - np.arange(N)) / (3 * SR), 1)
    return m * fade[:, None].astype(np.float32)

def exporta(m, nombre):
    m = m / (np.abs(m).max() + 1e-9) * 0.8
    raw = f"{OUT}/_{nombre}"
    with wave.open(raw, "w") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((m * 32767).astype(np.int16).tobytes())
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", raw, "-af", "loudnorm=I=-14:TP=-1.5:LRA=7", "-ar", "48000", "-c:a", "pcm_s16le", f"{OUT}/{nombre}"], check=True)
    subprocess.run(["rm", "-f", raw])
    print(nombre, round(len(m) / SR, 1), "s")

if __name__ == "__main__":
    import os
    os.makedirs(OUT, exist_ok=True)
    plan = json.load(open(f"{RAIZ}/montaje/src/data/plan.json"))
    exporta(mezcla(plan["largo"]["len"] / 30 + 1), "fondo-largo.wav")
    exporta(mezcla(45, brillo=True), "fondo-short.wav")
