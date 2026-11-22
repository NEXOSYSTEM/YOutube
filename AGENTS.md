# Instrucciones para agentes (Antigravity, Claude, Gemini…)

Responde siempre en **español**. Proyecto del canal de YouTube «Alucínate con el mundo» de Luis. Totalmente separado de AlphaHub.

Reglas obligatorias (detalle en `REGLAS-DEL-CANAL.md`):

1. Enseña siempre los guiones a Luis antes de producir un vídeo.
2. **Subida directa y programada** (Luis, 2026-11-22): con el guion aprobado, sube cada pieza en cuanto pase `comprobar.py`, completa (título, descripción, etiquetas, miniatura, subtítulos, créditos fijados, marca de IA si la lleva) y programada a las 18:00 de su día con `subida/programar.py`. Máx. 4 subidas al día. Sin guion aprobado, no se sube nada. Detalle en REGLAS-DEL-CANAL.md, regla 2.
3. Clips de vídeo del tema antes que fotos (≥ 70 % de vídeo).
4. Animales siempre completos, de cabeza a cola; primeros planos solo si el guion habla de esa parte.
5. Voz: ElevenLabs «Thimsen» (español de España; Qwen3-TTS «ryan» de reserva), x1,25 real, revisada con Whisper.
6. Siempre subtítulos (quemados + `.srt`).
7. Largos: gancho 15–30 s → intro de la lupa → contenido. Shorts: sin intro, logo pequeño arriba a la izquierda.
8. Solo licencias con uso comercial; créditos en `creditos.md`.
9. Cada vídeo en su carpeta con fecha dentro de `videos/`.
10. Actualiza `ESTADO.md` en tareas largas y avisa a Luis al empezar, al terminar y si algo falla.
11. Nunca subas al repo `credenciales/`, `herramientas/claves-stock.txt`, tokens ni material pesado.
12. Planos con IA: Veo (Gemini) solo para escenas concretas; reglas, cuota y registro en `docs/veo.md`. Archivar cada clip con `herramientas/veo/archivar.py`.
13. **REGLA GLOBAL (Luis, 2026-11-22): antes de compactar el contexto**, y al cerrar cada tarea larga, actualiza el contexto y los documentos en GitHub (este repo, por PR) y en cerebro (bóveda Obsidian `/Users/luis/Desktop/Youtube/Youtube`).
14. **DURACIÓN DE LOS LARGOS: de 6 a 8 min como máximo** (Luis, 2026-11-22). Sustituye a los 8-12 min de antes. A x1,25 la voz va a ≈210 palabras/min, así que un guion largo tiene entre ≈1.250 y ≈1.650 palabras narradas. Si sale más largo, se recorta; si sale más corto de 6 min, se amplía. Los Shorts siguen en ≈60 s.
