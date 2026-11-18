"""Render del vídeo largo con el flujo rápido (decisión 2026-11-18): un único render de Remotion SIN audio, sin filtro de color
ni viñeta por fotograma (post=true); la banda sonora se mezcla aparte con numpy (mezcla_audio.py) y ffmpeg aplica al final
el color y la viñeta (fuera de la intro) con codificación por hardware (VideoToolbox). Después, normalización en dos pasadas.
Escribe el progreso en ESTADO.md. Uso: render_largo.py salida.mp4 [concurrencia]"""
import json, os, re, subprocess, sys, time
RAIZ = "/Users/luis/Desktop/Youtube/Alucinateconelmundo"
PY = f"{RAIZ}/voz/.venv/bin/python"; EST = [PY, f"{RAIZ}/montaje/scripts/estado.py"]
import imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
out = sys.argv[1]; CONC = sys.argv[2] if len(sys.argv) > 2 else "6"
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
                      "--hardware-acceleration=if-possible", "--video-bitrate=16M", f"--concurrency={CONC}", "--props", json.dumps({"post": True}),
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
# 3) color + viñeta (fuera de la intro) con VideoToolbox, y unión con la banda sonora
intro = next((b for b in plan["blocks"] if b.get("video")), None)
en = f":enable='not(between(t,{intro['from']/FPS:.3f},{(intro['from']+intro['len'])/FPS:.3f}))'" if intro else ""
vf = f"eq=contrast=1.08:saturation=1.14:brightness=-0.01{en},vignette=angle=PI/4.6{en}"
subprocess.run([FF, "-y", "-loglevel", "error", "-i", f"{tmp}/imagen.mp4", "-i", f"{tmp}/audio.wav", "-map", "0:v", "-map", "1:a", "-vf", vf,
                "-c:v", "h264_videotoolbox", "-b:v", "12M", "-c:a", "aac", "-b:a", "192k", "-shortest", f"{tmp}/unido.mp4"], check=True)
subprocess.run([PY, f"{RAIZ}/montaje/scripts/normalizar.py", f"{tmp}/unido.mp4", out], check=True)
t3 = time.time()
print(f"audio {t1-t0:.0f} s · render {t2-t1:.0f} s · color+unión+normalización {t3-t2:.0f} s · total {t3-t0:.0f} s")
subprocess.run(["rm", "-rf", tmp])
