"""Datos de la semana que se está produciendo (un solo sitio para todas las rutas).

La semana se elige con la variable ALUCINATE_SEMANA (p. ej. «2026-11-25-semana-02»); producir.sh la pone sola.
Sin variable se usa la semana 1, así los scripts siguen funcionando igual que antes.
Cada semana describe sus piezas en guiones/<semana>/semana.json (ver guiones/2026-11-18-semana-01/semana.json).
"""
import json, os

RAIZ = os.environ.get("ALUCINATE_RAIZ") or os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SEMANA = os.environ.get("ALUCINATE_SEMANA", "2026-11-18-semana-01")
CFG = json.load(open(f"{RAIZ}/guiones/{SEMANA}/semana.json", encoding="utf-8"))

MAT = f"{RAIZ}/material/{SEMANA}"          # clips, fotos y _catalogo.json
AUD = f"{RAIZ}/audio/{SEMANA}"             # narración y duraciones.json
TXT = f"{RAIZ}/guiones/{SEMANA}/textos-voz"
MINIS = f"{RAIZ}/miniaturas/{SEMANA}"

PIEZAS = CFG["piezas"]                                   # largo, short01, short02, short03…
CARP = {k: p["carpeta"] for k, p in PIEZAS.items()}      # carpeta con fecha dentro de videos/
ARCH = {k: p["archivo"] for k, p in PIEZAS.items()}      # nombre del mp4/.srt sin extensión
MINI = {k: p["miniatura"] for k, p in PIEZAS.items()}    # archivo dentro de MINIS
VID = {k: f"{CARP[k]}/{ARCH[k]}" for k in PIEZAS}

if __name__ == "__main__":  # usado por producir.sh: «clave composición carpeta/archivo nombre»
    for k, p in PIEZAS.items():
        print(k, p["composicion"], VID[k], p["nombre"], sep="\t")
