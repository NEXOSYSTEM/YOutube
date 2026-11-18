#!/bin/zsh
# Tarea del Mac (launchd, cada día a las 9:00). Instalar desde la raíz del proyecto:
#   sed "s#__RAIZ__#$PWD#" herramientas/com.alucinate.tareas.plist > ~/Library/LaunchAgents/com.alucinate.tareas.plist && launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.alucinate.tareas.plist
# Lunes, miércoles y viernes: radar de tendencias. Todos los días: informes a las 48 h de lo publicado.
# No carga ningún modelo ni deja nada en segundo plano; dura ~1 min.
R=${0:A:h:h}
PY=$R/subida/.venv/bin/python
LOG=$R/logs/$(date +%F)-tareas-diarias.log
cd $R
{ echo "== $(date '+%F %T')"
  case $(date +%u) in 1|3|5) $PY investigacion/radar.py || osascript -e 'display notification "El radar ha fallado (ver logs)" with title "Alucínate con el mundo"';; esac
  $PY subida/informe48h.py
} >> $LOG 2>&1
