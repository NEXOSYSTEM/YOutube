"""Estado en vivo del trabajo, en Alucinateconelmundo/ESTADO.md (Luis lo abre cuando quiera).
Uso desde producir.sh:
  estado.py inicio "<tarea>" "<pasos separados por |>"
  estado.py paso "<nombre del paso>"          → marca ese paso como «en curso»
  estado.py hecho "<nombre del paso>" <seg>   → lo marca como hecho con su duración
  estado.py progreso <fichero-log-remotion>   → lee «Rendered N/M» y escribe el % y la hora estimada de fin
  estado.py fin "<resumen>"                   → TERMINADO
  estado.py error "<motivo>"                  → ERROR
  estado.py esperando "<motivo>"              → ESPERANDO A LUIS
Si la última actualización tiene más de 3 minutos y no está TERMINADO, el propio archivo avisa de que puede estar parado.
"""
import json, os, re, sys, time
from datetime import datetime, timedelta

RAIZ = "/Users/luis/Desktop/Youtube/Alucinateconelmundo"
J = f"{RAIZ}/montaje/.estado.json"
MD = f"{RAIZ}/ESTADO.md"

def carga():
    return json.load(open(J)) if os.path.exists(J) else {}

def guarda(e):
    e["actualizado"] = datetime.now().strftime("%H:%M:%S")
    json.dump(e, open(J, "w"), ensure_ascii=False, indent=1)
    estado = e.get("estado", "EN MARCHA")
    icono = {"EN MARCHA": "🟢 EN MARCHA", "TRABAJANDO": "🟢 EN MARCHA", "ERROR": "🔴 ERROR", "PARADO": "🔴 ERROR",
             "ESPERANDO": "🟡 ESPERANDO A LUIS", "TERMINADO": "✅ TERMINADO"}.get(estado, estado)
    l = [f"# Estado del trabajo — {icono}", "",
         f"**Tarea:** {e.get('tarea', '')}  ", f"**Empezó:** {e.get('inicio', '')} · **Última actualización:** {e['actualizado']}  "]
    if e.get("eta"):
        l.append(f"**Fin estimado:** {e['eta']}  ")
    if estado in ("PARADO", "ERROR", "ESPERANDO"):
        l.append(f"**Motivo:** {e.get('motivo', '')}  ")
    if estado == "TERMINADO":
        l.append(f"**Resultado:** {e.get('resumen', '')}  ")
    l += ["", "| Paso | Estado | Tiempo |", "|---|---|---|"]
    for p in e.get("pasos", []):
        st = {"hecho": "✓ hecho", "curso": "⏳ en curso", "": "○ pendiente"}[p.get("st", "")]
        if p.get("st") == "curso" and p.get("pct") is not None:
            st += f" ({p['pct']} %)"
        l.append(f"| {p['n']} | {st} | {p.get('t', '')} |")
    l += ["", "_Si «Última actualización» tiene más de 3 minutos y no pone TERMINADO, algo se ha parado: avisa a Claude._", ""]
    open(MD, "w", encoding="utf-8").write("\n".join(l))

def busca(e, nombre):
    for p in e.get("pasos", []):
        if p["n"] == nombre: return p
    p = {"n": nombre, "st": ""}; e.setdefault("pasos", []).append(p); return p

cmd = sys.argv[1]
e = carga()
if cmd == "inicio":
    e = {"tarea": sys.argv[2], "inicio": datetime.now().strftime("%H:%M:%S"), "estado": "EN MARCHA",
         "pasos": [{"n": n, "st": ""} for n in sys.argv[3].split("|")], "t0": time.time()}
elif cmd == "paso":
    p = busca(e, sys.argv[2]); p["st"] = "curso"; p["t_ini"] = time.time(); e["estado"] = "EN MARCHA"
elif cmd == "hecho":
    p = busca(e, sys.argv[2]); p["st"] = "hecho"; s = int(float(sys.argv[3])); p["t"] = f"{s // 60} min {s % 60:02d} s"; p.pop("pct", None)
elif cmd == "progreso":
    txt = open(sys.argv[2], errors="ignore").read()[-4000:] if os.path.exists(sys.argv[2]) else ""
    m = re.findall(r"Rendered (\d+)/(\d+)", txt)
    cur = next((p for p in e.get("pasos", []) if p.get("st") == "curso"), None)
    if m and cur:
        n, tot = map(int, m[-1]); cur["pct"] = round(100 * n / tot)
        trans = time.time() - cur.get("t_ini", time.time())
        if n > 0:
            e["eta"] = (datetime.now() + timedelta(seconds=trans * (tot - n) / n)).strftime("%H:%M")
elif cmd == "fin":
    e["estado"] = "TERMINADO"; e["resumen"] = sys.argv[2]; e["eta"] = ""
elif cmd in ("parado", "error"):
    e["estado"] = "ERROR"; e["motivo"] = sys.argv[2]
elif cmd == "esperando":
    e["estado"] = "ESPERANDO"; e["motivo"] = sys.argv[2]
guarda(e)
