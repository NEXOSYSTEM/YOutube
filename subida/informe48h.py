"""Informe de resultados a las 48 h de publicar (se lanza cada día desde herramientas/tareas-diarias.sh).

Para cada videos/*/publicacion.json publicado hace ≥48 h y sin informe, escribe
informes/AAAA-MM-DD-resultado-<carpeta>.md con vistas, likes, comentarios y la comparación con los demás vídeos.
Solo datos públicos (CTR y retención necesitan YouTube Analytics, aún no activado).
"""
import datetime as dt, json, sys
from pathlib import Path
from zoneinfo import ZoneInfo

BASE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE / "subida"))
from googleapiclient.discovery import build  # noqa: E402
from subir import credenciales  # noqa: E402

MADRID = ZoneInfo("Europe/Madrid")


def main():
    ahora = dt.datetime.now(MADRID)
    pubs = []
    for p in sorted(BASE.glob("videos/*/publicacion.json")):
        d = json.loads(p.read_text())
        d["carpeta"] = p.parent.name
        d["cuando"] = dt.datetime.strptime(d["publica"], "%Y-%m-%d %H:%M").replace(tzinfo=MADRID)
        pubs.append(d)
    pend = [d for d in pubs if ahora - d["cuando"] >= dt.timedelta(hours=48) and not d.get("informe")]
    if not pend:
        print("Sin informes pendientes"); return
    yt = build("youtube", "v3", credentials=credenciales(), cache_discovery=False)
    stats = {}
    ids = [d["id"] for d in pubs if ahora > d["cuando"]]
    for i in range(0, len(ids), 50):
        for v in yt.videos().list(part="statistics", id=",".join(ids[i:i + 50])).execute().get("items", []):
            stats[v["id"]] = {k: int(v["statistics"].get(k, 0)) for k in ("viewCount", "likeCount", "commentCount")}
    for d in pend:
        s = stats.get(d["id"], {})
        mismos = [stats[x["id"]]["viewCount"] for x in pubs if x["tipo"] == d["tipo"] and x["id"] in stats and x["id"] != d["id"]]
        media = sum(mismos) / len(mismos) if mismos else None
        out = BASE / "informes" / f"{ahora:%Y-%m-%d}-resultado-{d['carpeta']}.md"
        vistas = s.get("viewCount", 0)
        L = [f"# Resultado a las 48 h: {d['titulo']}", "",
             f"- Vídeo: {d['url']} ({d['tipo']}) · publicado {d['publica']} (España)",
             f"- Vistas: **{vistas:,}**".replace(",", "."),
             f"- Me gusta: {s.get('likeCount', 0)} ({100 * s.get('likeCount', 0) / max(vistas, 1):.1f} % de las vistas)",
             f"- Comentarios: {s.get('commentCount', 0)}",
             f"- Frente a la media de nuestros {d['tipo']}s: " + (f"{vistas / media:.1f}×" if media else "es el primero, aún no hay media"),
             "", "## Qué aprender para el siguiente", "",
             "_Pendiente: Claude lo completa al revisar el informe (título, miniatura, gancho, hora)._", ""]
        out.write_text("\n".join(L), encoding="utf-8")
        p = BASE / "videos" / d["carpeta"] / "publicacion.json"
        j = json.loads(p.read_text()); j["informe"] = out.name
        p.write_text(json.dumps(j, ensure_ascii=False, indent=1))
        print("Informe:", out)


if __name__ == "__main__":
    main()
