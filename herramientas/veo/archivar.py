#!/usr/bin/env python3
"""Archiva un clip de Veo descargado en material/: lo copia a su carpeta, lo apunta en registro-veo.csv y creditos.md.
Uso: python3 herramientas/veo/archivar.py <origen> <id> <semana-dir> <subcarpeta> <nombre.mp4> <pieza> <escena> <tema> <especie> <formato> <estado> <prompt>"""
import csv, shutil, sys, os, datetime
R = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # raíz del proyecto
M = os.path.join(R, "material")
src, vid, sem, sub, nom, pieza, escena, tema, esp, fmt, estado, prompt = sys.argv[1:13]
dst_rel = f"{sem}/{sub}/{nom}"
dst = os.path.join(M, dst_rel)
os.makedirs(os.path.dirname(dst), exist_ok=True)
shutil.copy2(src, dst)
res = "1280x720" if fmt == "16:9" else "720x1280"
reg = os.path.join(M, "registro-veo.csv")
rows = list(csv.reader(open(reg)))
rows = [r for r in rows if r[0] != vid]
rows.append([vid, datetime.date.today().isoformat(), dst_rel, sem.split('-', 3)[-1], pieza, escena, tema, esp, fmt, "10", res, "Gemini app Veo (cuenta trabajo Pro)", estado, prompt])
csv.writer(open(reg, "w", newline="")).writerows(rows)
cred = os.path.join(M, sem, "creditos.md")
if os.path.exists(cred):
    L = open(cred).read().split("\n")
    fila = f"| {sub}/{nom} | Generado con IA (Veo, Google) | Uso propio; ver material/licencia-veo.md | Gemini app, cuenta de Luis, {datetime.date.today()} | {estado} |"
    if fila.split(" | ")[0] not in "\n".join(L):
        i = max(k for k, l in enumerate(L) if l.startswith("| ") and "```" not in l and k < next((j for j, x in enumerate(L) if x.startswith("```")), len(L)))
        L.insert(i + 1, fila); open(cred, "w").write("\n".join(L))
proc = os.path.join(M, "_entrada-veo", "procesados"); os.makedirs(proc, exist_ok=True)
try: shutil.move(src, os.path.join(proc, f"{vid}_{os.path.basename(src).lstrip('.')}"))
except Exception as e: print("aviso: no se pudo mover el original:", e)
print("OK", dst_rel)
