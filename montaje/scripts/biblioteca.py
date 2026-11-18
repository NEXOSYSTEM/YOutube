"""Biblioteca de clips reutilizable: material/biblioteca/<animal o tema>/ con los planos ya revisados y usados
(proxies 1080p H.264, 30 fps) e índice JSON (etiquetas, licencia, autor, URL). Enlaces duros: no ocupa espacio extra."""
import json, os

RAIZ = os.environ.get("ALUCINATE_RAIZ") or os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import semana as S  # rutas de la semana
MAT = S.MAT
BIB = f"{RAIZ}/material/biblioteca"
CAT = json.load(open(f"{MAT}/_catalogo.json", encoding="utf-8"))["items"]
PLAN = json.load(open(f"{RAIZ}/montaje/src/data/plan.json", encoding="utf-8"))
idx_path = f"{BIB}/indice.json"
idx = json.load(open(idx_path, encoding="utf-8")) if os.path.exists(idx_path) else {}
por_file = {it["file"]: (pg, it) for pg, it in CAT.items()}
usados = set()
def recorre(x):
    if isinstance(x, dict):
        if "src" in x and str(x.get("src", "")).startswith("material/"): usados.add(x["src"][len("material/"):])
        for v in x.values(): recorre(v)
    elif isinstance(x, list):
        for v in x: recorre(v)
recorre(PLAN)
n = 0
for f in sorted(usados):
    if f not in por_file: continue
    pg, it = por_file[f]
    tema = f.split("/")[0]
    os.makedirs(f"{BIB}/{tema}", exist_ok=True)
    dst = f"{BIB}/{f}"
    if not os.path.exists(dst):
        os.link(f"{MAT}/{f}", dst)
    idx[f] = {"tema": tema, "tipo": "video" if it["video"] else "foto", "titulo": it["title"], "autor": it["author"],
              "licencia": it["license"], "fuente": it["src"], "url": pg, "ancho": it["w"], "alto": it["h"],
              "duracion_s": it.get("dur", 0), "usado_en": sorted(set(idx.get(f, {}).get("usado_en", [])) | {S.SEMANA})}
    n += 1
json.dump(idx, open(idx_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"biblioteca: {n} archivos usados indexados en material/biblioteca/indice.json")
