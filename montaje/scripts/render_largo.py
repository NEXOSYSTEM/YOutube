"""Render del vídeo largo con el flujo rápido (medido el 2026-11-18 con un bloque de 855 fotogramas):
un único render de Remotion SIN audio, Chrome en GPU (gl=angle; en CPU «swangle» es 5× más lento), concurrencia 4
(6 → 48 s, 8 → 64 s, 4 → 40 s por bloque), color y viñeta dentro de Remotion (evita volver a codificar), codificación H.264
por hardware (VideoToolbox). La banda sonora se mezcla aparte con numpy (mezcla_audio.py, segundos) y se une sin recodificar
la imagen; después, normalización en dos pasadas.
Escribe el progreso en ESTADO.md. Uso: render_largo.py salida.mp4 [concurrencia]"""
import json, os, re, subprocess, sys, time
RAIZ = os.environ.get("ALUCINATE_RAIZ") or os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
PY = f"{RAIZ}/voz/.venv/bin/python"; EST = [PY, f"{RAIZ}/montaje/scripts/estado.py"]
import imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
out = sys.argv[1]; CONC = sys.argv[2] if len(sys.argv) > 2 else "4"
PL = json.load(open(f"{RAIZ}/montaje/src/data/plan.json")); plan = PL["largo"]; FPS = PL.get("fps", 30); total = plan["len"]
tmp = f"{RAIZ}/montaje/.render-largo"; os.makedirs(tmp, exist_ok=True)
env = dict(os.environ, PATH=f"{RAIZ}/herramientas/node/bin:" + os.environ["PATH"], npm_config_cache=f"{RAIZ}/herramientas/.npm-cache")
def estado(*a): subprocess.run(EST + list(a))
t0 = time.time()
# 1) audio (segundos)
subprocess.run([PY, f"{RAIZ}/montaje/scripts/mezcla_audio.py", "largo", f"{tmp}/audio.wav"], check=True)
# 2) imagen: un único render, sin audio y sin color/viñeta por fotograma
lg = open(f"{tmp}/render.log", "w")
p = subprocess.Popen(["npx", "remotion", "render", "src/index.jsx", "Largo", f"{tmp}/imagen.mp4", "--muted", "--codec=h264",
                      "--hardware-acceleration=if-possible", "--video-bitrate=12M", f"--concurrency={CONC}", "--gl=angle",
                      "--offthreadvideo-cache-size-in-bytes=3000000000", "--timeout=120000"], cwd=f"{RAIZ}/montaje", env=env, stdout=lg, stderr=subprocess.STDOUT)
t1 = time.time()
while p.poll() is None:
    m = re.findall(r"Rendered (\d+)/(\d+)", open(f"{tmp}/render.log", errors="ignore").read()[-3000:])
    if m:
        n = int(m[-1][0]); e = json.load(open(f"{RAIZ}/montaje/.estado.json"))
        for x in e.get("pasos", []):
            if x.get("st") == "curso": x["pct"] = round(100 * n / total)
        if n: e["eta"] = time.strftime("%H:%M", time.localtime(time.time() + (time.time() - t1) * (total - n) / n + 90))
        json.dump(e, open(f"{RAIZ}/montaje/.estado.json", "w"), ensure_ascii=False, indent=1)
        estado("progreso", "/dev/null")
    time.sleep(15)
if p.returncode: print("ERROR en el render; ver", f"{tmp}/render.log"); sys.exit(1)
t2 = time.time()
# 3) unir imagen y banda sonora (sin recodificar la imagen) y normalizar
subprocess.run([FF, "-y", "-loglevel", "error", "-i", f"{tmp}/imagen.mp4", "-i", f"{tmp}/audio.wav", "-map", "0:v", "-map", "1:a",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", f"{tmp}/unido.mp4"], check=True)
subprocess.run([PY, f"{RAIZ}/montaje/scripts/normalizar.py", f"{tmp}/unido.mp4", out], check=True)
t3 = time.time()
print(f"audio {t1-t0:.0f} s · render {t2-t1:.0f} s · unión+normalización {t3-t2:.0f} s · total {t3-t0:.0f} s")
subprocess.run(["rm", "-rf", tmp])
