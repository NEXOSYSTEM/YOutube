"""Sube un vídeo de videos/<carpeta>/ y lo deja programado. SOLO cuando Luis dice «sube».

Lee de la carpeta: el .mp4, descripcion.txt (la línea «Título: …» es el título), etiquetas.txt y miniatura.jpg.
Sin --cuando elige el siguiente hueco del calendario del canal (hora de España):
  largo  → martes 18:00 · Shorts → jueves, sábado y domingo 13:00 (el primero libre).
Deja videos/<carpeta>/publicacion.json, que usa subida/informe48h.py.

Uso: subida/.venv/bin/python subida/programar.py videos/2026-11-25-largo-xxx [--cuando "2026-11-25 18:00"] [--titulo "…"] [--prueba]
"""
import argparse, datetime as dt, json, subprocess, sys
from pathlib import Path
from zoneinfo import ZoneInfo

BASE = Path(__file__).resolve().parent.parent
MADRID = ZoneInfo("Europe/Madrid")
HUECOS = {"largo": [(1, 18, 0)], "short": [(3, 13, 0), (5, 13, 0), (6, 13, 0)]}  # (día 0=lunes, hora, min)


def ocupados():
    return {json.loads(p.read_text())["publica"] for p in BASE.glob("videos/*/publicacion.json")}


def siguiente_hueco(tipo):
    ahora, usados = dt.datetime.now(MADRID), ocupados()
    for d in range(1, 60):
        dia = (ahora + dt.timedelta(days=d)).date()
        for wd, h, m in HUECOS[tipo]:
            if dia.weekday() == wd:
                t = f"{dia:%Y-%m-%d} {h:02d}:{m:02d}"
                if t not in usados:
                    return t
    sys.exit("No encuentro hueco libre en 60 días")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("carpeta")
    p.add_argument("--cuando", help="'AAAA-MM-DD HH:MM' hora de España")
    p.add_argument("--titulo")
    p.add_argument("--prueba", action="store_true", help="enseña lo que haría sin subir nada")
    a = p.parse_args()
    c = (BASE / a.carpeta).resolve() if not Path(a.carpeta).is_absolute() else Path(a.carpeta)
    if (c / "publicacion.json").exists():
        sys.exit(f"Ya está subido: {json.loads((c / 'publicacion.json').read_text())['url']}")
    mp4 = [f for f in c.glob("*.mp4") if not f.name.endswith("._render.mp4")]
    if len(mp4) != 1:
        sys.exit(f"Esperaba un solo .mp4 en {c}")
    tipo = "short" if "-short-" in c.name else "largo"
    lineas = (c / "descripcion.txt").read_text(encoding="utf-8").splitlines()
    titulo = a.titulo
    if lineas and lineas[0].startswith("Título:"):
        titulo = titulo or lineas[0][len("Título:"):].strip()
        lineas = lineas[1:]
    if not titulo and (c / "titulo.txt").exists():
        titulo = (c / "titulo.txt").read_text(encoding="utf-8").strip()
    if not titulo:
        sys.exit("Falta el título: pon --titulo, una línea «Título: …» en descripcion.txt o titulo.txt")
    desc = "\n".join(lineas).strip() + "\n"
    cuando = a.cuando or siguiente_hueco(tipo)
    tags = (c / "etiquetas.txt").read_text(encoding="utf-8").strip() if (c / "etiquetas.txt").exists() else ""
    tmp = c / ".descripcion-subida.txt"
    tmp.write_text(desc, encoding="utf-8")
    cmd = [sys.executable, str(BASE / "subida" / "subir.py"), "--video", str(mp4[0]), "--titulo", titulo,
           "--descripcion-archivo", str(tmp), "--tags", tags, "--publicar", cuando,
           "--categoria", "27"]  # 27 = Educación (curiosidades del mundo)
    if (c / "miniatura.jpg").exists():
        cmd += ["--miniatura", str(c / "miniatura.jpg")]
    print(f"{tipo} · «{titulo}» · se publica {cuando} (España)")
    if a.prueba:
        print("Prueba: no se ha subido nada.\n" + " ".join(cmd[:2]) + " …")
        tmp.unlink()
        return
    r = subprocess.run(cmd, capture_output=True, text=True)
    tmp.unlink(missing_ok=True)
    print(r.stdout[-2000:], r.stderr[-2000:], sep="\n")
    if r.returncode:
        sys.exit("La subida ha fallado (ver logs/<fecha>-subidas.log)")
    res = json.loads(r.stdout.strip().splitlines()[-1])
    (c / "publicacion.json").write_text(json.dumps({**res, "titulo": titulo, "publica": cuando, "tipo": tipo},
                                                   ensure_ascii=False, indent=1))
    print(f"Programado: {res['url']} · {cuando}")


if __name__ == "__main__":
    main()
