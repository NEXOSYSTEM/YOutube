#!/bin/zsh
# Producción completa de una semana con un solo comando (ver REGLAS-DEL-CANAL.md).
#   ./producir.sh semana-01            → plan + comprobaciones + render de los 3 Shorts y el largo + empaquetado
#   ./producir.sh semana-01 --voz      → además regenera la narración (voz/narrar.py) antes
# Cada paso se cronometra y queda en logs/<fecha>-produccion-<semana>.md
set -e
R=/Users/luis/Desktop/Youtube/Alucinateconelmundo
SEMANA=${1:-semana-01}
PY=$R/voz/.venv/bin/python
export PATH=$R/herramientas/node/bin:$PATH npm_config_cache=$R/herramientas/.npm-cache
FF=$($PY -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
LOG=$R/logs/$(date +%F)-produccion-$SEMANA.md
typeset -A CARP
CARP=(Short01 2026-11-18-short-pez-piedra/short01-pez-piedra Short02 2026-11-18-short-pez-arana/short02-pez-arana \
      Short03 2026-11-18-short-ornitorrinco/short03-ornitorrinco Largo 2026-11-18-largo-peces-venenosos/largo-peces-venenosos)
echo "# Producción $SEMANA — $(date '+%F %T')\n\n| Paso | Tiempo |\n|---|---|" > $LOG
paso() { local t0=$(date +%s); "$@"; local dt=$(( $(date +%s) - t0 )); printf "| %s | %d min %02d s |\n" "$PASO" $((dt/60)) $((dt%60)) >> $LOG; echo "  ⏱ $PASO: $((dt/60)) min $((dt%60)) s"; }
zmodload zsh/datetime
T0=$(date +%s)
cd $R
if [[ "$2" == "--voz" ]]; then PASO="Voz frase a frase + control Whisper"; paso $PY voz/narrar_frases.py --textos guiones/2026-11-18-$SEMANA/textos-voz --salida audio/2026-11-18-$SEMANA; fi
PASO="Tiempos de subtítulos"; paso $PY montaje/scripts/tiempos_subtitulos.py > /dev/null
PASO="Plan de montaje + .srt"; paso $PY montaje/scripts/plan.py > /dev/null
PASO="Descripciones, créditos, etiquetas, miniaturas"; paso $PY montaje/scripts/textos_youtube.py > /dev/null
PASO="Biblioteca de clips"; paso $PY montaje/scripts/biblioteca.py
cd $R/montaje
render() {
  local comp=$1 out=$R/videos/${CARP[$1]}.mp4 conc=$2
  $PY scripts/comprobar.py $comp
  local tmp=${out:r}._render.mp4
  npx remotion render src/index.jsx $comp $tmp --codec=h264 --hardware-acceleration=if-possible --video-bitrate=12M \
     --audio-codec=aac --audio-bitrate=192k --concurrency=$conc --offthreadvideo-cache-size-in-bytes=3000000000 --timeout=120000 --log=error
  $PY $R/montaje/scripts/normalizar.py $tmp $out
  rm -f $tmp
}
for c in Short01 Short02 Short03; do PASO="Render $c"; paso render $c 8; done
PASO="Render Largo"; paso render Largo 8
PASO="Revisión automática"; paso $PY scripts/revisar.py
TT=$(( $(date +%s) - T0 )); printf "| **Total** | **%d min %02d s** |\n" $((TT/60)) $((TT%60)) >> $LOG
echo "Total: $((TT/60)) min $((TT%60)) s · log: $LOG"
