"""Vídeo de stock con licencia comercial desde Pexels y Pixabay (claves gratuitas de Luis).
Las claves se leen de herramientas/claves-stock.txt (PEXELS=… / PIXABAY=…); nunca se escriben en logs.
Licencias: Pexels License y Pixabay Content License (uso comercial sin atribución obligatoria; se acredita igualmente).
"""
import json, os, re, subprocess, sys, time, urllib.parse, urllib.request
sys.path.insert(0, "/Users/luis/Desktop/Youtube/Alucinateconelmundo/montaje/scripts")
import buscar_material as B

RAIZ = B.RAIZ
CLAVES = {}
for l in open(f"{RAIZ}/herramientas/claves-stock.txt", encoding="utf-8"):
    if "=" in l:
        k, v = l.strip().split("=", 1); CLAVES[k.strip().upper()] = v.strip()

BUSQUEDAS = {  # carpeta: consultas (Pixabay busca en inglés)
    "pez-piedra": ["stonefish", "stone fish", "scorpionfish camouflage", "reef fish camouflage"],
    "pez-arana": ["weever", "fish sand", "flatfish sand", "fish hiding sand"],
    "ornitorrinco": ["platypus", "duck billed platypus", "australia river", "creek water australia"],
    "pez-conejo": ["rabbitfish", "foxface", "siganus", "reef fish algae"],
    "blenio": ["blenny", "goby", "small reef fish coral"],
    "groenlandia": ["greenland shark", "sleeper shark", "shark", "arctic sea ice", "iceberg"],
    "pez-gato": ["catfish school", "eel catfish", "catfish", "fish school ball"],
    "cabracho": ["scorpionfish", "scorpion fish", "red scorpionfish", "mediterranean fish"],
    "pastinaca": ["stingray", "sting ray", "ray fish", "manta"],
    "pez-leon": ["lionfish", "lion fish", "pterois"],
    "pez-globo": ["pufferfish", "puffer fish", "blowfish", "porcupinefish", "fugu"],
    "generico": ["shark jaws", "octopus", "deep sea", "underwater light", "feet beach", "fisherman", "fish market",
                 "frying fish", "crowded beach spain", "lifeguard", "ambulance", "sushi chef", "dead fish beach",
                 "coral reef", "foot water", "hand water"],
}

def get_json(url, headers):
    req = urllib.request.Request(url, headers={"User-Agent": "AlucinateMontaje/1.0", **headers})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())

def pexels(q):
    if "PEXELS" not in CLAVES: return []
    d = get_json("https://api.pexels.com/videos/search?" + urllib.parse.urlencode({"query": q, "per_page": 12}), {"Authorization": CLAVES["PEXELS"]})
    out = []
    for v in d.get("videos", []):
        fs = sorted([f for f in v["video_files"] if (f.get("width") or 0) >= 1280 and f.get("file_type") == "video/mp4"], key=lambda f: f["width"])
        if not fs or v.get("duration", 0) < 4: continue
        f = next((x for x in fs if x["width"] >= 1920), fs[-1])
        out.append({"src": "Pexels", "title": f"pexels_{v['id']}", "w": f["width"], "h": f["height"], "video": True, "dl": f["link"],
                    "page": v["url"], "author": v["user"]["name"], "license": "Pexels License", "rank": 0, "q": q})
    return out

def pixabay(q):
    if "PIXABAY" not in CLAVES: return []
    d = get_json("https://pixabay.com/api/videos/?" + urllib.parse.urlencode({"key": CLAVES["PIXABAY"], "q": q, "per_page": 12, "safesearch": "true"}), {})
    out = []
    for h in d.get("hits", []):
        v = h["videos"].get("large") or h["videos"].get("medium")
        if not v or not v.get("url") or (v.get("width") or 0) < 1280 or h.get("duration", 0) < 4: continue
        if re.search(r"\bai\b|ai generated|ai-generated|generated|artificial intelligence|render|3d|animation|cgi", h.get("tags", ""), re.I):
            continue  # nada generado por IA ni 3D: debe ser metraje real
        out.append({"src": "Pixabay", "title": f"pixabay_{h['id']}", "w": v["width"], "h": v["height"], "video": True, "dl": v["url"],
                    "page": h["pageURL"], "author": h.get("user", "Pixabay"), "license": "Pixabay Content License", "rank": 0, "q": q})
    return out

def main():
    cat = B.cat
    cat.setdefault("stock", {})
    for carpeta, qs in BUSQUEDAS.items():
        for q in qs:
            key = f"{carpeta}:{q}"
            if cat["stock"].get(key) is not None: continue
            cands = []
            for f in (pexels, pixabay):
                try: cands += f(q)
                except Exception as e: cat["log"].append(f"{f.__name__} '{q}': {type(e).__name__}")
                time.sleep(1)
            got = []
            for c in cands[: (6 if carpeta != "generico" else 3)]:
                r = B.descarga(c, carpeta)
                if r: got.append(r["page"])
            cat["stock"][key] = got
            json.dump(cat, open(B.CAT_PATH, "w"), ensure_ascii=False, indent=1)
            print(key, len(got), flush=True)
    print("FIN")

if __name__ == "__main__":
    main()
