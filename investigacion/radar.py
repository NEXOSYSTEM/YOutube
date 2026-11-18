"""Radar de tendencias del nicho (lunes, miércoles y viernes a las 9:00 desde herramientas/tareas-diarias.sh; ver herramientas/com.alucinate.tareas.plist).

Busca con la API de YouTube los vídeos y Shorts de los últimos 7 días que más rápido crecen en curiosidades
(español e inglés) y en los canales de competencia, y escribe investigacion/AAAA-MM-DD-radar.md.
Solo lee datos públicos con el token que ya usa subida/subir.py. Gasto: ~1.300 de las 10.000 unidades diarias.

Uso: subida/.venv/bin/python investigacion/radar.py [--dias 7]
"""
import argparse, collections, datetime as dt, json, re, subprocess, sys
from pathlib import Path
from zoneinfo import ZoneInfo

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / "subida"))
from googleapiclient.discovery import build  # noqa: E402
from subir import credenciales  # noqa: E402  (mismo token y refresco que la subida)

MADRID = ZoneInfo("Europe/Madrid")
CACHE = BASE / "investigacion" / "radar-canales.json"

# Búsquedas por pilar de la ficha del canal (es + en). Cambiar aquí si cambian los pilares.
BUSQUEDAS = [
    ("Naturaleza extrema", "es", "animales más peligrosos curiosidades"),
    ("Naturaleza extrema", "en", "most dangerous animals facts"),
    ("Lugares imposibles", "es", "lugares prohibidos del mundo"),
    ("Lugares imposibles", "en", "places you are not allowed to visit"),
    ("Historia insólita", "es", "historia curiosa datos que no sabías"),
    ("Tu cuerpo y tu mente", "es", "qué le pasa a tu cuerpo si"),
    ("Ciencia y espacio fácil", "es", "curiosidades del espacio"),
    ("Ciencia y espacio fácil", "en", "what if space facts"),
]
COMPETENCIA = ["SORPRENDENTE", "BÚHO SABIO", "ZooLore", "Andrés Andel", "Curiosidad Animal",
               "Casual Geographic", "Odd Animal Specimens", "1 Minute Animals"]
PALABRAS_VACIAS = set("""de la el los las un una y que en del por con para es se su al lo más mas como qué que no
the of and to a in is you your this that what if for on are with why how it from shorts short""".split())


def segundos(iso):
    m = re.fullmatch(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or "")
    if not m:
        return 0
    d, h, mi, s = (int(x or 0) for x in m.groups())
    return d * 86400 + h * 3600 + mi * 60 + s


