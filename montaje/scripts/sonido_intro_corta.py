"""Sonido de la intro corta (3 s), con los mismos sintetizadores que la intro larga (sonido_intro.py).
Salida: logo/intro-2026-11-18/intro-lupa-corta.wav e intro-lupa-corta.mp4"""
import json, re, subprocess, wave
import numpy as np

RAIZ = "/Users/luis/Desktop/Youtube/Alucinateconelmundo"
src = open(f"{RAIZ}/montaje/scripts/sonido_intro.py", encoding="utf-8").read()
G = {"__name__": "sonido_lib"}
exec(src[: src.index("# ---------- 3) Mezcla")], G)  # solo tiempos + sintetizadores, sin mezclar
FF, SR, FPS, OUT = G["FF"], G["SR"], G["FPS"], G["OUT"]
intro = open(f"{RAIZ}/montaje/src/intro.jsx", encoding="utf-8").read()
TC = {k: int(v) for k, v in re.findall(r"(\w+): (\d+)", re.search(r"const TC = \{([^}]*)\}", intro).group(1))}

DUR = TC["total"] / FPS
N = int(DUR * SR) + SR // 2
mix = np.zeros((N, 2))
def add(sig, frame, gain=1.0):
    i = int(frame / FPS * SR)
    sig = sig[: N - i] * gain
    mix[i : i + len(sig), 0] += sig; mix[i : i + len(sig), 1] += sig

add(G["pad_espacial"](DUR), 0, 0.6)
add(G["riser"](TC["zoom"] / FPS + 0.1), 0, 0.6)
add(G["whoosh"](0.4), TC["lupa"] - 2, 0.6)
add(G["succion"](0.5), TC["enc"], 0.8)
botes = [TC["enc"] + round(0.55 * (TC["quieto"] - TC["enc"])), TC["quieto"]]
for b in botes: add(G["golpecito"](), b, 0.7)
add(G["brillo"](0.66), TC["enc"] + 12, 0.6)
add(G["golpe_final"](), TC["enc"] + 32, 0.9)
# pequeño motivo de marimba (las 4 notas del arranque de la base) que se apaga en el golpe
for i, (f, fr) in enumerate([(220, 2), (329.6, 8), (261.6, 14), (329.6, 20), (174.6, 26), (261.6, 32)]):
    add(G["marimba"](f, 0.5, 0.5), fr, 0.5)

mix = mix[: int(DUR * SR)]
mix /= np.abs(mix).max() + 1e-9
raw = f"{OUT}/_corta_crudo.wav"
with wave.open(raw, "w") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mix * 0.8 * 32767).astype(np.int16).tobytes())
med = subprocess.run([FF, "-hide_banner", "-i", raw, "-af", "loudnorm=I=-14:TP=-1:LRA=9:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
js = json.loads(med[med.rindex("{"): med.rindex("}") + 1])
filtro = (f"loudnorm=I=-14:TP=-1:LRA=9:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}"
          f":measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true,alimiter=limit=0.89:level=false")
wav = f"{OUT}/intro-lupa-corta.wav"
subprocess.run([FF, "-y", "-loglevel", "error", "-i", raw, "-af", filtro, "-ar", "48000", "-c:a", "pcm_s16le", wav], check=True)
subprocess.run(["rm", "-f", raw])
subprocess.run([FF, "-y", "-loglevel", "error", "-i", f"{OUT}/intro-lupa-corta-sin-sonido.mp4", "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                "-c:a", "aac", "-b:a", "256k", "-shortest", "-movflags", "+faststart", f"{OUT}/intro-lupa-corta.mp4"], check=True)
r = subprocess.run([FF, "-hide_banner", "-i", f"{OUT}/intro-lupa-corta.mp4", "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
print("intro-lupa-corta.mp4 →", re.findall(r"I:\s+(-?[\d.]+) LUFS", r)[-1], "LUFS, pico", re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r)[-1])
