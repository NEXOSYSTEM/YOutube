"""Banda sonora de la intro de la lupa, 100 % sintetizada (numpy + ffmpeg de imageio). Sin samples ni descargas:
no hay licencias de terceros ni riesgo de Content ID.

Los momentos salen de la misma lógica que la animación (montaje/src/intro.jsx): se recalcula el recorrido de la
lupa y el fotograma exacto en que «encuentra» cada huella, continente y «¿?».
Salida: logo/intro-2026-11-18/intro-lupa-sonido.wav, intro-lupa-sonido.mp4 e intro-lupa-vertical-sonido.mp4
"""
import os
import json, math, re, subprocess, wave
import numpy as np
import imageio_ffmpeg

RAIZ = os.environ.get("ALUCINATE_RAIZ") or os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
OUT = f"{RAIZ}/logo/intro-2026-11-18"
FF = imageio_ffmpeg.get_ffmpeg_exe()
SR, FPS = 48000, 30
rng = np.random.default_rng(11)

# ---------- 1) Tiempos (copia fiel de intro.jsx) ----------
src = open(f"{RAIZ}/montaje/src/intro.jsx", encoding="utf-8").read()
T = {k: int(v) for k, v in re.findall(r"(\w+): (\d+)", re.search(r"const T = \{([^}]*)\}", src).group(1))}
SPIN = int(re.search(r"const SPIN = (\d+)", src).group(1))
HUELLAS = json.loads(re.search(r"const HUELLAS = (\[\[.*?\]\]);", src).group(1))
ORDEN = json.loads(re.search(r"const ORDEN = (\[.*?\]);", src).group(1))
DUDAS = [[float(a), float(b)] for a, b in re.findall(r'\["[¿?]+", (-?\d+), (-?\d+), \d+\]', src)]
M = json.load(open(f"{RAIZ}/montaje/src/data/mapa-intro.json"))
U = 280
CONT = [[v * U for v in M["continentes"][k]["c"]] for k in ORDEN]
MEX = [v * U for v in M["mexico"]]

def inout_cubic(t):
    return 4 * t ** 3 if t < 0.5 else 1 - (-2 * t + 2) ** 3 / 2

def interp(f, a, b):
    return min(1.0, max(0.0, (f - a) / (b - a)))

def recorrido(pts, p):
    n = len(pts) - 1
    k = min(n - 1, int(math.floor(p * n)))
    t = min(1.0, (p * n - k) / 0.72)
    e = inout_cubic(t)
    return [pts[k][0] + (pts[k + 1][0] - pts[k][0]) * e, pts[k][1] + (pts[k + 1][1] - pts[k][1]) * e]

def pos(f):
    hu = [[x, y] for x, y, _ in HUELLAS]
    if f < T["enLupa"]: return hu[0]
    if f < T["g1"]: return recorrido(hu, interp(f, T["enLupa"], T["g1"] - 4))
    if f < T["g1"] + SPIN: return hu[-1]
    mapa = [hu[-1], *CONT, MEX]
    if f < T["g2"]: return recorrido(mapa, interp(f, T["g1"] + SPIN, T["g2"] - 4))
    if f < T["g2"] + SPIN: return MEX
    return recorrido([MEX, *DUDAS], interp(f, T["g2"] + SPIN, T["fin"] - 4))

def encontrado(x, y, a, b):
    for k in range(a, b + 1):
        lx, ly = pos(k)
        if math.hypot(lx - x, ly - y) < 30:
            return k
    return None

ev_huellas = [encontrado(x, y, T["enLupa"], T["g1"]) for x, y, _ in HUELLAS]
ev_cont = [encontrado(x, y, T["g1"] + SPIN, T["g2"]) for x, y in CONT]
ev_pin = encontrado(*MEX, T["g1"] + SPIN, T["g2"])
ev_dudas = [encontrado(x, y, T["g2"] + SPIN, T["fin"]) for x, y in DUDAS]
ev_botes = [T["fin"] + round(0.55 * (T["quieto"] - T["fin"])), T["quieto"]]
golpe_logo = T["fin"] + 32
print("huellas", ev_huellas, "continentes", ev_cont, "pin", ev_pin, "dudas", ev_dudas, "botes", ev_botes)

DUR = T["total"] / FPS
N = int(DUR * SR) + SR // 2
mix = np.zeros((N, 2))

def add(sig, frame=None, t=None, gain=1.0, pan=0.0):
    i = int((t if t is not None else frame / FPS) * SR)
    if i >= N: return
    sig = sig[: N - i] * gain
    l, r = math.cos((pan + 1) * math.pi / 4), math.sin((pan + 1) * math.pi / 4)
    mix[i : i + len(sig), 0] += sig * l * 1.414
    mix[i : i + len(sig), 1] += sig * r * 1.414

def tt(d): return np.arange(int(d * SR)) / SR
def env(n, a=0.005, rel=None):
    t = np.arange(n) / SR
    e = np.minimum(t / a, 1)
    return e if rel is None else e * np.exp(-t / rel)

