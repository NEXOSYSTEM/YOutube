# Vídeos con más engagement en el nicho (22-nov-2026)

**Para qué sirve:** sacar patrones de los vídeos en español que más enganchan en nuestros 4 temas (animales, informática, geografía e historia) y aplicarlos a guiones, títulos, miniaturas y al radar.

## Cómo se ha hecho

- **NexLev:** la cuenta de Luis está en el plan gratis. El Niche Finder y los "outliers" piden NexLev Pro (42 €/mes, o 39 €/mes en plan anual). Luis eligió no pagarlo y hacer el análisis gratis.
- **API de YouTube (datos públicos, sin subir nada):** 13 búsquedas en español (3-4 por tema), ordenadas por visualizaciones, del último año (23-nov-2025 a 22-nov-2026), más los últimos 50 vídeos de 4 canales de competencia en español (SORPRENDENTE, BÚHO SABIO, Andrés Andel, Curiosidad Animal).
- **Muestra:** 493 vídeos en español con más de 20.000 visualizaciones; 313 de ellos pasan de 50.000 visualizaciones y no son de la competencia.
- **Métricas:**
  - **Engagement** = (likes + comentarios) / visualizaciones.
  - **Comentarios por cada 1.000 visualizaciones.**
  - **Outlier** = visualizaciones del vídeo / media de visualizaciones de su canal. Un 10× significa que rindió 10 veces más de lo normal en ese canal.
- Script: `investigacion/engagement.py` · datos: `investigacion/2026-11-22-engagement.json`.

**Límites:** la búsqueda de YouTube no es una lista completa del nicho, sino una muestra de lo más visto. No hay datos de retención ni de CTR (eso solo lo tiene cada canal). Algunos resultados se salen del nicho (memes, terror) y se han ignorado al sacar las conclusiones.

## Lo más importante en 6 puntos

1. **Los Shorts enganchan el doble que los largos.** Mediana de engagement: 2,1 % en Shorts frente a 0,9 % en largos.
2. **Los Shorts de 1 a 3 minutos enganchan más que los de menos de 1 minuto.** De 61-90 s: 2,9 %; de 91-180 s: 3,3 %; de 30-60 s: 1,4 %; de menos de 30 s: 0,9 %. Los cortísimos consiguen visualizaciones, pero casi nadie da like ni comenta.
3. **El formato estrella en animales es "Los 5 [animal] más [adjetivo] del mundo"** en 60-90 s. El canal Tigrazo lo repite con 1,8-9 M de visualizaciones y un engagement del 5-10 % (5 veces la media). Su truco para los comentarios es este: en la descripción y en el cierre pide **"Comenta 'No puede ser' o 'Ya lo sabía'"**. Consigue entre 4 y 10 comentarios por cada 1.000 visualizaciones, frente a 0,13 de mediana.
4. **"Peligroso, letal o venenoso" en Shorts** sube el engagement a 3,9 % (frente a 2,0 %). En largos no ayuda por sí solo.
5. **En largos, lo que más dispara el outlier es una comparativa local o un mapa**: "Los animales más letales de cada estado de México" (48× la media del canal), "El animal más peligroso de cada…", "1 dato asombroso sobre cada país", "[5 países de América que ya no existen… uno era más grande que México](https://youtu.be/zkt2Z-e82ZQ)" (322.000 visualizaciones en un canal de 751 suscriptores).
6. **Informática tiene poca oferta en español pero el engagement más alto** (3,4 % en largos, 3 veces más que el resto). Los que mejor funcionan explican algo cotidiano de forma sencilla: "Todo sobre direcciones IP" (17×), "Lo que ocurre dentro de una IA cuando le preguntas algo" (23×), "Lo que sucede cuando envías un mensaje".

## Por tema

| Tema | Vídeos | Engagement Shorts | Engagement largos | Coment./1.000 | Outlier mediano |
|---|---|---|---|---|---|
| Animales | 148 | 1,9 % | 0,8 % | 0,12 | 3,3× |
| Geografía | 86 | 2,3 % | 0,6 % | 0,23 | 5,6× |
| Historia | 92 | 2,6 % | 1,1 % | 0,29 | 4,0× |
| Informática | 19 | 3,9 % | 3,4 % | 0,65 | 3,4× |

