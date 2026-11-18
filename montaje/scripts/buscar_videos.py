"""Búsqueda de CLIPS DE VÍDEO con licencia comercial para cada animal y para planos de entorno.
- Wikimedia Commons (vídeo webm/ogv): CC0, dominio público (NOAA, USFWS, NPS…), CC BY y CC BY-SA. Sin NC/ND.
- Mixkit: solo clips con «Mixkit Stock Video Free License» (entorno: arrecife, fondo marino, río…).
- Pexels/Pixabay: requieren clave de API → no se usan (no se crean cuentas).
Pausas largas entre peticiones para no recibir HTTP 429 de Commons.
"""
import os
import json, sys, time
RAIZ = os.environ.get("ALUCINATE_RAIZ") or os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, f"{RAIZ}/montaje/scripts")
import buscar_material as B


ESPECIES = {
    "pez-piedra": ["Synanceia", "stonefish"],
    "pez-arana": ["Trachinus", "Echiichthys", "weever"],
    "ornitorrinco": ["Ornithorhynchus", "platypus"],
    "pez-conejo": ["Siganus", "rabbitfish"],
    "blenio": ["Meiacanthus", "Plagiotremus", "blenny"],
    "groenlandia": ["Somniosus", "Greenland shark", "sleeper shark"],
    "pez-gato": ["Plotosus", "eel catfish"],
    "cabracho": ["Scorpaena", "scorpionfish"],
    "pastinaca": ["Dasyatis", "stingray", "Hypanus"],
    "pez-leon": ["Pterois", "lionfish"],
    "pez-globo": ["Tetraodontidae", "pufferfish", "Arothron", "Diodon"],
}
ENTORNO = [  # (carpeta, etiqueta Mixkit, palabras del nombre)
    ("entorno", "coral-reef", []), ("entorno", "underwater", ["fish", "coral", "reef", "sea", "ocean", "school"]),
    ("entorno", "fish", ["fish", "school", "reef", "underwater"]), ("entorno", "ocean", ["underwater", "reef", "deep", "fish"]),
    ("entorno", "river", ["river", "stream", "water"]), ("entorno", "beach", ["shore", "waves", "sand", "people", "summer"]),
]

def main():
    cat = B.cat
    cat.setdefault("videos", {})
    for pool, qs in ESPECIES.items():
        if cat["videos"].get(pool):
            continue
        got, vistos = [], set()
        for q in qs:
            for intento in range(4):
                try:
                    res = B.commons(q, video=True, limit=25); break
                except Exception as e:
                    if "429" in str(e): time.sleep(40 * (intento + 1)); continue
                    res = []; break
            else:
                res = []
            for c in res:
                if c["page"] in vistos or len(got) >= 6:
                    continue
                vistos.add(c["page"])
                r = B.descarga(c, pool)
                if r and r.get("dur", 0) >= 3:
                    got.append(r["page"])
                time.sleep(3)
            time.sleep(4)
        cat["videos"][pool] = got
        json.dump(cat, open(B.CAT_PATH, "w"), ensure_ascii=False, indent=1)
        print(pool, len(got), "vídeos", flush=True)
    for carpeta, tag, kws in ENTORNO:
        key = f"entorno:{tag}"
        if cat["videos"].get(key):
            continue
        got = []
        for c in B.mixkit(tag, kws, limit=5):
            r = B.descarga(c, carpeta)
            if r:
                got.append(r["page"])
        cat["videos"][key] = got
        json.dump(cat, open(B.CAT_PATH, "w"), ensure_ascii=False, indent=1)
        print(key, len(got), "vídeos", flush=True)
    print("FIN")

if __name__ == "__main__":
    main()
