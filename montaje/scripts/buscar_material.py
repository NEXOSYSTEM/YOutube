"""Descarga material con licencia libre para la semana 1.

Fuentes: Wikimedia Commons (API, sin clave; incluye NOAA/USFWS/NPS/USGS subidas allí)
y Mixkit (vídeo, solo ítems con «Mixkit Stock Video Free License»).
Salida: material/2026-11-18-semana-01/<carpeta>/ + _catalogo.json
"""
import html, json, os, re, subprocess, sys, time, urllib.parse, urllib.request

RAIZ = os.environ.get("ALUCINATE_RAIZ") or os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import semana as S  # rutas de la semana
MAT = S.MAT
ESC = json.load(open(f"{RAIZ}/montaje/src/data/escenas.json", encoding="utf-8"))
sys.path.insert(0, "")
import imageio_ffmpeg  # del venv de voz
FF = imageio_ffmpeg.get_ffmpeg_exe()
UA_API = "AlucinateMontaje/1.0 (montaje local de vídeo educativo; python-urllib)"
UA_WEB = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"
CAT_PATH = f"{MAT}/_catalogo.json"
cat = json.load(open(CAT_PATH)) if os.path.exists(CAT_PATH) else {"items": {}, "pools": {}, "queries": {}, "log": []}

BAD_TITLE = re.compile(r"(map|distribution|range|stamp|logo|diagram|drawing|illustrat|plate|label|chart|skeleton_of|fossil|coat_of_arms|\.svg|\.gif|\.tif)", re.I)
LIC_OK = re.compile(r"^(cc0|pd[a-z0-9-]*|public domain|cc-by-[0-9.]+|cc-by-sa-[0-9.]+|cc by [0-9.]+|cc by-sa [0-9.]+|cc-by-sa-[0-9.]+-[a-z]+|cc-by-[0-9.]+-[a-z]+)$", re.I)


def get(url, ua=UA_API, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": ua})
            with urllib.request.urlopen(req, timeout=60) as r:
                return r.read()
        except Exception as e:
            if i == tries - 1:
                raise
            time.sleep(2 + 3 * i)


def strip(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s or "")).strip()


def lic_rank(lic):
    l = lic.lower()
    if "sa" in l.split("-") or "by-sa" in l or "by sa" in l:
        return 2
    if l.startswith("cc-by") or l.startswith("cc by"):
        return 1
    return 0  # cc0 / dominio público / Mixkit Free


def commons(query, video=False, limit=40):
    ft = "filetype:video" if video else "filetype:bitmap"
    p = {"action": "query", "format": "json", "generator": "search", "gsrnamespace": 6,
         "gsrsearch": f"{query} {ft}", "gsrlimit": limit, "prop": "imageinfo",
         "iiprop": "url|size|mime|extmetadata", "iiurlwidth": 1920}
    d = json.loads(get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(p)))
    pages = sorted((d.get("query") or {}).get("pages", {}).values(), key=lambda x: x.get("index", 0))
    out = []
    for pg in pages:
        ii = (pg.get("imageinfo") or [None])[0]
        if not ii:
            continue
        title = pg["title"]
        em = ii.get("extmetadata", {})
        lic = (em.get("License", {}) or {}).get("value", "") or ""
        short = strip((em.get("LicenseShortName", {}) or {}).get("value", ""))
        lic_s = lic or short
        low = (lic_s + " " + short).lower()
        if "nc" in re.split(r"[-\s]", low) or "nd" in re.split(r"[-\s]", low):
            continue
        if not (LIC_OK.match(lic.strip()) or LIC_OK.match(short.strip()) or short.lower().startswith("public domain")):
            continue
        if BAD_TITLE.search(title):
            continue
        mime = ii.get("mime", "")
        w, h = ii.get("width", 0), ii.get("height", 0)
        if video:
            if mime not in ("video/webm", "application/ogg", "video/ogg"):
                continue
            if w < 960:
                continue
        else:
            if mime not in ("image/jpeg", "image/png"):
                continue
            if w < 1280 or h < 600:
                continue
            if w / max(h, 1) < 0.9 or w / max(h, 1) > 2.6:
                pass  # se admiten verticales para los Shorts
        author = strip((em.get("Artist", {}) or {}).get("value", "")) or "Desconocido"
        out.append({"src": "Wikimedia Commons", "title": title, "w": w, "h": h, "video": video,
                    "dl": ii.get("url") if video else (ii.get("thumburl") or ii["url"]),
                    "page": ii.get("descriptionurl"), "author": author[:160],
                    "license": short or lic, "rank": lic_rank(lic or short)})
    return out


