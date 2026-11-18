#!/bin/zsh
# Producción completa de una semana con un solo comando (ver REGLAS-DEL-CANAL.md).
#   ./producir.sh semana-01            → plan + comprobaciones + render de los 3 Shorts y el largo + empaquetado
#   ./producir.sh semana-01 --voz      → además regenera la narración (frase a frase + control Whisper) antes
# Estado en vivo en ESTADO.md (cada paso y cada 30 s) y notificación de macOS al terminar cada vídeo o si algo falla.
# Cada paso se cronometra y queda en logs/<fecha>-produccion-<semana>.md
R=/Users/luis/Desktop/Youtube/Alucinateconelmundo
SEMANA=${1:-semana-01}
PY=$R/voz/.venv/bin/python
EST="$PY $R/montaje/scripts/estado.py"
export PATH=$R/herramientas/node/bin:$PATH npm_config_cache=$R/herramientas/.npm-cache
LOG=$R/logs/$(date +%F)-produccion-$SEMANA.md
RLOG=$R/montaje/.render-actual.log
typeset -A CARP NOMBRE
CARP=(Short01 2026-11-18-short-pez-piedra/short01-pez-piedra Short02 2026-11-18-short-pez-arana/short02-pez-arana \
      Short03 2026-11-18-short-ornitorrinco/short03-ornitorrinco Largo 2026-11-18-largo-peces-venenosos/largo-peces-venenosos)
NOMBRE=(Short01 "Render Short pez piedra" Short02 "Render Short pez araña" Short03 "Render Short ornitorrinco" Largo "Render vídeo largo")
avisa() { osascript -e "display notification \"$2\" with title \"Alucínate con el mundo\" subtitle \"$1\"" 2>/dev/null || true; }
falla() { ${=EST} error "$1"; avisa "ERROR" "$1"; echo "ERROR: $1"; exit 1; }
PASOS="Plan y subtítulos|Descripciones y biblioteca|Render Short pez piedra|Render Short pez araña|Render Short ornitorrinco|Render vídeo largo|Revisión automática"
[[ "$2" == "--voz" ]] && PASOS="Voz frase a frase + Whisper|$PASOS"
${=EST} inicio "Producción $SEMANA" "$PASOS"
echo "# Producción $SEMANA — $(date '+%F %T')\n\n| Paso | Tiempo |\n|---|---|" > $LOG
paso() { local n="$1"; shift; ${=EST} paso "$n"; local t0=$(date +%s); "$@" || falla "falló: $n"; local dt=$(( $(date +%s) - t0 ));
         ${=EST} hecho "$n" $dt; printf "| %s | %d min %02d s |\n" "$n" $((dt/60)) $((dt%60)) >> $LOG; echo "  ⏱ $n: $((dt/60)) min $((dt%60)) s"; }
T0=$(date +%s)
cd $R
if [[ "$2" == "--voz" ]]; then paso "Voz frase a frase + Whisper" $PY voz/narrar_frases.py --textos guiones/2026-11-18-$SEMANA/textos-voz --salida audio/2026-11-18-$SEMANA; fi
paso "Plan y subtítulos" zsh -c "$PY montaje/scripts/tiempos_subtitulos.py > /dev/null && $PY montaje/scripts/plan.py > /dev/null"
paso "Descripciones y biblioteca" zsh -c "$PY montaje/scripts/textos_youtube.py > /dev/null && $PY montaje/scripts/biblioteca.py"
cd $R/montaje
render() {
  local comp=$1 out=$R/videos/${CARP[$1]}.mp4
  $PY scripts/comprobar.py $comp || return 1
  local tmp=${out:r}._render.mp4
  : > $RLOG
  ( while sleep 30; do ${=EST} progreso $RLOG; done ) & local vig=$!
  npx remotion render src/index.jsx $comp $tmp --codec=h264 --hardware-acceleration=if-possible --video-bitrate=12M \
     --audio-codec=aac --audio-bitrate=192k --concurrency=6 --offthreadvideo-cache-size-in-bytes=3000000000 --timeout=120000 > $RLOG 2>&1
  local rc=$?; kill $vig 2>/dev/null
  [[ $rc == 0 ]] || return 1
  $PY scripts/normalizar.py $tmp $out && rm -f $tmp && avisa "Vídeo terminado" "${NOMBRE[$comp]#Render } listo"
}
for c in Short01 Short02 Short03 Largo; do paso "${NOMBRE[$c]}" render $c; done
paso "Revisión automática" $PY scripts/revisar.py
TT=$(( $(date +%s) - T0 )); printf "| **Total** | **%d min %02d s** |\n" $((TT/60)) $((TT%60)) >> $LOG
${=EST} fin "4 vídeos en videos/ · total $((TT/60)) min $((TT%60)) s"
avisa "Producción terminada" "$SEMANA: 4 vídeos en $((TT/60)) min"
echo "Total: $((TT/60)) min $((TT%60)) s · log: $LOG"
