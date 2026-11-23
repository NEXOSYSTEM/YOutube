"""Engagement del nicho (2026-11-22): vídeos en español con más engagement en animales, informática,
geografía e historia. Solo lee datos públicos con el token de subida/subir.py (como investigacion/radar.py).
Gasto aproximado: ~1.300 de las 10.000 unidades diarias.

Uso (desde la raíz Alucinateconelmundo):
  subida/.venv/bin/python investigacion/engagement.py [--dias 365]
Escribe investigacion/2026-11-22-engagement.json
"""
import argparse, datetime as dt, json, math, re, sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / "subida"))
from googleapiclient.discovery import build  # noqa: E402
from subir import credenciales  # noqa: E402

BUSQUEDAS = [
    ("Animales", "curiosidades de animales"),
    ("Animales", "animales más peligrosos del mundo"),
    ("Animales", "animales increíbles que no conocías"),
    ("Animales", "datos curiosos animales shorts"),
    ("Informática", "cómo funciona internet explicado"),
    ("Informática", "historia de la informática curiosidades"),
    ("Informática", "cómo funciona un ordenador por dentro"),
    ("Geografía", "curiosidades de países del mundo"),
    ("Geografía", "lugares más extraños del mundo"),
    ("Geografía", "mapas curiosos geografía"),
    ("Historia", "historia curiosa datos que no sabías"),
    ("Historia", "inventos que cambiaron la historia"),
    ("Historia", "misterios de la historia"),
]
COMPETENCIA_ES = ["SORPRENDENTE", "BÚHO SABIO", "Andrés Andel", "Curiosidad Animal"]
CACHE = BASE / "investigacion" / "radar-canales.json"
ES = set("el la los las de que y en un una por para con más como qué cómo por qué este esta es son del al lo".split())


def segundos(iso):
    m = re.fullmatch(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or "")
    if not m:
        return 0
    d, h, mi, s = (int(x or 0) for x in m.groups())
    return d * 86400 + h * 3600 + mi * 60 + s


def es_espanol(sn):
    lang = (sn.get("defaultAudioLanguage") or sn.get("defaultLanguage") or "").lower()
    if lang:
        return lang.startswith("es")
    palabras = re.findall(r"[a-záéíóúñ]+", sn["title"].lower())
    return any(p in ES for p in palabras) or bool(re.search(r"[ñ¿¡áéíóú]", sn["title"].lower()))


def lotes(xs, n=50):
    for i in range(0, len(xs), n):
        yield xs[i:i + n]


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dias", type=int, default=365)
    a = p.parse_args()
    yt = build("youtube", "v3", credentials=credenciales(), cache_discovery=False)
    ahora = dt.datetime.now(dt.timezone.utc)
    desde = (ahora - dt.timedelta(days=a.dias)).strftime("%Y-%m-%dT%H:%M:%SZ")

    origen = {}
    for pilar, q in BUSQUEDAS:  # 100 unidades cada una
        r = yt.search().list(part="id", q=q, type="video", order="viewCount", publishedAfter=desde,
                             relevanceLanguage="es", maxResults=50).execute()
        for it in r.get("items", []):
            origen.setdefault(it["id"]["videoId"], pilar)
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    ids_comp = [cache[n] for n in COMPETENCIA_ES if n in cache]
    if ids_comp:
        ch = yt.channels().list(part="contentDetails", id=",".join(ids_comp)).execute()
        for c in ch.get("items", []):
            pl = c["contentDetails"]["relatedPlaylists"]["uploads"]
            r = yt.playlistItems().list(part="contentDetails", playlistId=pl, maxResults=50).execute()
            for it in r.get("items", []):
                origen.setdefault(it["contentDetails"]["videoId"], "Competencia")

    videos = []
    for grupo in lotes(list(origen)):
        r = yt.videos().list(part="snippet,statistics,contentDetails", id=",".join(grupo)).execute()
        videos += r.get("items", [])
    canales = {}
    for grupo in lotes(sorted({v["snippet"]["channelId"] for v in videos})):
        r = yt.channels().list(part="statistics,snippet", id=",".join(grupo)).execute()
        for c in r.get("items", []):
            st = c["statistics"]
            canales[c["id"]] = {"nombre": c["snippet"]["title"], "subs": int(st.get("subscriberCount", 0) or 0),
                                "videos": int(st.get("videoCount", 0) or 0), "vistas": int(st.get("viewCount", 0) or 0),
                                "pais": c["snippet"].get("country")}

    filas = []
    for v in videos:
        sn, st = v["snippet"], v.get("statistics", {})
        if not es_espanol(sn):
            continue
        vistas = int(st.get("viewCount", 0) or 0)
        if vistas < 20000:
            continue
        likes, coms = int(st.get("likeCount", 0) or 0), int(st.get("commentCount", 0) or 0)
        c = canales.get(sn["channelId"], {})
        media_canal = c.get("vistas", 0) / max(c.get("videos", 1), 1)
        pub = dt.datetime.fromisoformat(sn["publishedAt"].replace("Z", "+00:00"))
        dias = max((ahora - pub).days, 1)
        dur = segundos(v["contentDetails"]["duration"])
        filas.append({
            "id": v["id"], "url": f"https://youtu.be/{v['id']}", "pilar": origen[v["id"]],
            "titulo": sn["title"], "canal": sn["channelTitle"], "subs": c.get("subs", 0),
            "publicado": sn["publishedAt"][:10], "dias": dias, "duracion_s": dur,
            "tipo": "Short" if dur <= 180 else "Largo", "vistas": vistas, "likes": likes, "comentarios": coms,
            "engagement_pct": round((likes + coms) / vistas * 100, 2),
            "comentarios_por_mil": round(coms / vistas * 1000, 2),
            "outlier_subs": round(vistas / max(c.get("subs", 0), 1000), 2),
            "outlier_media_canal": round(vistas / max(media_canal, 1), 2),
            "vistas_dia": round(vistas / dias),
            "tags": sn.get("tags", [])[:15], "descripcion": sn.get("description", "")[:400],
            "miniatura": (sn.get("thumbnails", {}).get("maxres") or sn.get("thumbnails", {}).get("high") or {}).get("url"),
        })
    for f in filas:  # puntuación: engagement x sobre-rendimiento frente al canal (log), x alcance (log)
        f["puntuacion"] = round(f["engagement_pct"] * math.log10(1 + f["outlier_media_canal"] * 10)
                                * math.log10(f["vistas"]), 2)
    filas.sort(key=lambda f: f["puntuacion"], reverse=True)
    out = BASE / "investigacion" / "2026-11-22-engagement.json"
    out.write_text(json.dumps({"generado": ahora.isoformat(), "dias": a.dias, "total": len(filas), "videos": filas},
                              ensure_ascii=False, indent=1))
    print(f"{len(filas)} vídeos en español -> {out}")


if __name__ == "__main__":
    main()
