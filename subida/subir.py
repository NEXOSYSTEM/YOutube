"""Alucinate Uploader: sube un vídeo al canal y, si se indica, programa su publicación.

Ejemplos:
  subida/.venv/bin/python subida/subir.py --video videos/2026-11-25/video.mp4 \
      --titulo "10 animales imposibles" --descripcion-archivo guiones/2026-11-25/descripcion.txt \
      --tags "animales,curiosidades" --miniatura miniaturas/2026-11-25/mini.jpg \
      --publicar "2026-11-25 18:00"
  (la hora de --publicar es hora de España; sin --publicar el vídeo queda privado)
"""
import argparse
import datetime as dt
import json
import sys
import time
from pathlib import Path
from zoneinfo import ZoneInfo

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

BASE = Path(__file__).resolve().parent.parent
CRED = BASE / "credenciales"
LOGS = BASE / "logs"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload",
          "https://www.googleapis.com/auth/youtube"]
MADRID = ZoneInfo("Europe/Madrid")


def log(msg):
    linea = f"[{dt.datetime.now(MADRID):%Y-%m-%d %H:%M:%S}] {msg}"
    print(linea, flush=True)
    LOGS.mkdir(exist_ok=True)
    with open(LOGS / f"{dt.date.today():%Y-%m-%d}-subidas.log", "a") as f:
        f.write(linea + "\n")


def credenciales():
    token = CRED / "token.json"
    creds = Credentials.from_authorized_user_file(str(token), SCOPES)
    if not creds.valid:
        creds.refresh(Request())
        token.write_text(creds.to_json())
        token.chmod(0o600)
    return creds


def main():
    p = argparse.ArgumentParser(description="Sube un vídeo a Alucinate Con el mundo")
    p.add_argument("--video", required=True)
    p.add_argument("--titulo", required=True)
    p.add_argument("--descripcion", default="")
    p.add_argument("--descripcion-archivo")
    p.add_argument("--tags", default="", help="separadas por comas")
    p.add_argument("--miniatura")
    p.add_argument("--categoria", default="15", help="15 = Mascotas y animales")
    p.add_argument("--publicar", help="'AAAA-MM-DD HH:MM' hora de España; programa la publicación")
    p.add_argument("--privacidad", default="private", choices=["private", "unlisted", "public"])
    a = p.parse_args()

    video = Path(a.video)
    if not video.is_file():
        sys.exit(f"No existe el vídeo: {video}")
    descripcion = Path(a.descripcion_archivo).read_text() if a.descripcion_archivo else a.descripcion

    status = {"privacyStatus": a.privacidad, "selfDeclaredMadeForKids": False}
    if a.publicar:
        cuando = dt.datetime.strptime(a.publicar, "%Y-%m-%d %H:%M").replace(tzinfo=MADRID)
        if cuando <= dt.datetime.now(MADRID):
            sys.exit("La fecha de --publicar tiene que ser futura")
        status = {"privacyStatus": "private", "selfDeclaredMadeForKids": False,
                  "publishAt": cuando.astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}

    body = {
        "snippet": {"title": a.titulo[:100], "description": descripcion[:5000],
                    "tags": [t.strip() for t in a.tags.split(",") if t.strip()],
                    "categoryId": a.categoria, "defaultLanguage": "es",
                    "defaultAudioLanguage": "es"},
        "status": status,
    }

    yt = build("youtube", "v3", credentials=credenciales())
    log(f"Subiendo {video.name} ({video.stat().st_size / 1e6:.1f} MB): '{a.titulo}'")
    req = yt.videos().insert(part="snippet,status", body=body,
                             media_body=MediaFileUpload(str(video), chunksize=8 * 1024 * 1024, resumable=True))
    resp, intentos = None, 0
    while resp is None:
        try:
            estado, resp = req.next_chunk()
            if estado:
                print(f"  {estado.progress() * 100:.0f}%", flush=True)
        except HttpError as e:
            if e.resp.status in (500, 502, 503, 504) and intentos < 5:
                intentos += 1
                time.sleep(2 ** intentos)
                continue
            raise
    vid = resp["id"]
    log(f"Subido: https://youtu.be/{vid} | estado: {resp['status'].get('privacyStatus')}"
        f"{' | se publica: ' + a.publicar + ' (España)' if a.publicar else ''}")

    if a.miniatura:
        yt.thumbnails().set(videoId=vid, media_body=MediaFileUpload(a.miniatura)).execute()
        log(f"Miniatura puesta: {a.miniatura}")

    print(json.dumps({"id": vid, "url": f"https://youtu.be/{vid}",
                      "studio": f"https://studio.youtube.com/video/{vid}/edit"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
