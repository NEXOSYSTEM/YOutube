"""Narración «fijada»: genera trozos de ≤2 frases (las tomas cortas apenas se desvían de acento/idioma),
con temperatura baja, lang_code spanish e instrucción de acento de España EN CADA LLAMADA.
Une los trozos con pausas cortas y aplica atempo 1,25 UNA vez al conjunto (regla del canal).
Registra crudo/final en <salida>/duraciones.json para comprobar.py.

Uso: voz/.venv/bin/python voz/narrar_frases.py --textos <dir> --salida <dir> [nombre ...]
"""
import argparse, json, os, re, subprocess, wave
import numpy as np

RAIZ = "/Users/luis/Desktop/Youtube/Alucinateconelmundo"
os.environ["HF_HOME"] = f"{RAIZ}/voz/modelos"
os.environ["HF_HUB_OFFLINE"] = "1"  # modelos ya descargados: sin conexión
MODELO = "mlx-community/Qwen3-TTS-12Hz-1.7B-CustomVoice-8bit"
VOZ, IDIOMA = "ryan", "spanish"
INSTR = ("Speak ONLY in Spanish with a neutral accent from Spain (standard Castilian, Madrid). "
         "Never switch to English or any other language or accent. Neutral, clear documentary narrator tone, "
         "no exaggerated emotion. Fairly fast, fluid pace.")
TEMP, TOP_K, TOP_P = 0.6, 30, 0.9
SR = 24000
PAUSA_FRASE = 0.22   # segundos (en crudo) entre trozos
ATEMPO = 1.25


def trozos(texto):
    frases = [f.strip() for f in re.findall(r"[^.!?…]+(?:[.!?…]+|$)", re.sub(r"\s+", " ", texto.strip())) if f.strip()]
    out, cur = [], ""
    for f in frases:
        if cur and (len(cur) + len(f) > 170 or cur.count(".") + cur.count("?") + cur.count("!") + cur.count("…") >= 2):
            out.append(cur.strip()); cur = ""
        cur += " " + f
    if cur.strip():
        out.append(cur.strip())
    return out


def lee(p):
    with wave.open(p) as w:
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768, w.getframerate()


def recorta(a, sr, umbral=0.012):
    fr = int(0.01 * sr); n = len(a) // fr
    if n == 0: return a
    rms = np.sqrt((a[: n * fr].reshape(n, fr) ** 2).mean(1))
    voz = np.where(rms > umbral)[0]
    if not len(voz): return a
    i0 = max(0, voz[0] * fr - int(0.03 * sr)); i1 = min(len(a), (voz[-1] + 1) * fr + int(0.06 * sr))
    return a[i0:i1]


def ok_trozo(a, sr, texto):
    d = len(a) / sr
    letras = len(re.sub(r"[^\wáéíóúüñ]", "", texto.lower()))
    cps = letras / max(d, 0.01)  # letras por segundo en crudo (≈11–17 en una lectura normal)
    fr = int(0.05 * sr); n = len(a) // fr
    rms = np.sqrt((a[: n * fr].reshape(n, fr) ** 2).mean(1)) if n else np.array([0])
    sil = rms < 0.01; best = cur = 0
    for s in sil:
        cur = cur + 1 if s else 0; best = max(best, cur)
    return 7 <= cps <= 24 and best * 0.05 < 1.6, cps  # solo descarta casos extremos (atropellos, cuelgues)


def norm(t):
    import unicodedata
    t = unicodedata.normalize("NFD", t.lower())
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-zñ0-9 ]", " ", t).split()


def carga16k(FF, x, sr):
    p = subprocess.run([FF, "-loglevel", "error", "-f", "f32le", "-ar", str(sr), "-ac", "1", "-i", "-", "-f", "f32le", "-ar", "16000", "-ac", "1", "-"],
                       input=x.astype(np.float32).tobytes(), capture_output=True, check=True)
    return np.frombuffer(p.stdout, np.float32)


def control_whisper(FF, x, sr, texto):
    """Idioma detectado y parecido palabra a palabra con el guion (0–1)."""
    import difflib, mlx_whisper
    r = mlx_whisper.transcribe(carga16k(FF, x, sr), path_or_hf_repo="mlx-community/whisper-large-v3-turbo", verbose=None, condition_on_previous_text=False)
    a, b = norm(texto), norm(r["text"])
    sim = difflib.SequenceMatcher(None, a, b).ratio()
    return r.get("language", "?"), sim, r["text"].strip()


