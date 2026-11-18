#!/bin/zsh
# Renderiza una composición y normaliza el audio a −14 LUFS (estándar de YouTube).
# Uso: ./render.sh <Composición> <salida.mp4>     p. ej. ./render.sh Largo ../videos/2026-11-18-semana-01/largo-peces-venenosos.mp4
set -e
R=/Users/luis/Desktop/Youtube/Alucinateconelmundo
export PATH=$R/herramientas/node/bin:$PATH npm_config_cache=$R/herramientas/.npm-cache
FF=$($R/voz/.venv/bin/python -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
cd $R/montaje
# Comprobaciones obligatorias (voz a x1,25 real y ≥70 % de vídeo); si fallan, no se renderiza
$R/voz/.venv/bin/python scripts/comprobar.py "$1"
TMP="${2:r}._sin_normalizar.mp4"
npx remotion render src/index.jsx "$1" "$TMP" --codec=h264 --crf=18 --audio-codec=aac --audio-bitrate=192k --log=error
$FF -y -loglevel error -i "$TMP" -c:v copy -af "loudnorm=I=-14:TP=-1.5:LRA=11" -ar 48000 -c:a aac -b:a 192k -movflags +faststart "$2"
rm -f "$TMP"
$FF -i "$2" -af ebur128 -f null - 2>&1 | grep -E "^\s+I:" | head -1
