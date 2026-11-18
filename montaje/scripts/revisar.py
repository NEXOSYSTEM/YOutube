"""Revisión automática de los vídeos renderizados: duración, resolución, sonoridad, cortes a negro, congelados
y hoja de contactos (1 fotograma cada 10 s) para la revisión visual. Escribe revision.txt en cada carpeta."""
import re, subprocess, json
import imageio_ffmpeg

RAIZ = "/Users/luis/Desktop/Youtube/Alucinateconelmundo"
FF = imageio_ffmpeg.get_ffmpeg_exe()
VID = {"largo": "2026-11-18-largo-peces-venenosos/largo-peces-venenosos", "short01": "2026-11-18-short-pez-piedra/short01-pez-piedra",
       "short02": "2026-11-18-short-pez-arana/short02-pez-arana", "short03": "2026-11-18-short-ornitorrinco/short03-ornitorrinco"}
PLAN = json.load(open(f"{RAIZ}/montaje/src/data/plan.json", encoding="utf-8"))
for k, rel in VID.items():
    f = f"{RAIZ}/videos/{rel}.mp4"
    info = subprocess.run([FF, "-i", f], capture_output=True, text=True).stderr
    dur = re.search(r"Duration: (\d+):(\d+):([\d.]+)", info); dur = int(dur[1]) * 3600 + int(dur[2]) * 60 + float(dur[3])
    res = re.search(r"Video: .*?, (\d{3,4})x(\d{3,4})", info)
    an = subprocess.run([FF, "-i", f, "-vf", "blackdetect=d=0.25:pix_th=0.06,freezedetect=n=0.002:d=4", "-af", "ebur128=peak=true",
                         "-f", "null", "-"], capture_output=True, text=True).stderr
    negros = re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", an)
    congelados = re.findall(r"freeze_start: ([\d.]+)", an)
    I = re.findall(r"I:\s+(-?[\d.]+) LUFS", an)[-1]; P = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", an)[-1]
    esperado = PLAN[k]["len"] / PLAN.get("fps", 30)
    cols = "6x4" if k == "largo" else "8x2"
    step = max(1, dur / (24 if k == "largo" else 16))
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", f, "-vf", f"fps=1/{step:.2f},scale={320 if k == 'largo' else 180}:-1,tile={cols}:padding=4",
                    "-frames:v", "1", f"{RAIZ}/videos/{rel.split('/')[0]}/hoja-revision.jpg"])
    txt = (f"{rel}.mp4\n  duración {dur:.1f} s (plan {esperado:.1f} s) · {res[1]}x{res[2]} · {I} LUFS · pico {P} dBTP\n"
           f"  cortes a negro: {', '.join(f'{float(a):.1f}–{float(b):.1f}s' for a, b in negros) or 'ninguno'}\n"
           f"  imagen congelada >4 s: {', '.join(f'{float(a):.1f}s' for a in congelados) or 'ninguna'}\n")
    planos = [x for b in PLAN[k]["blocks"] for sc in b["scenes"] for x in sc.get("shots", []) if x.get("media")]
    ent = sum(1 for x in planos if x["media"].get("entero"))
    txt += f"  animal entero (contain, zoom ≤8 %): {ent} planos del animal de {len(planos)} · revisar en hoja-revision.jpg que no se corta\n"
    open(f"{RAIZ}/videos/{rel.split('/')[0]}/revision.txt", "w", encoding="utf-8").write(txt)
    print(txt, end="")
