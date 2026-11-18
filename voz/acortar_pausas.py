"""Acorta las pausas entre frases de la narración final SIN cambiar la velocidad de la voz (sigue a x1,25).
Recorta silencios del principio/fin y deja cada pausa interna larga en `--pausa` segundos (bajando hasta 0,05 s si
hace falta para llegar a `--objetivo` ppm). Apunta en duraciones.json los segundos recortados para que
montaje/scripts/comprobar.py siga verificando: final = crudo/1,25 − pausas recortadas.
Uso: acortar_pausas.py --salida audio/... [--objetivo 155] nombre ..."""
import argparse, json, wave
import numpy as np

RAIZ = "/Users/luis/Desktop/Youtube/Alucinateconelmundo"

def lee(p):
    with wave.open(p) as w:
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768, w.getframerate()

def escribe(p, a, sr):
    with wave.open(p, "w") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(sr); w.writeframes((np.clip(a, -1, 1) * 32767).astype(np.int16).tobytes())

def acorta(a, sr, pausa, umbral=0.012, minimo=0.12):
    fr = int(0.01 * sr); n = len(a) // fr
    rms = np.sqrt((a[: n * fr].reshape(n, fr) ** 2).mean(1))
    voz = rms > umbral
    idx = np.where(voz)[0]
    if not len(idx): return a
    trozos, i = [], idx[0]
    keep_ini = max(0, idx[0] - 4)  # 40 ms antes de la primera voz
    out = [a[keep_ini * fr: idx[0] * fr]]
    j = idx[0]
    while j < n:
        if voz[j]:
            k = j
            while k < n and voz[k]: k += 1
            out.append(a[j * fr: k * fr]); j = k
        else:
            k = j
            while k < n and not voz[k]: k += 1
            largo = (k - j) * 0.01
            if k >= n:  # silencio final: dejar 60 ms
                out.append(a[j * fr: j * fr + int(0.06 * sr)])
            elif largo > minimo:
                m = int(pausa * sr / 2)
                out.append(a[j * fr: j * fr + m]); out.append(a[k * fr - m: k * fr])
            else:
                out.append(a[j * fr: k * fr])
            j = k
    return np.concatenate(out)

ap = argparse.ArgumentParser(); ap.add_argument("--salida", required=True); ap.add_argument("--objetivo", type=float, default=155)
ap.add_argument("nombres", nargs="+"); a = ap.parse_args()
sal = f"{RAIZ}/{a.salida}"
dur = json.load(open(f"{sal}/duraciones.json"))
for nombre in a.nombres:
    p = f"{sal}/{nombre}.wav"
    orig, sr = lee(p)
    d = dur[nombre]; previo = d.get("pausas_recortadas_s", 0)
    for pausa in (0.10, 0.08, 0.065, 0.05):
        nuevo = acorta(orig, sr, pausa)
        ppm = d["palabras"] / (len(nuevo) / sr) * 60
        if ppm >= a.objetivo: break
    escribe(p, nuevo, sr)
    recortado = len(orig) / sr - len(nuevo) / sr
    d.update({"final_s": round(len(nuevo) / sr, 3), "ppm": round(ppm), "pausa_entre_frases_s": pausa,
              "pausas_recortadas_s": round(previo + recortado, 3)})
    print(f"{nombre}: {len(orig)/sr:.2f} s → {len(nuevo)/sr:.2f} s · {round(ppm)} ppm · pausa {pausa} s")
json.dump(dur, open(f"{sal}/duraciones.json", "w"), indent=1, ensure_ascii=False)