UMBRAL = 0.85


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--textos", required=True); ap.add_argument("--salida", required=True); ap.add_argument("--intentos", type=int, default=5)
    ap.add_argument("nombres", nargs="*")
    a = ap.parse_args()
    textos = a.textos if a.textos.startswith("/") else f"{RAIZ}/{a.textos}"
    salida = a.salida if a.salida.startswith("/") else f"{RAIZ}/{a.salida}"
    tmp = f"{salida}/_trozos"; os.makedirs(tmp, exist_ok=True)
    import imageio_ffmpeg
    from mlx_audio.tts.utils import load_model
    from mlx_audio.tts.generate import generate_audio
    FF = imageio_ffmpeg.get_ffmpeg_exe()
    model = load_model(model_path=MODELO)
    dpath = f"{salida}/duraciones.json"
    dur = json.load(open(dpath)) if os.path.exists(dpath) else {}
    nombres = a.nombres or sorted(f[:-4] for f in os.listdir(textos) if f.endswith(".txt"))
    for nombre in nombres:
        texto = open(f"{textos}/{nombre}.txt", encoding="utf-8").read()
        partes, repetidos, revisar = [], 0, []
        for i, t in enumerate(trozos(texto)):
            mejor = None
            for k in range(a.intentos):
                pref = f"{tmp}/{nombre}_{i:02d}_{k}"
                generate_audio(text=t, model=model, voice=VOZ, lang_code=IDIOMA, instruct=INSTR, temperature=TEMP, top_k=TOP_K, top_p=TOP_P,
                               file_prefix=pref, join_audio=True, verbose=False)
                x, sr = lee(pref + ".wav"); x = recorta(x, sr)
                ritmo_ok, cps = ok_trozo(x, sr, t)
                idioma, sim, oido = control_whisper(FF, x, sr, t)
                bueno = ritmo_ok and idioma == "es" and sim >= UMBRAL
                nota = 2 * (idioma == "es") + sim + (0.3 if ritmo_ok else 0)
                if mejor is None or nota > mejor[2]:
                    mejor = (x, bueno, nota, idioma, sim, oido)
                if bueno: break
                repetidos += 1
                print(json.dumps({"nombre": nombre, "trozo": i, "intento": k + 1, "idioma": idioma, "parecido": round(sim, 2), "ritmo_ok": ritmo_ok, "oido": oido[:90]}, ensure_ascii=False), flush=True)
            if not mejor[1]:
                revisar.append({"trozo": i, "texto": t, "oido": mejor[5], "idioma": mejor[3], "parecido": round(mejor[4], 2)})
            partes.append(mejor[0])
        pausa = np.zeros(int(PAUSA_FRASE * SR), np.float32)
        crudo = np.concatenate([np.concatenate([p, pausa]) for p in partes])[: -len(pausa)]
        raw = f"{tmp}/{nombre}_crudo.wav"
        with wave.open(raw, "w") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(crudo, -1, 1) * 32767).astype(np.int16).tobytes())
        fin = f"{salida}/{nombre}.wav"
        subprocess.run([FF, "-y", "-loglevel", "error", "-i", raw, "-filter:a", f"atempo={ATEMPO}", "-ar", "24000", "-ac", "1", "-c:a", "pcm_s16le", fin], check=True)
        _, sr = lee(fin); fd = len(lee(fin)[0]) / sr; rd = len(crudo) / SR
        palabras = len(texto.split())
        dur[nombre] = {"crudo_s": round(rd, 3), "final_s": round(fd, 3), "ratio": round(rd / fd, 4), "palabras": palabras,
                       "ppm": round(palabras / fd * 60), "metodo": "frases+whisper", "trozos": len(partes), "repetidos": repetidos, "revisar": revisar, "atempo": ATEMPO}
        json.dump(dur, open(dpath, "w"), indent=1, ensure_ascii=False)
        print(json.dumps({"nombre": nombre, **dur[nombre]}, ensure_ascii=False), flush=True)
    subprocess.run(["rm", "-rf", tmp])


if __name__ == "__main__":
    main()