def lp(x, fc):  # paso bajo de un polo
    a = math.exp(-2 * math.pi * fc / SR); y = np.zeros_like(x); s = 0.0
    for i in range(len(x)): s = (1 - a) * x[i] + a * s; y[i] = s
    return y

def bp_sweep(x, f0, f1, q=3):
    n = len(x); y = np.zeros(n); y1 = y2 = x1 = x2 = 0.0
    fs = np.geomspace(f0, f1, n)
    for i in range(n):
        w = 2 * math.pi * fs[i] / SR; al = math.sin(w) / (2 * q); c = math.cos(w)
        v = (al * x[i] - al * x2 + 2 * c * y1 - (1 - al) * y2) / (1 + al)
        x2, x1 = x1, x[i]; y2, y1 = y1, v; y[i] = v
    return y

# ---------- 2) Sonidos ----------
def riser(d):
    t = tt(d); f = 120 * (8 ** (t / d))
    tone = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.25
    air = bp_sweep(rng.standard_normal(len(t)), 300, 5000, 2) * 0.5
    return (tone + air) * (t / d) ** 1.6

def pad_espacial(d):
    t = tt(d)
    x = sum(np.sin(2 * np.pi * f * t + p) * a for f, p, a in [(55, 0, 1), (82.4, 1, .6), (110, 2, .4), (164.8, 0.5, .2)])
    x *= 0.6 + 0.4 * np.sin(2 * np.pi * 0.3 * t)
    return x * np.minimum(t / 0.8, 1) * np.minimum((d - t) / 0.8, 1) * 0.35

def pisada(freq):
    n = int(0.18 * SR); t = np.arange(n) / SR
    body = np.sin(2 * np.pi * freq * t * (1 - 0.35 * t / 0.18)) * np.exp(-t * 28)
    tap = lp(rng.standard_normal(n), 1800) * np.exp(-t * 90) * 0.8
    return body * 0.8 + tap

def whoosh(d=0.42):
    n = int(d * SR); x = bp_sweep(rng.standard_normal(n), 250, 4200, 2.5)
    return x * np.sin(np.linspace(0, np.pi, n)) ** 2 * 1.6

def swish_click():
    n = int(0.16 * SR); t = np.arange(n) / SR
    click = np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 160) * 0.6
    sw = bp_sweep(rng.standard_normal(n), 1200, 6000, 4) * np.exp(-t * 25)
    return click + sw * 0.8

def tic():
    n = int(0.04 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * 3200 * t) * np.exp(-t * 180)

def campana(f0=1568, d=1.6, g=1.0):
    t = tt(d)
    parts = [(1, 1, 3), (2.76, .5, 5), (5.4, .25, 8), (8.9, .12, 11)]
    return sum(a * np.sin(2 * np.pi * f0 * k * t) * np.exp(-t * dec) for k, a, dec in parts) * env(len(t), 0.002) * g

def burbuja(f0):
    n = int(0.14 * SR); t = np.arange(n) / SR
    f = f0 * (1 + 2.2 * t / 0.14)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 30) * env(n, 0.003)

def succion(d=0.5):
    n = int(d * SR); t = np.arange(n) / SR
    air = bp_sweep(rng.standard_normal(n), 5000, 300, 3) * 1.2
    tone = np.sin(2 * np.pi * np.cumsum(900 * (0.25 ** (t / d))) / SR) * 0.35
    return (air + tone) * np.sin(np.linspace(0, np.pi, n)) ** 1.5

def golpecito():
    n = int(0.2 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * (140 - 60 * t / 0.2) * t) * np.exp(-t * 22) + lp(rng.standard_normal(n), 900) * np.exp(-t * 60) * 0.4

def brillo(d=0.7):
    t = tt(d); out = np.zeros(len(t))
    notas = [1046.5, 1318.5, 1568, 2093, 2637, 3136]
    for i, f in enumerate(notas):
        s = int(i * d / len(notas) * SR); seg = t[: len(t) - s]
        out[s:] += np.sin(2 * np.pi * f * seg) * np.exp(-seg * 9) * 0.35
    out += bp_sweep(rng.standard_normal(len(t)), 2000, 9000, 6) * (t / d) * 0.5
    return out

def golpe_final():
    n = int(1.8 * SR); t = np.arange(n) / SR
    boom = np.sin(2 * np.pi * (70 - 25 * np.minimum(t, .5)) * t) * np.exp(-t * 3.5) * 1.3
    knock = lp(rng.standard_normal(n), 600) * np.exp(-t * 35) * 0.7
    return boom + knock + campana(1318.5, 1.8, 0.55) + campana(1975.5, 1.8, 0.3)

def marimba(f, d=0.5, g=1.0):
    t = tt(d)
    x = np.sin(2 * np.pi * f * t) * np.exp(-t * 7) + 0.35 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t * 30) + 0.1 * np.sin(2 * np.pi * f * 9.9 * t) * np.exp(-t * 60)
    return x * env(len(t), 0.002) * g

