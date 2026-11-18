"""Segunda pasada de material: búsquedas por categoría exacta de Commons (más precisas), con pausas
para no saturar la API (la primera pasada recibió HTTP 429). Mismas reglas de licencia."""
import os
import json, sys, time
RAIZ = os.environ.get("ALUCINATE_RAIZ") or os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, f"{RAIZ}/montaje/scripts")
import buscar_material as B


TAREAS = [
    # (carpeta, clave en el catálogo, [búsquedas], máximo)
    ("pez-arana", "x:pez-arana", ['incategory:"Trachinus draco"', 'incategory:"Echiichthys vipera"', 'incategory:"Trachinus araneus"'], 14),
    ("pastinaca", "x:pastinaca", ['incategory:"Dasyatis pastinaca"', 'incategory:"Hypanus americanus"', 'incategory:"Taeniura lymma"', 'incategory:"Bathytoshia lata"'], 14),
    ("pastinaca", "x:aguijon", ['stingray barb', 'stingray stinger tail', 'incategory:"Stingray spines"'], 4),
    ("pez-globo", "x:pez-globo", ['incategory:"Takifugu rubripes"', 'incategory:"Arothron hispidus"', 'incategory:"Arothron nigropunctatus"', 'incategory:"Arothron meleagris"'], 14),
    ("pez-globo", "x:inflado", ['incategory:"Inflated pufferfish"', 'incategory:"Diodon holocanthus"', 'inflated porcupinefish', 'puffed pufferfish'], 6),
    ("pez-globo", "x:fugu", ['incategory:"Fugu"', 'fugu sashimi', 'tessa fugu'], 6),
    ("groenlandia", "x:groenlandia", ['incategory:"Somniosus microcephalus"', 'incategory:"Somniosus pacificus"', 'Greenland shark NOAA'], 10),
    ("groenlandia", "x:hakarl", ['incategory:"Hákarl"', 'hákarl Bjarnarhöfn'], 5),
    ("groenlandia", "x:hielo", ['incategory:"Sea ice in the Arctic Ocean"', 'arctic sea ice floes', 'pack ice Svalbard'], 5),
    ("generico", "x:pulpo", ['incategory:"Octopus vulgaris"', 'octopus tentacles underwater'], 4),
    ("generico", "x:queensland", ['incategory:"Aerial photographs of the Great Barrier Reef"', 'Great Barrier Reef aerial', 'Queensland coastline beach'], 4),
    ("generico", "x:guantes", ['fisherman gloves fish', 'gloved hands fish market'], 3),
    ("cabracho", "x:cabracho", ['incategory:"Scorpaena scrofa"'], 8),
    ("pez-piedra", "x:pez-piedra", ['incategory:"Synanceia verrucosa"', 'incategory:"Synanceia horrida"'], 10),
    ("ornitorrinco", "x:espolon", ['platypus spur', 'incategory:"Ornithorhynchus anatinus skeletons"', 'platypus hind foot'], 4),
]


def main():
    cat = B.cat
    for folder, key, qs, mx in TAREAS:
        if cat.get("extra", {}).get(key):
            continue
        cands, seen = [], set(cat["items"].keys())
        for q in qs:
            for video in (False, True):
                for intento in range(4):
                    try:
                        res = B.commons(q, video=video, limit=30 if not video else 8)
                        break
                    except Exception as e:
                        if "429" in str(e):
                            time.sleep(30 * (intento + 1)); continue
                        res = []; break
                else:
                    res = []
                for c in res:
                    if c["page"] not in seen:
                        seen.add(c["page"]); cands.append(c)
                time.sleep(1.5)
        # relevancia primero (orden de la búsqueda); BY-SA solo detrás de CC0/PD/BY dentro de cada búsqueda
        got = []
        for c in cands:
            if len(got) >= mx:
                break
            for intento in range(4):
                r = B.descarga(c, folder)
                if r or not any("429" in l for l in cat["log"][-1:]):
                    break
                cat["log"].pop(); time.sleep(30 * (intento + 1))
            if r:
                got.append(r["page"])
            time.sleep(1.2)
        cat.setdefault("extra", {})[key] = got
        json.dump(cat, open(B.CAT_PATH, "w"), ensure_ascii=False, indent=1)
        print(key, folder, len(got), flush=True)
    print("FIN")


if __name__ == "__main__":
    main()