def canales_competencia(yt):
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    for nombre in COMPETENCIA:
        if nombre not in cache:  # 100 unidades, solo la primera vez
            r = yt.search().list(part="snippet", q=nombre, type="channel", maxResults=1).execute()
            if r.get("items"):
                cache[nombre] = r["items"][0]["snippet"]["channelId"]
    CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=1))
    return cache


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--dias", type=int, default=7)
    a = p.parse_args()
    yt = build("youtube", "v3", credentials=credenciales(), cache_discovery=False)
    ahora = dt.datetime.now(dt.timezone.utc)
    desde = (ahora - dt.timedelta(days=a.dias)).strftime("%Y-%m-%dT%H:%M:%SZ")

    origen = {}  # videoId -> de dónde salió
    for pilar, idioma, q in BUSQUEDAS:  # 100 unidades cada una
        r = yt.search().list(part="id", q=q, type="video", order="viewCount", publishedAfter=desde,
                             relevanceLanguage=idioma, maxResults=25).execute()
        for it in r.get("items", []):
            origen.setdefault(it["id"]["videoId"], f"{pilar} ({idioma})")
    comp = canales_competencia(yt)
    if comp:  # 1 unidad por canal: últimas subidas de cada uno
        ch = yt.channels().list(part="contentDetails", id=",".join(comp.values())).execute()
        nombre_de = {v: k for k, v in comp.items()}
        for c in ch.get("items", []):
            pl = c["contentDetails"]["relatedPlaylists"]["uploads"]
            r = yt.playlistItems().list(part="contentDetails", playlistId=pl, maxResults=15).execute()
            for it in r.get("items", []):
                if it["contentDetails"].get("videoPublishedAt", "") >= desde:
                    origen.setdefault(it["contentDetails"]["videoId"], f"Competencia: {nombre_de[c['id']]}")

    ids = list(origen)
    videos = []
    for i in range(0, len(ids), 50):  # 1 unidad por cada 50
        r = yt.videos().list(part="snippet,statistics,contentDetails", id=",".join(ids[i:i + 50])).execute()
        videos += r.get("items", [])
    cids = sorted({v["snippet"]["channelId"] for v in videos})
    media = {}
    for i in range(0, len(cids), 50):
        for c in yt.channels().list(part="statistics", id=",".join(cids[i:i + 50])).execute().get("items", []):
            s = c["statistics"]
            media[c["id"]] = int(s.get("viewCount", 0)) / max(int(s.get("videoCount", 1)), 1)

    filas = []
    for v in videos:
        sn, st = v["snippet"], v["statistics"]
        pub = dt.datetime.fromisoformat(sn["publishedAt"].replace("Z", "+00:00"))
        horas = max((ahora - pub).total_seconds() / 3600, 1)
        vistas = int(st.get("viewCount", 0))
        dur = segundos(v["contentDetails"].get("duration"))
        filas.append({"id": v["id"], "titulo": sn["title"], "canal": sn["channelTitle"], "vistas": vistas,
                      "vph": vistas / horas, "x_media": vistas / media.get(sn["channelId"], 0) if media.get(sn["channelId"]) else 0,
                      "dur": dur, "short": dur <= 180, "horas": horas, "origen": origen[v["id"]],
                      "hora_pub": pub.astimezone(MADRID).strftime("%a %H:%M"),
                      "likes": int(st.get("likeCount", 0)), "coment": int(st.get("commentCount", 0))})

    hoy = dt.datetime.now(MADRID)
    out = BASE / "investigacion" / f"{hoy:%Y-%m-%d}-radar.md"
    L = [f"# Radar de tendencias — {hoy:%Y-%m-%d %H:%M}", "",
         f"Vídeos publicados en los últimos {a.dias} días. **Vistas/h** = velocidad; **× media** = vistas frente a la media "
         "de su canal (>3 = está despegando de verdad, no es solo un canal grande).", ""]
    for nombre, es_short in (("Vídeos largos", False), ("Shorts", True)):
        top = sorted([f for f in filas if f["short"] == es_short], key=lambda f: f["vph"], reverse=True)[:10]
        L += [f"## {nombre}: top 10 por velocidad", "",
              "| # | Título | Canal | Vistas | Vistas/h | × media | Duración | Publicado | De dónde |", "|---|---|---|---|---|---|---|---|---|"]
        for i, f in enumerate(top, 1):
            t = f["titulo"].replace("|", "/")
            L.append(f"| {i} | [{t}](https://youtu.be/{f['id']}) | {f['canal']} | {f['vistas']:,} | {f['vph']:,.0f} | "
                     f"{f['x_media']:.1f} | {f['dur'] // 60}:{f['dur'] % 60:02d} | {f['hora_pub']} | {f['origen']} |".replace(",", "."))
        L.append("")
    destacados = sorted(filas, key=lambda f: f["vph"], reverse=True)[:30]
    palabras = collections.Counter(w for f in destacados for w in re.findall(r"[a-záéíóúñü]{4,}", f["titulo"].lower())
                                   if w not in PALABRAS_VACIAS)
    largos = [f["dur"] for f in destacados if not f["short"]]
    con_numero = sum(bool(re.search(r"\d", f["titulo"])) for f in destacados)
    L += ["## Patrones de los 30 más rápidos", "",
          f"- Palabras que más se repiten en los títulos: {', '.join(w for w, _ in palabras.most_common(15))}",
          f"- Duración media de los largos: {sum(largos) / len(largos) / 60:.1f} min" if largos else "- Sin largos en el top",
          f"- Con número en el título: {con_numero} de {len(destacados)}",
          f"- Con pregunta (¿?): {sum('?' in f['titulo'] for f in destacados)} de {len(destacados)}", "",
          "## Ideas para nuestro canal", "",
          "_Pendiente: Claude propone aquí 5 ideas propias (pilar + 3 títulos) al revisar este informe, y Luis elige._", ""]
    out.write_text("\n".join(L), encoding="utf-8")
    (BASE / "investigacion" / f"{hoy:%Y-%m-%d}-radar.json").write_text(json.dumps(filas, ensure_ascii=False, indent=1))
    print(f"Radar listo: {out} ({len(filas)} vídeos)")
    subprocess.run(["osascript", "-e", f'display notification "{len(filas)} vídeos analizados" with title "Alucínate con el mundo" subtitle "Radar listo"'],
                   capture_output=True)


if __name__ == "__main__":
    main()
