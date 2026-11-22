# Reglas del canal «Alucínate con el mundo»

Reglas fijadas por Luis. Se aplican a todos los vídeos (largos y Shorts). Última actualización: 2026-11-22.

## Proceso

0. **Ficha del canal:** antes de proponer temas o escribir guiones, títulos o miniaturas, se lee `ficha-del-canal.md` (público, tono, pilares y formato).
0b. **Radar de tendencias 3 veces por semana** (lunes, miércoles y viernes a las 9:00, tarea del Mac): `investigacion/radar.py` deja `investigacion/AAAA-MM-DD-radar.md` con lo que despega en el nicho. Las ideas de la semana salen de ahí y las elige Luis.
1. **Guiones antes del vídeo:** Luis ve y aprueba los guiones antes de que se desarrolle ningún vídeo. Sin su «sí» directo no se hace el render final; solo pruebas de estilo de 20–30 s.
2. **Subida directa y programada** (Luis, 2026-11-22; sustituye a «nada se sube sin que Luis lo pida»). Con el guion aprobado por Luis, cada pieza se sube en cuanto está terminada y pasa `comprobar.py`, con `subida/programar.py`: en privado y programada a la hora de publicación de su día (18:00, hora de España). La subida va COMPLETA: título, descripción (primera línea que pide comentarios, capítulos en los largos y créditos), etiquetas, miniatura, subtítulos `.srt`, categoría Educación, idioma español, «no es contenido para niños», comentario de créditos fijado (en los Shorts, con el enlace al largo del mismo día) y la marca «contenido alterado o sintético» si lleva planos de IA. Después se comprueba con la API que todo quedó puesto y se avisa a Luis con el enlace y la hora programada. Máximo 4 subidas al día (cuota de la API). Sin guion aprobado no se sube nada. A las 48 h `subida/informe48h.py` deja el resultado en `informes/`. Los vídeos se quedan en `videos/<fecha>-<pieza>/`.
3. **Una carpeta por vídeo, con fecha:** `videos/AAAA-MM-DD-largo-<tema>/` y `videos/AAAA-MM-DD-short-<tema>/`. Cada una lleva el mp4, el `.srt`, `miniatura.jpg`, `descripcion.txt` (con capítulos y créditos), `comentario-creditos.txt` y `etiquetas.txt`. Las pruebas van en `videos/AAAA-MM-DD-pruebas/`.
3b. **Avisar siempre de en qué punto está el trabajo.** `ESTADO.md`, en la raíz del proyecto, se reescribe en cada paso y cada 30 s con la fase, el vídeo, el %, la hora de inicio, la hora estimada de fin, la última actualización y el estado (EN MARCHA, TERMINADO, ERROR o ESPERANDO A LUIS). macOS muestra una notificación al terminar cada vídeo y si algo falla. Claude avisa al empezar y al terminar cada fase larga (con hora estimada) y cada 15 min mientras siga en marcha.
4. **Datos verificados:** antes del render se comprueban los datos dudosos del guion. Si alguno no tiene fuente fiable, se propone otra frase a Luis.
4b. **REGLA GLOBAL: documentar antes de compactar** (Luis, 2026-11-22). Antes de compactar el contexto, y al cerrar cada tarea larga, se actualizan el contexto y los documentos en los dos sitios: GitHub (repo NEXOSYSTEM/YOutube, por PR) y cerebro (bóveda Obsidian `/Users/luis/Desktop/Youtube/Youtube`). Vale para todos los hilos y agentes (Claude, Antigravity…).
4c. **DURACIÓN DE LOS LARGOS: de 6 a 8 min como máximo** (Luis, 2026-11-22). Sustituye a los 8-12 min de antes. A x1,25 la voz va a ≈210 palabras/min, así que un guion largo tiene entre ≈1.250 y ≈1.650 palabras narradas. Si sale más largo, se recorta; si sale más corto de 6 min, se amplía. Los Shorts siguen en ≈60 s.
4d. **Llamada a suscribirse con animación** (Luis, 2026-11-22). Todos los vídeos llevan «Suscríbete para ver más contenido y activa la campanita» con su animación (botón «SUSCRIBIRSE» que se pulsa, pasa a «SUSCRITO» y una campana que suena), en un componente Remotion reutilizable. En los largos sale dos veces: justo después de la intro de la lupa (solo rótulo y sonido) y en el cierre, narrada. En los Shorts, una versión de 2 s al final, sin voz nueva.

## Voz

5. **Siempre a x1,25 real y siempre en español de España:** voz de ElevenLabs «Thimsen» (castellano de España), aprobada por Luis el 2026-11-18. La voz final = voz cruda / 1,25 (`atempo=1.25` una sola vez; ver `voz/config-voz.md`).
   - Se genera con `voz/narrar_elevenlabs.py` (o `./producir.sh semana-XX --voz`), que guarda en `audio/.../duraciones.json` la duración cruda y la final de cada bloque.
   - Cada pieza se comprueba con Whisper (idioma y texto frente al guion); si falla, se repite (máx. 3 intentos).
   - Reserva: si ElevenLabs no está disponible o no pasa el control, esa pieza se narra con Qwen3-TTS «ryan» frase a frase (`voz/narrar_frases.py`).
   - El montaje no estira ni acelera la voz: los tiempos de escenas y subtítulos se ajustan a la voz, nunca al revés.

## Imagen

6. **Vídeo antes que foto:** cada escena usa clips de VÍDEO del tema siempre que existan con licencia válida. Las fotos son el último recurso y siempre llevan movimiento (Ken Burns). Si un animal no tiene vídeo con licencia válida, se usa vídeo del entorno (arrecife, fondo marino, río…) mezclado con sus fotos, y se avisa a Luis.
6b. **El animal se ve ENTERO**, de la cabeza a la cola. Sus fotos y clips se encuadran en modo «contain» y el hueco se rellena con la misma imagen desenfocada y oscurecida. Nunca se recorta el animal para llenar la pantalla (clave en los Shorts verticales). El zoom sobre el animal es como mucho del 8 %, sin paneos y sin cortar ni la cabeza ni la cola. Se priorizan los planos con el animal completo; los primeros planos de una parte (espinas, boca…) solo cuando el guion habla de ella y después de haberlo visto entero.
6c. **El plano de presentación de cada animal** (rótulo «#N» y ficha) usa metraje real de esa especie o su foto, nunca vídeo de otro animal.
6d. **Más animal que relleno** (Luis, 2026-11-18): en cada vídeo el animal del tema sale más tiempo que cualquier otro plano. Si no hay vídeo libre de la especie, mandan SUS fotos (con movimiento y entero), no vídeos de entorno; el entorno (río, arrecife, playa) solo como apoyo puntual. `comprobar.py` mide el % de animal en pantalla (objetivo ≥ 50 %; de momento avisa, no detiene).
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
- el porcentaje de vídeo en los planos de la pieza baja del 70 % (las fotos del propio animal cuentan como vídeo, regla 6d).
Y avisa si el animal sale menos del 50 % del tiempo.
