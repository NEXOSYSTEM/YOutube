"""Mezcla la banda sonora del largo directamente desde plan.json (sin pasar por Chrome): narración, intro, música y efectos.
Mismos volúmenes que la composición de Remotion. Salida: WAV 48 kHz estéreo. Uso: mezcla_audio.py <clave-plan> salida.wav"""
import json, subprocess, sys, wave
import numpy as np, imageio_ffmpeg
RAIZ = "/Users/luis/Desktop/Youtube/Alucinateconelmundo"; PUB = f"{RAIZ}/montaje/public"; FF = imageio_ffmpeg.get_ffmpeg_exe()
SR, FPS = 48000, 30
clave, out = sys.argv[1], sys.argv[2]
PL = json.load(open(f"{RAIZ}/montaje/src/data/plan.json")); plan = PL[clave]; FPS = PL.get("fps", 30)
N = int(plan["len"] / FPS * SR) + SR
mix = np.zeros((N, 2), np.float32)
def carga(p):
    raw = subprocess.run([FF, "-loglevel", "error", "-i", p, "-f", "f32le", "-ac", "2", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2)
cache = {}
def pon(path, frame, vol=1.0, max_frames=None):
    if path not in cache: cache[path] = carga(path)
    a = cache[path]
    if max_frames is not None: a = a[: int(max_frames / FPS * SR)]
    i = int(frame / FPS * SR); a = a[: max(0, N - i)]
    mix[i:i + len(a)] += a * vol
intro = None
for b in plan["blocks"]:
    if b.get("video"):
        pon(f"{PUB}/{b['video']}", b["from"]); intro = b
    else:
        pon(f"{PUB}/{b['audio']}", b["from"], 1.0, b["audioLen"])
for s in plan["sfx"]:
    pon(f"{PUB}/sfx/{s['s']}.wav", max(0, s["f"]), s["v"], 75)
# música de fondo (tema.musica.volumen = 0.08), a cero durante la intro con fundidos de 0,5 s
m = carga(f"{PUB}/musica/fondo-largo.wav")[:N]
env = np.full(len(m), 0.08, np.float32)
if intro:
    a, z = intro["from"] / FPS, (intro["from"] + intro["len"]) / FPS
    t = np.arange(len(m)) / SR
    k = np.clip(np.minimum((a - t) / 0.5, (t - z) / 0.5), 0, 1)
    k[(t >= a) & (t <= z)] = 0
    env *= k
mix[:len(m)] += m * env[:, None]
mix = mix[: int(plan["len"] / FPS * SR)]
with wave.open(out, "w") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(mix, -1, 1) * 32767).astype(np.int16).tobytes())
print("mezcla", round(len(mix) / SR, 2), "s")