# Base musical de intriga (marimba en La menor, 112 bpm en corcheas) que se apaga al final
def base_musical():
    bpm = 112; corchea = 60 / bpm / 2
    A = {"A3": 220, "C4": 261.6, "D4": 293.7, "E4": 329.6, "G4": 392, "A4": 440, "B3": 246.9, "F3": 174.6, "E3": 164.8}
    patron = ["A3", "E4", "C4", "E4", "A3", "E4", "D4", "E4", "F3", "C4", "A3", "C4", "E3", "B3", "G4", "B3"]
    bajos = [110, 110, 87.3, 82.4]
    out = np.zeros(N)
    t0 = T["fijo"] / FPS - 0.1
    fin = golpe_logo / FPS
    k = 0; t = t0
    while t < fin - 0.05:
        f = A[patron[k % len(patron)]]
        s = marimba(f, 0.5, 0.55 if k % 2 == 0 else 0.4)
        i = int(t * SR); out[i : i + len(s)] += s[: max(0, N - i)][: len(out) - i]
        if k % 4 == 0:
            b = marimba(bajos[(k // 4) % 4], 0.9, 0.5)
            out[i : i + len(b)] += b[: len(out) - i]
        k += 1; t += corchea
    # fade out suave al final
    tt_ = np.arange(N) / SR
    out *= np.clip((fin + 0.6 - tt_) / 0.8, 0, 1)
    return out

# ---------- 3) Mezcla ----------
add(pad_espacial(T["fijo"] / FPS + 1.2), t=0, gain=0.8)
add(riser(T["fijo"] / FPS), t=0, gain=0.7)
add(whoosh(0.5), frame=T["lupa"] - 2, gain=0.6, pan=-0.4)
for i, fr in enumerate(ev_huellas):
    if fr is not None: add(pisada(330 * (2 ** (i * 2 / 12))), frame=fr, gain=0.7, pan=-0.3 + 0.15 * i)
for g in (T["g1"], T["g2"]):
    add(whoosh(0.38), frame=g - 2, gain=0.75)
for i, fr in enumerate(ev_cont):
    if fr is not None: add(swish_click(), frame=fr, gain=0.6, pan=-0.3 + 0.2 * i)
if ev_pin is not None:
    for k in range(ev_pin - 22, ev_pin, 3): add(tic(), frame=k, gain=0.35)
    add(campana(1760, 1.2, 0.8), frame=ev_pin, gain=0.6)
for i, fr in enumerate(ev_dudas):
    if fr is not None:
        add(burbuja(520 + 140 * i), frame=fr, gain=0.7, pan=[-0.4, 0.4, 0][i % 3])
        add(burbuja(780 + 140 * i), frame=fr + 3, gain=0.4)
add(succion(0.55), frame=T["fin"], gain=0.8)
for b in ev_botes: add(golpecito(), frame=b, gain=0.7)
add(brillo(0.66), frame=T["fin"] + 12, gain=0.6)
add(golpe_final(), frame=golpe_logo, gain=0.9)
add(np.stack([base_musical()] * 1, 0)[0], t=0, gain=0.45)

# ---------- 4) Masterización: −14 LUFS, pico −1 dB ----------
mix = mix[: int(DUR * SR)]
mix /= np.abs(mix).max() + 1e-9
raw = f"{OUT}/_sonido_crudo.wav"
with wave.open(raw, "w") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 0.8 * 32767).astype(np.int16).tobytes())
medida = subprocess.run([FF, "-hide_banner", "-i", raw, "-af", "loudnorm=I=-14:TP=-1:LRA=9:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
js = json.loads(medida[medida.rindex("{"): medida.rindex("}") + 1])
filtro = (f"loudnorm=I=-14:TP=-1:LRA=9:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}"
          f":measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true,alimiter=limit=0.89:level=false")
wav = f"{OUT}/intro-lupa-sonido.wav"
subprocess.run([FF, "-y", "-loglevel", "error", "-i", raw, "-af", filtro, "-ar", "48000", "-c:a", "pcm_s16le", wav], check=True)
subprocess.run(["rm", "-f", raw])
# vídeo con la nueva mezcla (sustituye a los efectos anteriores)
subprocess.run([FF, "-y", "-loglevel", "error", "-i", f"{OUT}/intro-lupa.mp4", "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", f"{OUT}/intro-lupa-sonido.mp4"], check=True)
# vertical: el tramo final de la misma mezcla
ini = (T["fin"] - 6) / FPS
subprocess.run([FF, "-y", "-loglevel", "error", "-i", f"{OUT}/intro-lupa-vertical.mp4", "-ss", f"{ini:.3f}", "-i", wav, "-map", "0:v", "-map", "1:a",
                "-c:v", "copy", "-af", "afade=t=in:d=0.08", "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart",
                f"{OUT}/intro-lupa-vertical-sonido.mp4"], check=True)
for f in ["intro-lupa-sonido.wav", "intro-lupa-sonido.mp4", "intro-lupa-vertical-sonido.mp4"]:
    r = subprocess.run([FF, "-hide_banner", "-i", f"{OUT}/{f}", "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    I = re.findall(r"I:\s+(-?[\d.]+) LUFS", r)[-1]; P = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r)[-1]
    print(f, "→", I, "LUFS, pico", P, "dBTP")