Cómo leerlo: animales da más visualizaciones (mediana 2,8 M), pero en largos engancha poco. Geografía tiene los outliers más fuertes (vídeos que rinden mucho más que su canal). Informática es el hueco: poca competencia y la audiencia comenta y da like.

## Los mejores ejemplos por tema

**Animales: Shorts**
- [Las Cinco Ranas Más Peligrosas Del Mundo](https://youtu.be/1i4jHpvXIHA) · Tigrazo · 2,8 M · 61 s · 8,9 % · 7,5 coment./1.000
- [Los 5 Tiburones Más Extraños Del Mundo](https://youtu.be/0LpUOytMnSA) · Tigrazo · 4,0 M · 90 s · 6,6 %
- [Los Cinco Animales Que Pueden Desaparecer Ante Tus Ojos](https://youtu.be/bDag-Fe_oZM) · Tigrazo · 3,4 M · 61 s · 7,0 %
- [¿Sabías que la cola de tu gato te está hablando todo el día?](https://youtu.be/9U4jDYQh0H8) · Eros Rosa · 289.000 · 3 min · 7,5 % · 34× su canal
- [Cómo los Pingüinos Emperador Protegen a Sus Crías](https://youtu.be/V6a353U9cMA) · Andrés Andel · 24 M · 5,8 %
- ["Animales con los peores padres"](https://youtu.be/MqwuBn9V2ZI) · Datos Salvajes · 8,4 M · 28× su canal

**Animales: largos**
- [Los animales Más LETALES de cada estado de MÉXICO](https://youtu.be/iM3IiJZU6Qk) · 1,3 M · 18 min · 48×
- [15 gatos increíbles de la mitología que no conocías](https://youtu.be/bxVpPCznN7Q) · 5,3 % · 28× (mezcla animales con historia)
- [ANIMALES VENENOSOS: criaturas más peligrosas sin antídoto](https://youtu.be/NvC6zIPRgcg) · Reino Vida Salvaje · 1,7 M · documental de 60 min

**Informática**
- [Aprende todo sobre direcciones IP](https://youtu.be/QN_hlEUxvHg) · 439.000 · 14 min · 5,8 % · 17×
- [Lo que ocurre dentro de una IA cuando le preguntas algo](https://youtu.be/kQ909EWT_yo) · Cómo Funciona Todo · 1,2 M · 23×
- [Lo que sucede cuando envías un mensaje](https://youtu.be/lb5cTIODdbg) · Cómo Funciona Todo · 181.000 · 3,4 %

**Geografía**
- [25 datos sorprendentes sobre la geografía de Cuba](https://youtu.be/gq0emxOlyw4) · 344.000 · 20 min · 3,6 % · 2,6 coment./1.000
- [Los 5 países con la mejor calidad de vida](https://youtu.be/iF-gzujDLVA) · Short · 813.000 · 28×
- [México vs Europa: el tamaño real te va a sorprender](https://youtu.be/0YoM2c8xqr4) · Short animado con mapas · 998.000
- [Estos 7 países tienen un nombre que les puso España](https://youtu.be/Myg3g6Mi3_M) · Short · 688.000 en un canal de 2.100 suscriptores (ángulo España, encaja con nuestra voz)
- [Los 10 lugares más paranormales del mundo](https://youtu.be/lc8R1H8gkaM) · 957.000 · 9,6×

**Historia**
- [33 inventos que arruinaron el mundo sin querer](https://youtu.be/o0G1U3UpKHU) · 271.000 · 42 min · 11,6×
- [La ciudad subterránea donde vivieron miles de personas](https://youtu.be/Wdjwi4gC1DA) · Short · 1,5 M · 28×
- [7 misterios que fueron resueltos en 2025](https://youtu.be/xza40njmjEw) · MundoCreepy · 1,4 M
- Patrón: los "misterios" atraen visualizaciones en largos (outlier 5,9× frente a 3,5×) pero en Shorts enganchan poco (0,9 %).

**Competencia:** SORPRENDENTE y Andrés Andel tienen muchas visualizaciones, pero sus vídeos rinden por debajo de la media de su propio canal (outlier de 0,2 a 0,9×). Están estancados, así que sirven poco como modelo actual.

## Patrones de títulos

- **Número + superlativo + "del mundo"**: "Los 5 tiburones más extraños del mundo". En Shorts sube el engagement (2,9 % frente a 2,1 %).
- **Sorpresa con un giro al final**: "…uno era más grande que México 😳", "¿Cuba no es una isla?".
- **"De cada…" (cada estado, cada país, cada continente)**: el patrón con el outlier más alto en largos.
- **Explicación sencilla de algo cotidiano** en informática: "Lo que ocurre cuando…", "Todo sobre…", "explicado fácil".
- **1-2 palabras en MAYÚSCULAS** en largos (outlier 6,3× frente a 3,0×). En Shorts no ayudan.
- **Emojis:** en Shorts casi todos los llevan (1 o 2, del animal o del tema + 🌎). En largos no marcan diferencia.
- Lo que no ayuda: "que no conocías/sabías" (está muy gastado: rinde por debajo de la media en Shorts).

## Patrones de miniaturas (vistas 10 de las mejores)

- **Shorts (Tigrazo):** el animal real a pantalla completa y **una sola palabra en blanco, grande y con sombra** en el centro ("RANAS", "TIBURONES"); a veces una flecha roja.
- **Largos con mapa:** mapa del país con los animales encima y el texto en 2-3 colores ("EL ANIMAL MÁS PELIGROSO DE CADA ESTADO DE MÉXICO").
- **Pregunta en franja amarilla** + mapa con flechas y 2 etiquetas cortas ("¿CUBA NO ES UNA ISLA?").
- **Informática:** texto grande de 3 palabras ("TODO SOBRE DIRECCIONES IP") + icono o personaje + objeto reconocible (router).
- **Ilustración o IA** cuando no hay foto real (gatos de la mitología): una palabra grande ("GATOS") sobre arte llamativo. Funciona bien en historia y mitología.
- Documentales largos: escena cinematográfica sin texto (anaconda sobre el agua). Solo funciona en canales grandes.

## Qué aplicamos al canal (propuesta)

1. **Shorts de 60-90 s, no de 30.** Ahora apuntamos a menos de 1 minuto. Propongo subir el objetivo a 60-90 s, con 5 elementos (top 5).
2. **Formato fijo de Shorts de animales:** "Los 5 [animal] más [peligrosos/extraños/raros] del mundo", con el animal completo en pantalla y su nombre rotulado.
3. **Pedir comentarios con dos opciones** al final de cada Short y en la descripción: "Comenta 'No puede ser' o 'Ya lo sabía'". Es lo que más sube los comentarios en toda la muestra.
4. **Largos con estructura "de cada…":** encaja con el largo-23 ya escrito ("el animal más peligroso de cada continente"). En la miniatura, el mapa con los animales encima.
5. **Abrir una línea de informática "explicado fácil"** (1 de cada 4 o 5 piezas): cómo funciona el wifi, qué pasa cuando envías un WhatsApp, qué hay dentro de una IA. Hay poca competencia y mucho engagement.
6. **Geografía con mapa y giro:** "¿Sabías que X no es…?", "países que ya no existen", tamaño real, nombres que puso España.
7. **Miniaturas de Shorts:** una palabra grande en blanco sobre el animal. Para largos: mapa o pregunta en franja amarilla, de 3 a 5 palabras como máximo.
8. **Radar:** añadir estas búsquedas a `radar.py` ("los 5 animales más…", "de cada país", "explicado fácil informática") y medir el engagement y el outlier, no solo las visualizaciones.

## Encaje con el lote que ya está escrito (22-25 nov)

- Largo 23 "animal más peligroso de cada continente": **muy alineado** con el patrón "de cada…". Conviene una miniatura con mapa.
- Largo 25 "inventos por accidente": alineado ("33 inventos que arruinaron el mundo sin querer", 11,6×). Se podría probar un título con número y giro.
- Shorts de casuario e hipopótamo: van bien en tema; habría que alargarlos a 60-90 s y añadir el cierre "No puede ser / Ya lo sabía".