def mixkit(tag, keywords, limit=3):
    try:
        page = get(f"https://mixkit.co/free-stock-video/{tag}/", ua=UA_WEB).decode("utf-8", "ignore")
    except Exception as e:
        cat["log"].append(f"Mixkit {tag}: error {e}")
        return []
    links = list(dict.fromkeys(re.findall(r'/free-stock-video/([a-z0-9-]+-(\d+))/', page)))
    out = []
    for slug, vid in links:
        if keywords and not any(k in slug for k in keywords):
            continue
        url = f"https://mixkit.co/free-stock-video/{slug}/"
        try:
            ip = get(url, ua=UA_WEB).decode("utf-8", "ignore")
        except Exception:
            continue
        lics = set(re.findall(r'data-license="([a-zA-Z]+)"', ip))
        if lics != {"videoFree"}:
            cat["log"].append(f"Mixkit {slug}: licencia {lics or 'desconocida'} → descartado")
            continue
        mp4s = re.findall(rf'https://assets.mixkit.co/videos/{vid}/{vid}-(\d+)\.mp4', ip)
        res = max([int(x) for x in mp4s] or [0])
        if res < 720:
            continue
        try:
            req = urllib.request.Request(f"https://assets.mixkit.co/videos/{vid}/{vid}-1080.mp4",
                                         headers={"User-Agent": UA_WEB, "Range": "bytes=0-10"})
            with urllib.request.urlopen(req, timeout=20) as r:
                if r.status in (200, 206):
                    res = 1080
        except Exception:
            pass
        out.append({"src": "Mixkit", "title": slug, "w": 0, "h": res, "video": True,
                    "dl": f"https://assets.mixkit.co/videos/{vid}/{vid}-{res}.mp4", "page": url,
                    "author": "Mixkit", "license": "Mixkit Stock Video Free License", "rank": 0})
        if len(out) >= limit:
            break
    return out


def descarga(it, folder):
    key = it["page"]
    if key in cat["items"]:
        return cat["items"][key]
    os.makedirs(f"{MAT}/{folder}", exist_ok=True)
    base = re.sub(r"[^A-Za-z0-9]+", "_", re.sub(r"^File:", "", it["title"]))[:60].strip("_").lower()
    n = len(os.listdir(f"{MAT}/{folder}")) + 1
    try:
        data = get(it["dl"], ua=UA_API if it["src"] == "Wikimedia Commons" else UA_WEB)
    except Exception as e:
        cat["log"].append(f"descarga fallida {it['page']}: {e}")
        return None
    if it["video"]:
        tmp = f"{MAT}/{folder}/_tmp_{n}"
        open(tmp, "wb").write(data)
        out = f"{MAT}/{folder}/{n:02d}_{base}.mp4"
        r = subprocess.run([FF, "-y", "-loglevel", "error", "-i", tmp, "-t", "20", "-an",
                            "-vf", "scale='min(1920,iw)':-2,fps=30", "-c:v", "libx264", "-preset", "veryfast",
                            "-crf", "20", "-pix_fmt", "yuv420p", out])
        os.remove(tmp)
        if r.returncode != 0:
            cat["log"].append(f"conversión fallida {it['page']}")
            return None
        pr = subprocess.run([FF, "-i", out], capture_output=True, text=True).stderr
        m = re.search(r"Duration: (\d+):(\d+):([\d.]+)", pr)
        dur = int(m[1]) * 3600 + int(m[2]) * 60 + float(m[3]) if m else 0
        s = re.search(r", (\d{3,4})x(\d{3,4})", pr)
        it = dict(it, dur=dur, w=int(s[1]) if s else it["w"], h=int(s[2]) if s else it["h"])
        if dur < 3:
            os.remove(out)
            return None
    else:
        ext = ".png" if it["dl"].lower().endswith(".png") else ".jpg"
        out = f"{MAT}/{folder}/{n:02d}_{base}{ext}"
        open(out, "wb").write(data)
        # medidas reales del archivo bajado (miniatura de 1920 px)
        r = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", out], capture_output=True, text=True).stdout
        wv = re.search(r"pixelWidth: (\d+)", r); hv = re.search(r"pixelHeight: (\d+)", r)
        it = dict(it, w=int(wv[1]) if wv else it["w"], h=int(hv[1]) if hv else it["h"])
    rec = {k: it[k] for k in ("src", "title", "w", "h", "video", "page", "author", "license", "rank")}
    rec["dur"] = it.get("dur", 0)
    rec["file"] = os.path.relpath(out, MAT)
    cat["items"][key] = rec
    json.dump(cat, open(CAT_PATH, "w"), ensure_ascii=False, indent=1)
    return rec


def ordena(cands):
    # licencia más permisiva primero; se mantiene el orden de relevancia dentro de cada nivel
    return sorted(cands, key=lambda c: c["rank"])


