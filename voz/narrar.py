"""Narración del canal con Qwen3-TTS (mlx-audio), carga el modelo UNA vez para todos los textos.

Regla del canal: la voz final va SIEMPRE a x1,25 real sobre la voz cruda (atempo=1.25, una sola vez).
El modelo no habla siempre al mismo ritmo en cada toma, así que se generan varias tomas y se queda
la más fluida (más palabras/minuto) que pase los controles (sin silencios largos ni atropellos).
Cada resultado se apunta en <salida>/duraciones.json (crudo, final, palabras, ppm) para que
montaje/scripts/comprobar.py verifique en cada render que final = crudo / 1,25.

Uso:
  voz/.venv/bin/python voz/narrar.py --textos guiones/.../textos-voz --salida audio/... [--tomas 3] [--min-ppm 160] [nombre ...]
"""
import argparse, json, os, subprocess, time, wave
import numpy as np

RAIZ = "/Users/luis/Desktop/Youtube/Alucinateconelmundo"
os.environ["HF_HOME"] = f"{RAIZ}/voz/modelos"
MODELO = "mlx-community/Qwen3-TTS-12Hz-1.7B-CustomVoice-8bit"
VOZ = "ryan"
INSTR = "Speak Spanish with a neutral accent from Spain (standard Castilian). Neutral, clear narrator tone, no exaggerated emotion. Fairly fast, fluid pace."
ATEMPO = 1.25


def lee(p):
    with wave.open(p) as w:
        sr = w.getframerate()
        a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    return a, sr


def analiza(p):
    a, sr = lee(p)
    fr = int(0.05 * sr); n = len(a) // fr
    rms = np.sqrt((a[: n * fr].reshape(n, fr) ** 2).mean(1)) if n else np.array([0])
    sil = rms < 0.01; voz = np.where(~sil)[0]; best = cur = 0
    if len(voz):
        for s in sil[voz[0]: voz[-1] + 1]:
            cur = cur + 1 if s else 0; best = max(best, cur)
    return len(a) / sr, best * 0.05, float(np.abs(a).max())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--textos", required=True); ap.add_argument("--salida", required=True)
    ap.add_argument("--tomas", type=int, default=3); ap.add_argument("--min-ppm", type=float, default=160)
    ap.add_argument("nombres", nargs="*")
    a = ap.parse_args()
    textos = a.textos if a.textos.startswith("/") else f"{RAIZ}/{a.textos}"
    salida = a.salida if a.salida.startswith("/") else f"{RAIZ}/{a.salida}"
    raw_dir = f"{salida}/_raw"; os.makedirs(raw_dir, exist_ok=True)
    import imageio_ffmpeg
    from mlx_audio.tts.utils import load_model
    from mlx_audio.tts.generate import generate_audio
    FF = imageio_ffmpeg.get_ffmpeg_exe()
    model = load_model(model_path=MODELO)
    dpath = f"{salida}/duraciones.json"
    dur = json.load(open(dpath)) if os.path.exists(dpath) else {}
    nombres = a.nombres or sorted(f[:-4] for f in os.listdir(textos) if f.endswith(".txt"))
    for nombre in nombres:
        texto = open(f"{textos}/{nombre}.txt", encoding="utf-8").read().strip()
        palabras = len(texto.split())
        mejor = None
        for toma in range(1, a.tomas + 1):
            t0 = time.time()
            generate_audio(text=texto, model=model, voice=VOZ, lang_code="spanish", instruct=INSTR,
                           file_prefix=f"{raw_dir}/{nombre}_t{toma}", join_audio=True, verbose=False)
            raw = f"{raw_dir}/{nombre}_t{toma}.wav"
            fin = f"{raw_dir}/{nombre}_t{toma}_x125.wav"
            subprocess.run([FF, "-y", "-loglevel", "error", "-i", raw, "-filter:a", f"atempo={ATEMPO}", "-ar", "24000", "-ac", "1", "-c:a", "pcm_s16le", fin], check=True)
            rd, _, _ = analiza(raw); fd, sil, pico = analiza(fin)
            ppm = palabras / fd * 60
            ok = 130 <= ppm <= 250 and sil < 1.5 and pico > 0.05
            print(json.dumps({"nombre": nombre, "toma": toma, "crudo": round(rd, 2), "final": round(fd, 2), "ppm": round(ppm), "silencio": sil, "ok": ok, "gen_s": round(time.time() - t0, 1)}), flush=True)
            if ok and (mejor is None or ppm > mejor["ppm"]):
                mejor = {"toma": toma, "raw": raw, "fin": fin, "crudo": rd, "final": fd, "ppm": ppm}
            if mejor and mejor["ppm"] >= a.min_ppm:
                break
        if not mejor:
            print(f"!! {nombre}: ninguna toma pasó los controles; se conserva el audio anterior", flush=True)
            continue
        previo = dur.get(nombre, {}).get("ppm", 0)
        if os.path.exists(f"{salida}/{nombre}.wav") and previo >= mejor["ppm"]:
            print(f"== {nombre}: la toma anterior ({previo} ppm) es mejor que la nueva ({round(mejor['ppm'])} ppm); se conserva", flush=True)
            continue
        os.replace(mejor["fin"], f"{salida}/{nombre}.wav")
        dur[nombre] = {"crudo_s": round(mejor["crudo"], 3), "final_s": round(mejor["final"], 3), "ratio": round(mejor["crudo"] / mejor["final"], 4),
                       "palabras": palabras, "ppm": round(mejor["ppm"]), "toma": mejor["toma"], "atempo": ATEMPO}
        json.dump(dur, open(dpath, "w"), indent=1, ensure_ascii=False)
    subprocess.run(["rm", "-rf", raw_dir])


if __name__ == "__main__":
    main()
