# Veo (Gemini) en el canal: decisiones y flujo

Acordado con Luis el 2026-11-18. Sustituye a la versión anterior de este documento.

## 1. Quién hace qué

- **Claude es el orquestador.** Lee el guion, saca la lista de planos, pide a Veo los que tocan, archiva y registra cada clip, y monta el vídeo final.
- **Veo (app de Gemini) hace solo la imagen de escenas concretas.** No hace el vídeo entero: genera clips sueltos de 10 s, sin nuestra voz, sin subtítulos y sin el orden del guion.
- **El pipeline de siempre hace todo lo demás:** voz (Qwen3-TTS «ryan», España, x1,25), clips de stock libres, fotos con movimiento, mapas, gráficos, subtítulos, intro, música y un único render con Remotion en la GPU del Mac.
- Antigravity puede abrir el repo y leer `AGENTS.md`, pero no genera vídeo.

## 2. Cuándo se usa Veo (cuota pequeña)

La cuota es pequeña, así que Veo solo se usa para:

1. La **presentación (#N) de los animales que no tienen vídeo libre** de su especie.
2. **Acciones clave que pide el guion y no existen en stock**: abrir la boca, enterrarse, hincharse, cazar...
3. El **plano gancho de un Short** si no hay vídeo libre.

Antes de pedir un plano, se comprueba `material/biblioteca/` y el catálogo de la semana. Si ya hay vídeo libre de esa especie, no se gasta cuota.

## 3. Cuota medida (cuenta de trabajo de Luis, plan Pro)

| Dato | Valor |
|---|---|
| Clips por ventana | **4** (2026-11-18, de 21:02 a 21:18; el 5.º ya aparece desactivado) |
| Reinicio | Gemini avisó: «hasta el 19/11 a las 01:41». No es a las 24 h ni a medianoche. |
| Por clip | 10 s, 1280x720, con audio. Tarda de 1,5 a 2 min. |
| Por semana | Pendiente de medir. Estimación: unos 8 clips útiles, suficientes para las escenas del punto 2. |

El seguimiento está en `material/medicion-cuota-veo.md` en el Mac.

## 4. Cómo se generan

- Desde el Chrome del Mac de Luis, con su sesión en gemini.google.com: **+ › Crear vídeo**, Horizontal (16:9) para el largo y Vertical (9:16) para los Shorts.
- **Prompts en inglés.** Deben describir la **acción y el movimiento de la escena del guion**, con el **animal entero de cabeza a cola**, sin texto, sin marcas y sin personas.
- Hay que describir la **morfología real** de la especie. El primer pez piedra salió con aspecto de cabracho. Añadir, por ejemplo: «short, thick, lumpy, rock-shaped… It is NOT a scorpionfish».
- Plantilla: `Realistic underwater nature documentary footage, <especie (nombre científico)>, <aspecto real>, full body visible from head to tail, <acción del guion>, <entorno>, <movimiento de cámara>, natural light, sharp focus. No text, no watermark, no people.`

## 5. Dónde se guardan y cómo se registran

- **Chrome descarga directamente en** `material/`, sin preguntar. En `chrome://settings/downloads`, la ubicación es `.../Alucinateconelmundo/material` y «Preguntar ubicación» está desactivado.
- Claude archiva cada clip con `herramientas/veo/archivar.py`. El script:
  - lo copia a `material/<fecha>-semana-NN/<animal>/NN_veo_<animal>_NN.mp4`, junto al resto del material de ese vídeo;
  - añade una fila en `material/registro-veo.csv` con id, fecha, archivo, semana, pieza, escena, tema, especie, formato, duración, resolución, herramienta, estado y prompt;
  - añade una fila en `creditos.md` de la semana: «Generado con IA (Veo, Google)»;
  - mueve el original a `material/_entrada-veo/procesados/`.
- Cada semana tiene su plan de planos para Veo en `material/plan-veo-<fecha>-semana-NN.md`.

## 6. Condiciones de uso

- Términos de Servicio de Google (vigentes desde el 30-07-2026): «Google won't claim ownership over that content». No prohíben el uso comercial, aunque tampoco lo autorizan de forma expresa. Al ser una cuenta de Workspace, puede aplicar además el contrato de la empresa. Luis confirma que tiene permiso.
- Está prohibido hacer pasar contenido de IA por contenido hecho por una persona.
- Los clips llevan SynthID, una marca invisible.
- **Al subir a YouTube**, marcar «Contenido alterado o sintético» si el vídeo usa estos clips realistas. En la descripción, poner «Planos generados con IA (Veo, Google)».
- Detalle en `material/licencia-veo.md`, en el Mac.

## 7. Estado a 2026-11-18

| id | Archivo | Escena | Estado |
|---|---|---|---|
| veo-0001 | pez-piedra/30_veo_pez_piedra_01.mp4 | 13.5 / S1.6 | descartado (parece cabracho) |
| veo-0002 | pez-piedra/31_veo_pez_piedra_02.mp4 | 13.5 / S1.6 | bueno |
| veo-0003 | pez-arana/30_veo_pez_arana_01.mp4 | 8.1 / S2.2 | candidato |
| veo-0004 | pez-arana/31_veo_pez_arana_02.mp4 | 8.2 / S2.3 | candidato (aleta poco levantada) |

Siguientes en la lista: pez piedra camuflado que se revela, ornitorrinco en vertical, blenio colmillo, pez gato, tiburón de Groenlandia, pez globo hinchándose, etc.