MIXKIT = {  # escena -> (etiqueta de Mixkit, palabras del slug)
    "0.4": ("beach", ["feet", "walk", "barefoot"]), "8.4": ("beach", ["feet", "foot", "barefoot", "walk"]),
    "S2.1": ("beach", ["feet", "foot", "barefoot"]), "S1.4": ("beach", ["feet", "foot", "barefoot"]),
    "0.7": ("underwater", ["deep", "dark", "particles", "ocean", "underwater"]),
    "8.3": ("beach", ["people", "tourists", "crowded", "summer", "bathers"]),
    "S2.4": ("beach", ["people", "tourists", "crowded", "summer"]),
    "13.6": ("ambulance", ["ambulance"]), "4.2": ("ice", ["arctic", "iceberg", "glacier", "ice"]),
    "6.6": ("cooking", ["fish", "pan", "frying"]), "2.4": ("fishing", ["fish", "fisherman"]),
    "S2.5": ("beach", ["walking-out", "leaving", "coming-out", "exit"]),
    "12.4": ("sushi", ["chef", "cutting", "sushi"]),
}


def main():
    os.makedirs(MAT, exist_ok=True)
    # 1) Pools por especie: imágenes + vídeos de Commons
    for pool, cfg in ESC["pools"].items():
        if pool in cat["pools"] and len(cat["pools"][pool]) >= 12:
            continue
        cands, seen = [], set()
        for q in cfg["commons"]:
            for video in (False, True):
                try:
                    for c in commons(q, video=video, limit=30 if not video else 10):
                        if c["page"] not in seen:
                            seen.add(c["page"]); cands.append(c)
                except Exception as e:
                    cat["log"].append(f"Commons '{q}': {e}")
            time.sleep(0.5)
        vids = [c for c in cands if c["video"]][:3]
        imgs = ordena([c for c in cands if not c["video"]])
        got = []
        for c in vids + imgs:
            if len(got) >= 16:
                break
            r = descarga(c, pool)
            if r:
                got.append(r["page"])
        cat["pools"][pool] = got
        print(pool, len(got), "archivos", flush=True)
        json.dump(cat, open(CAT_PATH, "w"), ensure_ascii=False, indent=1)
    # 2) Escenas con búsqueda propia
    def scenes():
        for b in ESC["largo"]:
            for s in b["scenes"]:
                yield s
                for side in ("left", "right"):
                    if isinstance(s.get(side), dict) and s[side].get("q"):
                        yield dict(s[side], id=f"{s['id']}{side[0]}")
        for sh in ESC["shorts"].values():
            yield from sh["scenes"]
    for s in scenes():
        if not s.get("q"):
            continue
        key = s["id"]
        if key in cat["queries"] and cat["queries"][key]:
            continue
        need = 3 if s.get("t", 4) >= 8 else 2
        got = []
        if key in MIXKIT:
            tag, kws = MIXKIT[key]
            for c in mixkit(tag, kws, limit=2):
                r = descarga(c, s["folder"])
                if r:
                    got.append(r["page"])
        cands, seen = [], set()
        for q in s["q"]:
            try:
                for c in commons(q, limit=20):
                    if c["page"] not in seen:
                        seen.add(c["page"]); cands.append(c)
            except Exception as e:
                cat["log"].append(f"Commons '{q}': {e}")
        for c in ordena(cands):
            if len(got) >= need + (1 if key in MIXKIT else 0):
                break
            r = descarga(c, s["folder"])
            if r:
                got.append(r["page"])
        cat["queries"][key] = got
        print(key, s["folder"], len(got), flush=True)
        json.dump(cat, open(CAT_PATH, "w"), ensure_ascii=False, indent=1)
    # 3) Mapa base (NASA Blue Marble, dominio público)
    if "mapa" not in cat:
        p = {"action": "query", "format": "json", "titles": "File:Land ocean ice 2048.jpg", "prop": "imageinfo",
             "iiprop": "url|size|extmetadata", "iiurlwidth": 1920}
        d = json.loads(get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(p)))
        pg = list(d["query"]["pages"].values())[0]
        ii = pg["imageinfo"][0]; em = ii["extmetadata"]
        it = {"src": "Wikimedia Commons", "title": pg["title"], "w": ii["width"], "h": ii["height"], "video": False,
              "dl": ii.get("thumburl") or ii["url"], "page": ii["descriptionurl"],
              "author": strip(em.get("Artist", {}).get("value", "NASA")),
              "license": strip(em.get("LicenseShortName", {}).get("value", "")), "rank": 0}
        r = descarga(it, "mapas")
        cat["mapa"] = r["page"] if r else None
    json.dump(cat, open(CAT_PATH, "w"), ensure_ascii=False, indent=1)
    print("FIN", len(cat["items"]), "archivos")


if __name__ == "__main__":
    main()
