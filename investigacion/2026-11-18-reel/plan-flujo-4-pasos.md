# Plan: aplicar el flujo de 4 pasos al canal (pendiente de tu OK)

Nada de esto está construido aún. No toca montaje/, audio/ ni videos/ mientras haya un render en marcha.

## Lo que ya existe (no se rehace)
- Producción con un comando: `producir.sh` (guion → voz → montaje → subtítulos → miniatura, descripción, etiquetas y comentario de créditos).
- Subida programada: `subida/subir.py --publicar "AAAA-MM-DD HH:MM"` ya programa en hora de España y pone la miniatura.

## Paso 1 · Ficha del canal
- Archivo nuevo `ficha-del-canal.md` en la raíz (borrador adjunto). Se añade una línea en AGENTS.md y REGLAS-DEL-CANAL.md: «leer la ficha antes de proponer temas o escribir guiones».

## Paso 2 · Radar de tendencias (nuevo)
- Script nuevo `investigacion/radar.py`: usa la API de YouTube con el token que ya tenemos (no hace falta permiso nuevo). Busca vídeos y Shorts de los últimos 7 días del nicho (español e inglés + canales de competencia de la memoria), calcula vistas por hora y frente a la media de su canal, y escribe `investigacion/AAAA-MM-DD-radar.md` con el top 10, por qué funcionan y 5 ideas propias con pilar y 3 títulos.
- Gasto de cuota: ~2.000 de las 10.000 unidades diarias por pasada.
- Cuándo se ejecuta: ver decisión A.

## Paso 3 · Producción de cualquier semana
- Hoy `producir.sh` lleva escritas a mano las carpetas de la semana 1. Se cambia para que lea las piezas de `guiones/<fecha>-semana-XX/` y sirva para cualquier semana. Objetivo ≤15 min por largo (la prueba de GPU de hoy da ~12 min).
- Miniaturas: 2 variantes por vídeo para que elijas.
- Se hace cuando termine el render que está en marcha.

## Paso 4 · Subida programada y aprendizaje
- Script nuevo `subida/programar.py`: lee la carpeta del vídeo (mp4, título, descripción, etiquetas, miniatura) y llama a `subir.py --publicar`. Solo se ejecuta cuando tú dices «sube».
- Hora: martes 18:00 para el largo; Shorts jueves, sábado y domingo 13:00 (hora de España) hasta tener datos propios.
- Informe a las 48 h (vistas, likes, comentarios) en `informes/AAAA-MM-DD-resultado-<video>.md`. Para CTR y retención hace falta YouTube Analytics: ver decisión B.

## Decisiones que necesito
- **A. ¿Cuándo corre el radar?** Recomiendo que lo lance yo cuando empecemos cada semana (lunes), sin nada automático en tu Mac. La alternativa es una tarea programada del Mac (launchd) lunes y jueves a las 9:00: dura 1 min, no carga modelos, pero el Mac tiene que estar encendido.
- **B. ¿Añadimos YouTube Analytics?** Necesita un permiso nuevo (tendrías que volver a autorizar con un clic) y puede retrasar la auditoría que Google está revisando. Recomiendo esperar a que llegue la respuesta de la auditoría y, mientras, usar las vistas públicas.
