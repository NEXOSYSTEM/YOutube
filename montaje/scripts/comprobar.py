"""Comprobaciones obligatorias antes de cada render (ver REGLAS-DEL-CANAL.md).
Uso: comprobar.py <Composición>     (Largo, Short01, Short02, Short03, Prueba)
Sale con código 1 (y el render se detiene) si:
  1) algún audio de narración no está a x1,25 real (final = crudo / 1,25 ± 1 %) o el montaje lo recorta/estira;
  2) el porcentaje de vídeo en los planos baja del 70 % (los gráficos propios no cuentan).
"""
import json, sys, wave

RAIZ = "/Users/luis/Desktop/Youtube/Alucinateconelmundo"
FPS = json.load(open("/Users/luis/Desktop/Youtube/Alucinateconelmundo/montaje/src/data/plan.json")).get("fps", 30)
MIN_VIDEO = 0.70

comp = sys.argv[1]
clave = {"Largo": "largo", "Prueba": "prueba", "Short01": "short01", "Short02": "short02", "Short03": "short03"}.get(comp)
if not clave:
    print(f"(sin comprobaciones para {comp})"); sys.exit(0)
plan = json.load(open(f"{RAIZ}/montaje/src/data/plan.json", encoding="utf-8"))[clave]
dur = json.load(open(f"{RAIZ}/audio/2026-11-18-semana-01/duraciones.json", encoding="utf-8"))
errores = []

# 1) Voz a x1,25 real y sin estirar
for b in plan["blocks"]:
    if b.get("video"):
        continue
    nombre = b["audio"].split("/")[-1][:-4]
    d = dur.get(nombre)
    if not d:
        errores.append(f"{nombre}: no hay registro de duración cruda (generar con voz/narrar.py)"); continue
    with wave.open(f"{RAIZ}/audio/2026-11-18-semana-01/{nombre}.wav") as w:
        real = w.getnframes() / w.getframerate()
    esperado = d["crudo_s"] / 1.25 - d.get("pausas_recortadas_s", 0)  # pausas acortadas sin tocar la velocidad
    if abs(real - esperado) / esperado > 0.01:
        errores.append(f"{nombre}: dura {real:.2f} s y a x1,25 debería durar {esperado:.2f} s")
    if not b.get("cut") and abs(b["audioLen"] - round(real * FPS)) > 1:
        errores.append(f"{nombre}: el montaje reproduce {b['audioLen'] / FPS:.2f} s de {real:.2f} s")
    print(f"  voz {nombre}: {real:.2f} s = {d['crudo_s']:.2f}/1,25 ✓  ({d.get('ppm', '?')} ppm)")

# 2) Porcentaje de vídeo en los planos
tv = tf = 0
for b in plan["blocks"]:
    for sc in b["scenes"]:
        for sh in sc.get("shots", []):
            m = sh.get("media")
            if not m:
                continue
            if m["video"]:
                tv += sh["len"]
            else:
                tf += sh["len"]
pct = tv / (tv + tf) if tv + tf else 1
print(f"  vídeo en planos: {pct * 100:.0f} % ({tv / FPS:.0f} s vídeo · {tf / FPS:.0f} s foto)")
if pct < MIN_VIDEO:
    errores.append(f"solo {pct * 100:.0f} % de vídeo en los planos (mínimo {MIN_VIDEO * 100:.0f} %)")

if errores:
    print("✗ COMPROBACIÓN FALLIDA:\n  - " + "\n  - ".join(errores)); sys.exit(1)
print("✓ comprobaciones OK")
