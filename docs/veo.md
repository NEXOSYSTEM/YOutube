# Planos generados con Veo (Gemini)

Para los planos que no existen con licencia libre (pez piedra entero nadando, pez araña, ornitorrinco bajo el agua…).

## Reparto

- **Veo** genera clips sueltos de ~8 s, un plano por escena del guion.
- **Nuestro pipeline** (voz, subtítulos, música, intro, montaje) sigue montando el vídeo. Veo no hace el vídeo entero: no usa la voz del canal ni subtítulos ni el orden del guion.

## Reglas para los prompts

- Animal **completo de cabeza a cola**, realista, estilo documental de naturaleza.
- Sin texto, sin rótulos, sin marcas de agua, sin personas salvo que el guion lo pida.
- 16:9 para el vídeo largo; 9:16 para los Shorts.
- Plantilla: `Realistic nature documentary footage, <animal y especie>, full body visible from head to tail, <acción>, <entorno>, natural light, steady camera, shallow depth of field, 4K, no text, no watermark.`

## Dónde se guardan

`material/<fecha>-veo/` en el Mac, con `prompts.txt` (prompt de cada clip) y `licencia-veo.md` (condiciones de uso comercial). En `creditos.md` del vídeo se anota «Generado con Veo (Google)».
