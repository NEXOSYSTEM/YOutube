"""Autoriza una sola vez el acceso al canal y guarda el token en credenciales/token.json.
Uso: subida/.venv/bin/python subida/autorizar.py
"""
import os
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

BASE = Path(__file__).resolve().parent.parent
CRED = BASE / "credenciales"
SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube",
]

flow = InstalledAppFlow.from_client_secrets_file(str(CRED / "client_secret.json"), SCOPES)
creds = flow.run_local_server(port=0, prompt="consent", access_type="offline")
token = CRED / "token.json"
token.write_text(creds.to_json())
os.chmod(token, 0o600)

yt = build("youtube", "v3", credentials=creds)
canal = yt.channels().list(part="snippet,statistics", mine=True).execute()["items"][0]
print("Autorizado el canal:", canal["snippet"]["title"], "| id:", canal["id"],
      "| suscriptores:", canal["statistics"].get("subscriberCount"))
