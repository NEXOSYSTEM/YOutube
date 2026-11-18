# Ideas útiles del reel y prompt para el canal

## Qué ya tenemos y qué aporta el reel

| Paso del reel | Estado en Alucínate con el Mundo | Qué falta |
|---|---|---|
| 1. Explicar el canal una vez | Hecho: REGLAS-DEL-CANAL.md, AGENTS.md y memoria del proyecto | Un único "documento del canal" con público objetivo y tono, que lea cada agente |
| 2. Cada mañana mirar qué funciona en el nicho | Solo hubo un informe de competencia puntual (18 nov) | **Radar diario automático** de vídeos que despegan en el nicho y propuesta de ideas |
| 3. Hacer el vídeo entero | Hecho: guion, voz Qwen3, Remotion + FFmpeg (producir.sh) | Que salga de una sola orden y en ≤15 min |
| 4. Subir y programar con título, descripción y miniatura | Subida por API funciona (subida/subir.py) | **Programar a la hora de mayor audiencia**, miniatura automática y paquete título+descripción+etiquetas |

## Lo que NO copiamos del reel

- **"Sin que tú toques nada" y "todos los días":** tus reglas mandan. Los guiones se te enseñan antes de producir y nada se sube sin tu visto bueno. El ritmo sigue siendo 1 largo + 3 Shorts por semana.
- **Riesgo de monetización:** YouTube penaliza el "contenido repetitivo / no auténtico" (voz IA + plantilla + metraje de archivo sin aportación propia). Producir a diario en piloto automático es justo lo que más riesgo tiene; por eso mantenemos guiones propios con fuentes, estructuras variadas y tu revisión.
- **Copiar ideas virales tal cual:** se usa la tendencia como señal de tema, nunca se clona el vídeo ni se usan clips de otros canales.

## Prompt listo para usar

Pégalo en el chat del proyecto cuando quieras activarlo:

```
Quiero dar forma al flujo completo del canal «Alucínate con el Mundo» en 4 pasos, respetando todas las reglas de REGLAS-DEL-CANAL.md y la memoria del proyecto (guiones siempre revisados por mí antes de producir, nada se sube sin mi OK, ritmo 1 largo + 3 Shorts por semana, voz Qwen3 «ryan» x1,25, clips de vídeo con licencia comercial, subtítulos, carpetas con fecha).

PASO 1 – Ficha del canal (una sola vez)
Crea ficha-del-canal.md en la carpeta del proyecto: de qué va el canal, público objetivo (edad, países, qué le engancha), tono y estilo de narración, 5 pilares de temas, estructura de largos y Shorts, qué no hacemos nunca. Que todos los agentes la lean antes de trabajar. Enséñamela para aprobarla.

PASO 2 – Radar de tendencias (automático, lunes y jueves por la mañana)
Crea una tarea programada que, con la API de YouTube, revise los vídeos y Shorts de los últimos 7 días en nuestro nicho (curiosidades del mundo en español y en inglés, canales de competencia de la memoria) y detecte los que más rápido crecen (vistas por hora frente a la media del canal). Guarda un informe en investigacion/AAAA-MM-DD-radar.md con: top 10 vídeos, por qué funcionan (gancho, título, miniatura, duración) y 5 ideas propias para nuestro canal, cada una con su pilar y 3 títulos posibles. Avísame con el resumen y deja que yo elija las ideas de la semana.

PASO 3 – Producción con un solo comando
Con las ideas que yo elija: guion con fuentes → me lo enseñas → tras mi OK, voz + clips + montaje + subtítulos con ./producir.sh, objetivo ≤15 min para el largo. Que el flujo genere también: miniatura (2 variantes), título, descripción con capítulos y créditos, etiquetas, y el texto fijado para comentarios. Todo en la carpeta con fecha del vídeo.

PASO 4 – Subida programada (solo con mi OK)
Prepara la subida como "programada" a la hora de mayor audiencia (consulta YouTube Analytics; mientras no haya datos, martes 18:00 hora de España para el largo y Shorts repartidos en la semana). No subas nada hasta que yo diga «sube». Después de publicar, a las 48 h haz un mini informe (CTR, retención, vistas) y apunta qué aprender para el siguiente.

Antes de construir nada, enséñame un plan corto con qué archivos o tareas nuevas vas a crear y qué cambia del flujo actual, y espera a que lo apruebe. Avísame al empezar y terminar cada fase larga.
```
