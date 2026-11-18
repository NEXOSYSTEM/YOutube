# Reglas del canal «Alucínate con el mundo»

Reglas fijadas por Luis. Se aplican a todos los vídeos (largos y Shorts). Última actualización: 2026-11-18.

## Proceso

1. **Guiones antes del vídeo:** Luis ve y aprueba los guiones antes de que se desarrolle ningún vídeo. Sin su «sí» directo no se hace el render final; solo pruebas de estilo de 20–30 s.
2. **Nada se sube a YouTube** sin que Luis lo pida. Los vídeos se quedan en `videos/<fecha>-<pieza>/`.
3. **Una carpeta por vídeo, con fecha:** `videos/AAAA-MM-DD-largo-<tema>/` y `videos/AAAA-MM-DD-short-<tema>/`. Cada una lleva el mp4, el `.srt`, `miniatura.jpg`, `descripcion.txt` (con capítulos y créditos), `comentario-creditos.txt` y `etiquetas.txt`. Las pruebas van en `videos/AAAA-MM-DD-pruebas/`.
3b. **Avisar siempre de en qué punto está el trabajo.** `ESTADO.md`, en la raíz del proyecto, se reescribe en cada paso y cada 30 s con la fase, el vídeo, el %, la hora de inicio, la hora estimada de fin, la última actualización y el estado (EN MARCHA, TERMINADO, ERROR o ESPERANDO A LUIS). macOS muestra una notificación al terminar cada vídeo y si algo falla. Claude avisa al empezar y al terminar cada fase larga (con hora estimada) y cada 15 min mientras siga en marcha.
4. **Datos verificados:** antes del render se comprueban los datos dudosos del guion. Si alguno no tiene fuente fiable, se propone otra frase a Luis.

## Voz

5. **Siempre a x1,25 real y siempre en español de España:** voz Qwen3-TTS «ryan», acento de España neutro. La voz final = voz cruda / 1,25 (`atempo=1.25` una sola vez; ver `voz/config-voz.md`).
   - Se genera con `voz/narrar.py`, que guarda en `audio/.../duraciones.json` la duración cruda y la final de cada bloque.
   - Como el modelo no habla siempre al mismo ritmo, se generan varias tomas y se queda la más fluida (objetivo ≥ 160 palabras/min), sin cambiar nunca el x1,25.
   - Se genera frase a frase (trozos de ≤ 2 frases) con `lang_code spanish`, la instrucción de acento de España en cada llamada y temperatura baja (`voz/narrar_frases.py`). Cada frase se comprueba con Whisper (idioma y texto frente al guion); si falla, se repite (máx. 5 intentos) y si no pasa se marca para revisión.
   - El montaje no estira ni acelera la voz: los tiempos de escenas y subtítulos se ajustan a la voz, nunca al revés.

## Imagen

6. **Vídeo antes que foto:** cada escena usa clips de VÍDEO del tema siempre que existan con licencia válida. Las fotos son el último recurso y siempre llevan movimiento (Ken Burns). Si un animal no tiene vídeo con licencia válida, se usa vídeo del entorno (arrecife, fondo marino, río…) mezclado con sus fotos, y se avisa a Luis.
6b. **El animal se ve ENTERO**, de la cabeza a la cola. Sus fotos y clips se encuadran en modo «contain» y el hueco se rellena con la misma imagen desenfocada y oscurecida. Nunca se recorta el animal para llenar la pantalla (clave en los Shorts verticales). El zoom sobre el animal es como mucho del 8 %, sin paneos y sin cortar ni la cabeza ni la cola. Se priorizan los planos con el animal completo; los primeros planos de una parte (espinas, boca…) solo cuando el guion habla de ella y después de haberlo visto entero.
6c. **El plano de presentación de cada animal** (rótulo «#N» y ficha) usa metraje real de esa especie o su foto, nunca vídeo de otro animal.
7. **Objetivo: ≥ 70 % de vídeo** en el tiempo de planos (sin contar los gráficos propios: mapas, esquemas, contadores).
8. **Licencias:** solo CC0, dominio público (NOAA, USFWS, NPS, USGS, NASA…), CC BY, CC BY-SA (marcado «BY-SA», solo si no hay alternativa), Mixkit Free License, y Pexels/Pixabay si hay clave. Nunca NC ni ND, ni clips de YouTube o TikTok. Todo queda en `material/<semana>/creditos.md`.
9. **Música y efectos:** sintetizados por código (`montaje/scripts/sonido_*.py`), sin licencias de terceros. Otra opción es la Biblioteca de audio de YouTube.

## Estilo y marca

10. **Vídeos largos:** gancho → intro de 8 s (`logo/intro-2026-11-18/intro-lupa-sonido.mp4`) → contenido. **Shorts:** sin intro, con el logo pequeño arriba a la izquierda y el gancho escrito desde el primer fotograma.
11. **Subtítulos siempre:** quemados en el vídeo y además el `.srt` aparte. En el largo, frases de 1 o 2 líneas abajo; en los Shorts, palabra a palabra.
12. **Tema visual:** `montaje/src/tema.js` (paleta y tipografía) y la identidad en `logo/final-2026-11-18/`. Tipografía Outfit pendiente del sí de Luis a la descarga.
13. **Audio final:** −14 LUFS y pico ≤ −1 dB.

## Comprobación automática en cada render

`montaje/render.sh` ejecuta `montaje/scripts/comprobar.py` antes de renderizar y **se detiene** si:
- algún audio de narración no cumple final = crudo / 1,25 (±1 %), o el montaje lo recorta o estira;
- el porcentaje de vídeo en los planos de la pieza baja del 70 %.
