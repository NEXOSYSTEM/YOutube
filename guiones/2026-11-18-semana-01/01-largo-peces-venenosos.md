# Semana 1 · Vídeo semilargo: Los 10 peces más venenosos del océano

*Escrito el 18/11/2026 · Publicación prevista: martes, 18:00 (hora de España)*

## Ficha

| Campo | Valor |
|---|---|
| **Título** | Los 10 peces más VENENOSOS del océano (el nº 1 está en la orilla) |
| **Títulos alternativos para probar** | «10 peces que NUNCA debes tocar» · «Los peces más venenosos del mundo… y dos viven en España» |
| **Duración objetivo** | ≈7:30–8:30 min (1.330 palabras de narración a x1,25, más las pausas). Los tiempos de las tablas son orientativos y se ajustan a la duración real de cada audio. |
| **Voz** | Qwen3-TTS «ryan», acento de España neutro, x1,25 (ver `voz/config-voz.md`) |
| **Miniatura** | Pez piedra en primer plano, camuflado en la roca, con un círculo rojo alrededor y una flecha. Texto: «NO LO PISES». Fondo oscuro y saturado. |
| **Música** | Fondo documental tenso y suave (biblioteca de audio de YouTube, categoría *Cinematic / Dark*), al −22 dB bajo la voz |
| **Formato** | 16:9, 1080p o 4K |

## Notas para la voz (TTS)

- Cada bloque `NARRACIÓN` se genera como **un audio aparte** (`01-gancho.wav`, `02-n10.wav`…). Así se puede repetir un bloque sin rehacer todo.
- Los números están escritos en letra para que el modelo los lea bien.
- Los `…` y los puntos marcan pausas. No añadir etiquetas SSML.

## Reglas de montaje (para todo el vídeo)

- **Ritmo de imagen:** cambio de plano cada 3–5 s. Nunca más de 6 s con la misma imagen.
- **Rótulo de puesto:** en cada animal aparece «#10», «#9»… en grande, arriba a la izquierda, durante 2 s, con la transición *whoosh* + golpe de zoom.
- **Ficha del animal:** en la esquina inferior derecha, durante 4 s, con el nombre común, el nombre científico en cursiva y una «barra de peligro» de 1 a 5 calaveras.
- **Mapa:** cuando se diga dónde vive, se muestra un mapa mundi (Wikimedia Commons, dominio público) con la zona resaltada en rojo.
- **Texto clave:** las frases marcadas como «RÓTULO» van en pantalla en tipografía gruesa (blanca con borde negro), 2–3 s.
- **Fuentes de imagen, por orden de preferencia:** Pexels, Pixabay, Wikimedia Commons (solo licencias CC0, CC BY o CC BY-SA, apuntando la atribución en `creditos.md`) y, si hace falta, un banco de pago. **Nunca** clips de otros canales de YouTube ni de TikTok.
- **Imágenes generadas con IA:** solo para ilustraciones claramente no realistas (esquemas, comparativas). Si alguna parece real, hay que marcar «contenido alterado o sintético» al subir el vídeo.

---

## BLOQUE 0 · Gancho (0:00–0:30)

**NARRACIÓN (`01-gancho.wav`)**

> En el mar hay animales con dientes enormes, con tentáculos, con mandíbulas que parten huesos… Pero los que deberían darte miedo de verdad son mucho más pequeños. Algunos caben en la palma de tu mano. Uno se esconde en la arena de las playas de España, justo donde pones el pie. Otro se sirve como plato de lujo, aunque un error al cortarlo puede matarte. Y el número uno tiene un veneno tan potente que hay quien ha pedido que le corten la pierna para dejar de sentir el dolor. Estos son los diez peces más venenosos del océano.

| # | Tiempo | Qué se ve | Rótulo / texto | Transición | Buscar (palabras clave) |
|---|---|---|---|---|---|
| 0.1 | 0:00–0:03 | Mandíbula de tiburón abriéndose a cámara lenta | — | Corte seco desde negro | `shark jaws slow motion`, `great white shark` |
| 0.2 | 0:03–0:06 | Tentáculos de pulpo o calamar | — | Corte | `octopus tentacles close up` |
| 0.3 | 0:06–0:09 | Un pez pequeño sobre una mano abierta bajo el agua | «Caben en tu mano» | Zoom lento hacia dentro | `small fish hand underwater` |
| 0.4 | 0:09–0:13 | Pies caminando por la orilla de una playa | «Playas de España» | Corte | `feet walking beach shore` |
| 0.5 | 0:13–0:17 | Plato de sashimi de fugu (pétalos finos) | — | Corte | `fugu sashimi`, `pufferfish dish` |
| 0.6 | 0:17–0:22 | Pez piedra camuflado; un *zoom* revela que es un pez | — | Zoom de revelación | `stonefish camouflage` |
| 0.7 | 0:22–0:30 | Título animado sobre un fondo marino oscuro con partículas | **LOS 10 PECES MÁS VENENOSOS DEL OCÉANO** | Golpe de sonido + desenfoque | `deep ocean dark particles` |

---

## BLOQUE 1 · Aclaración «venenoso frente a tóxico» (0:30–0:50)

**NARRACIÓN (`02-intro.wav`)**

> Antes de empezar, un detalle que casi nadie sabe. Un animal venenoso te inyecta su veneno, con una espina o un aguijón. Un animal tóxico, en cambio, te hace daño si te lo comes. En esta lista hay de los dos tipos… y algunos son las dos cosas a la vez. Empezamos.

| # | Tiempo | Qué se ve | Rótulo / texto | Transición | Buscar |
|---|---|---|---|---|---|
| 1.1 | 0:30–0:38 | Pantalla dividida: a la izquierda, una espina de pez (plano detalle); a la derecha, un pez en un plato | IZQ.: «VENENOSO = te lo inyecta» · DCHA.: «TÓXICO = te lo comes» | Barrido horizontal | `fish spines close up`, `fish on plate` |
| 1.2 | 0:38–0:46 | Las dos mitades se juntan sobre un pez globo | «…o las dos cosas» | Fusión | `pufferfish swimming` |
| 1.3 | 0:46–0:50 | Contador «10» que gira | **#10** | *Whoosh* | — (gráfico) |

---

## BLOQUE 2 · #10 Pez conejo (0:50–1:45)

**NARRACIÓN (`03-n10-pez-conejo.wav`)**

> Número diez: el pez conejo. Su nombre suena adorable, y su cara también. Tiene boquita de roedor y se pasa el día mordisqueando algas en los arrecifes del Índico y del Pacífico. Es vegetariano… y aun así es uno de los peces que más picaduras provoca entre los pescadores. El truco está en sus aletas. Esconden espinas cargadas de veneno que se clavan cuando lo agarras para quitarle el anzuelo. La picadura no suele ser mortal, pero el dolor dura horas. Moraleja: que algo tenga cara de conejo no significa que sea inofensivo.

| # | Tiempo | Qué se ve | Rótulo / texto | Transición | Buscar |
|---|---|---|---|---|---|
| 2.1 | 0:50–0:56 | Pez conejo nadando en el arrecife, de frente | **#10 PEZ CONEJO** · ficha: *Siganus* spp., ☠☠ | *Whoosh* + zoom | `rabbitfish`, `siganus` |
| 2.2 | 0:56–1:03 | Primer plano de la boca del pez comiendo algas | «Vegetariano» | Corte | `rabbitfish eating algae` |
| 2.3 | 1:03–1:10 | Mapa: Índico y Pacífico occidental resaltados | — | Zoom al mapa | (mapa de Wikimedia) |
| 2.4 | 1:10–1:20 | Pescador sacando un pez del anzuelo | — | Corte | `fisherman removing hook fish` |
| 2.5 | 1:20–1:32 | Aletas desplegadas a cámara lenta; un círculo rojo marca las espinas | «Espinas con veneno» | Congelado + círculo | `rabbitfish fins`, `siganus spines` |
| 2.6 | 1:32–1:45 | Pez conejo alejándose | «Cara de conejo ≠ inofensivo» | Fundido a negro corto | `rabbitfish reef` |

---

## BLOQUE 3 · #9 Blenio colmillo (1:45–2:40)

**NARRACIÓN (`04-n9-blenio.wav`)**

> Número nueve: el blenio colmillo. Mide menos que tu dedo, pero tiene dos colmillos enormes en la mandíbula inferior… y no los usa para cazar. Los usa para defenderse. Cuando un pez más grande se lo traga, el blenio le muerde por dentro, y su veneno tiene algo muy raro: contiene sustancias parecidas a los opioides, que le bajan la tensión de golpe al depredador. Este, mareado, abre la boca y lo escupe. El blenio sale nadando como si nada. Es tan eficaz que otros peces, sin veneno, han evolucionado para imitar su aspecto… y que nadie se atreva a comérselos.

| # | Tiempo | Qué se ve | Rótulo / texto | Transición | Buscar |
|---|---|---|---|---|---|
| 3.1 | 1:45–1:52 | Blenio pequeño asomado a un agujero del coral | **#9 BLENIO COLMILLO** · ficha: *Meiacanthus* spp., ☠☠ | *Whoosh* + zoom | `fang blenny`, `meiacanthus` |
| 3.2 | 1:52–2:00 | Comparativa de tamaño: silueta del blenio junto a un dedo | «Menos que tu dedo» | Gráfico | (gráfico propio) |
| 3.3 | 2:00–2:10 | Ilustración de la mandíbula con los dos colmillos señalados | «Colmillos defensivos» | Zoom | (ilustración propia o IA esquemática) |
| 3.4 | 2:10–2:22 | Animación sencilla: un pez grande se traga al blenio, se marea (líneas en espiral) y lo escupe | «Veneno tipo opioide» | Animación | (gráfico propio) |
| 3.5 | 2:22–2:40 | Dos peces parecidos lado a lado | «Los imitadores» | Pantalla dividida | `blenny mimic`, `fang blenny reef` |

---

## BLOQUE 4 · #8 Tiburón de Groenlandia (2:40–3:40)

**NARRACIÓN (`05-n8-groenlandia.wav`)**

> Número ocho, y aquí hacemos trampa, porque no pica ni muerde a nadie. El tiburón de Groenlandia vive en aguas heladas y es, según los científicos, el vertebrado que más años vive: se calcula que algunos superan los cuatrocientos. Pero su carne fresca es tóxica. Contiene una sustancia que el cuerpo transforma en algo que produce efectos parecidos a una borrachera muy fuerte: mareos, vómitos y dificultad para andar. En Islandia encontraron la solución hace siglos: fermentar la carne durante semanas y dejarla secar al aire durante meses. El resultado es el hákarl, un plato tradicional… con un olor que muchos comparan con el amoníaco.

| # | Tiempo | Qué se ve | Rótulo / texto | Transición | Buscar |
|---|---|---|---|---|---|
| 4.1 | 2:40–2:48 | Tiburón de Groenlandia nadando lento en aguas oscuras | **#8 TIBURÓN DE GROENLANDIA** · ficha: *Somniosus microcephalus*, ☠ (tóxico) | *Whoosh* | `greenland shark` |
| 4.2 | 2:48–2:58 | Hielo flotando en el Ártico | «Aguas heladas» | Corte | `arctic sea ice underwater` |
| 4.3 | 2:58–3:08 | Contador de años que sube rápido hasta «+400» | «+400 AÑOS» | Animación de número | (gráfico propio) |
| 4.4 | 3:08–3:20 | Persona mareada (desenfocada, tambaleándose) | «Carne fresca = tóxica» | Efecto de desenfoque | `dizzy man blurry` |
| 4.5 | 3:20–3:32 | Carne colgada secándose en una caseta de madera | «Hákarl (Islandia)» | Corte | `hakarl drying shed iceland` |
| 4.6 | 3:32–3:40 | Taco de hákarl en un plato; alguien pone cara de asco | — | Corte | `hakarl`, `fermented shark` |

---

## BLOQUE 5 · #7 Pez gato estriado (3:40–4:35)

**NARRACIÓN (`06-n7-pez-gato.wav`)**

> Número siete: el pez gato estriado. Cuando son jóvenes, cientos de ellos nadan pegados formando una bola que se mueve como un solo animal gigante. Precioso… hasta que lo tocas. Tiene espinas venenosas en la aleta dorsal y en las pectorales, y su picadura es de las más dolorosas entre los peces gato. Se han documentado casos graves. Y lo peor: incluso muerto, tirado en la playa, sus espinas pueden seguir picando. Por eso es uno de los peces que se recomienda no tocar ni con guantes finos.

| # | Tiempo | Qué se ve | Rótulo / texto | Transición | Buscar |
|---|---|---|---|---|---|
| 5.1 | 3:40–3:50 | Bola de peces gato jóvenes moviéndose en bloque | **#7 PEZ GATO ESTRIADO** · ficha: *Plotosus lineatus*, ☠☠☠ | *Whoosh* | `striped eel catfish ball`, `plotosus lineatus` |
| 5.2 | 3:50–4:02 | Plano cenital de la bola girando | «Se mueven como un solo animal» | Corte | `catfish school` |
| 5.3 | 4:02–4:15 | Un ejemplar suelto; un círculo rojo marca las espinas dorsales y pectorales | «Espinas venenosas» | Congelado + círculos | `plotosus lineatus close up` |
| 5.4 | 4:15–4:27 | Pez muerto en la arena de una playa | «Muerto… sigue picando» | Corte | `dead fish on beach` |
| 5.5 | 4:27–4:35 | Mano con guante apartándose | — | Corte | `glove hand beach` |

---

## BLOQUE 6 · #6 Cabracho (4:35–5:30)

**NARRACIÓN (`07-n6-cabracho.wav`)**

> Número seis… y este seguramente lo has comido. El cabracho, el rey del pastel de cabracho, vive en el Mediterráneo y en el Atlántico, muy cerca de nosotros. Es un pez escorpión: tiene la cabeza llena de crestas y espinas, y varias de sus aletas llevan veneno. Los pescadores lo saben bien y lo manipulan con mucho cuidado. Su picadura produce un dolor intenso e hinchazón, aunque no suele ser peligrosa para una persona sana. Cocinado, en cambio, es delicioso: el calor destruye el veneno de las espinas. Así que la próxima vez que pidas pastel de cabracho, recuerda que te estás comiendo a un pez venenoso.

| # | Tiempo | Qué se ve | Rótulo / texto | Transición | Buscar |
|---|---|---|---|---|---|
| 6.1 | 4:35–4:42 | Cabracho rojo inmóvil sobre una roca | **#6 CABRACHO** · ficha: *Scorpaena scrofa*, ☠☠ | *Whoosh* | `red scorpionfish`, `scorpaena scrofa` |
| 6.2 | 4:42–4:52 | Pastel de cabracho en una tapa o un plato | «¿Te suena?» | Corte | `fish pate spanish tapa` |
| 6.3 | 4:52–5:02 | Mapa con el Mediterráneo y la costa atlántica resaltados | — | Zoom al mapa | (mapa) |
| 6.4 | 5:02–5:14 | Detalle de la cabeza: crestas y espinas, con círculos rojos | «Pez escorpión» | Zoom + círculos | `scorpionfish head close up` |
| 6.5 | 5:14–5:22 | Pescadero manipulando pescado con guantes | — | Corte | `fishmonger gloves fish market` |
| 6.6 | 5:22–5:30 | Pescado cocinándose en una sartén | «El calor destruye el veneno» | Corte | `fish cooking pan` |

---

## BLOQUE 7 · Re-gancho (5:30–5:40)

**NARRACIÓN (`08-regancho.wav`)**

> Hasta aquí, dolorosos pero casi nunca mortales. A partir de ahora, la cosa cambia. Y el siguiente puede estar ahora mismo enterrado en tu playa favorita.

| # | Tiempo | Qué se ve | Rótulo / texto | Transición | Buscar |
|---|---|---|---|---|---|
| 7.1 | 5:30–5:40 | La pantalla se oscurece; arena de playa vista muy de cerca, con un ojo que se abre en la arena | «A partir de aquí… cuidado» | Viñeta oscura + golpe de sonido | `fish buried in sand eyes`, `weever fish sand` |

---

## BLOQUE 8 · #5 Pez araña (5:40–6:40)

**NARRACIÓN (`09-n5-pez-arana.wav`)**

> Número cinco: el pez araña. Es pequeño, de color arena, y se pasa el día enterrado en el fondo, en aguas poco profundas, con solo los ojos y la aleta dorsal fuera. Vive en las costas de España, y cada verano es responsable de muchísimas picaduras a bañistas que lo pisan sin verlo. Las espinas de su aleta dorsal y de las agallas inyectan un veneno que provoca un dolor intensísimo, de los que te sacan del agua cojeando. ¿Qué hacer si te pica? Sal del agua, avisa al socorrista y mete la zona en agua lo más caliente que aguantes sin quemarte, porque el calor ayuda a desactivar el veneno. Y si te mareas o te cuesta respirar, a urgencias.

| # | Tiempo | Qué se ve | Rótulo / texto | Transición | Buscar |
|---|---|---|---|---|---|
| 8.1 | 5:40–5:48 | Pez araña medio enterrado en la arena | **#5 PEZ ARAÑA** · ficha: *Trachinus draco*, ☠☠☠ | *Whoosh* | `weever fish`, `trachinus draco` |
| 8.2 | 5:48–5:58 | Detalle de la aleta dorsal negra levantada | «Aleta dorsal = espinas» | Zoom + círculo | `weever fish dorsal fin` |
| 8.3 | 5:58–6:08 | Bañistas en la orilla de una playa española en verano | «Costas de España» | Corte | `spain beach summer people water` |
| 8.4 | 6:08–6:18 | Pie entrando en el agua a cámara lenta | — | Cámara lenta | `foot stepping water slow motion` |
| 8.5 | 6:18–6:32 | Gráfico de 3 pasos: 1) salir del agua y avisar al socorrista · 2) agua caliente (sin quemarse) · 3) urgencias si hay mareo | Los 3 pasos | Aparecen uno a uno | (gráfico propio) |
| 8.6 | 6:32–6:40 | Bandera de socorrista o torre de vigilancia | — | Corte | `lifeguard tower spain beach` |

> ⚠️ Consejo de primeros auxilios genérico. En la descripción, añadir: «Ante cualquier picadura, consulta a un profesional sanitario».

---

## BLOQUE 9 · #4 Pastinaca (6:40–7:35)

**NARRACIÓN (`10-n4-pastinaca.wav`)**

> Número cuatro: la pastinaca, una raya que también vive en nuestras costas. Se mueve con elegancia, como si volara bajo el agua, y suele huir antes que atacar. El peligro está en su cola: lleva un aguijón aserrado, como un cuchillo de sierra, con glándulas de veneno. Solo lo usa cuando se siente atrapada o alguien la pisa. Pero cuando lo usa, puede ser muy grave. En dos mil seis, el famoso divulgador australiano Steve Irwin murió mientras grababa un documental, por el aguijón de una raya de otra especie que le alcanzó en el pecho. Fue un caso rarísimo… pero demuestra que con estos animales no se juega.

| # | Tiempo | Qué se ve | Rótulo / texto | Transición | Buscar |
|---|---|---|---|---|---|
| 9.1 | 6:40–6:48 | Raya deslizándose sobre la arena | **#4 PASTINACA** · ficha: *Dasyatis pastinaca*, ☠☠☠ | *Whoosh* | `common stingray`, `dasyatis pastinaca` |
| 9.2 | 6:48–6:58 | Raya «volando» vista desde abajo | «Huye antes que atacar» | Corte | `stingray swimming from below` |
| 9.3 | 6:58–7:10 | Detalle de la cola y el aguijón aserrado | «Aguijón aserrado + veneno» | Zoom + círculo | `stingray tail barb close up` |
| 9.4 | 7:10–7:25 | Foto de archivo de Steve Irwin (Wikimedia, con licencia) o, si no hay, un rótulo sobre una imagen de la costa australiana | «Steve Irwin · 2006» | Fundido suave | `Steve Irwin` en Wikimedia Commons · `australia reef coast` |
| 9.5 | 7:25–7:35 | Raya alejándose en el azul | «Caso rarísimo» | Fundido | `stingray blue water` |

> Nota de tono: tratar la muerte de Steve Irwin con respeto, sin efectos de sonido ni humor.

---

## BLOQUE 10 · #3 Pez león (7:35–8:30)

**NARRACIÓN (`11-n3-pez-leon.wav`)**

> Número tres: el pez león. Probablemente el pez venenoso más bonito del mundo, con aletas como plumas rayadas. Tiene dieciocho espinas con veneno, y su picadura es de las más dolorosas del mar, aunque rara vez mortal. Pero su verdadero peligro es otro. Es originario del Índico y del Pacífico… y desde los años ochenta ha invadido el Atlántico y el Caribe. Allí no tiene depredadores, se reproduce sin parar y devora a los peces de los arrecifes. Tanto, que en algunos países se organizan concursos para pescarlo, y hay restaurantes que lo sirven para frenar la plaga. Porque, una vez sin espinas, se come sin problema.

| # | Tiempo | Qué se ve | Rótulo / texto | Transición | Buscar |
|---|---|---|---|---|---|
| 10.1 | 7:35–7:45 | Pez león con las aletas desplegadas | **#3 PEZ LEÓN** · ficha: *Pterois* spp., ☠☠☠☠ | *Whoosh* | `lionfish`, `pterois volitans` |
| 10.2 | 7:45–7:55 | Plano detalle de las espinas | «18 espinas venenosas» | Zoom | `lionfish spines close up` |
| 10.3 | 7:55–8:08 | Mapa animado: zona de origen (Índico-Pacífico) → flecha hacia el Atlántico y el Caribe | «Invasión desde los años 80» | Animación | (mapa) |
| 10.4 | 8:08–8:18 | Pez león cazando peces pequeños en un arrecife | «Sin depredadores» | Corte | `lionfish hunting` |
| 10.5 | 8:18–8:30 | Buceador con arpón o filete de pez león cocinado | «Se lo comen para frenar la plaga» | Corte | `lionfish spearfishing`, `lionfish fillet` |

---

## BLOQUE 11 · Re-gancho (8:30–8:38)

**NARRACIÓN (`12-regancho2.wav`)**

> Quedan dos. Uno te mata si te lo comes mal preparado. El otro… si lo pisas.

| # | Tiempo | Qué se ve | Rótulo / texto | Transición | Buscar |
|---|---|---|---|---|---|
| 11.1 | 8:38–8:38 | Pantalla partida: pez globo / roca que se mueve | «2 · 1» | Corte rítmico al compás de la voz | `pufferfish`, `stonefish` |

---

## BLOQUE 12 · #2 Pez globo (8:38–9:35)

**NARRACIÓN (`13-n2-pez-globo.wav`)**

> Número dos: el pez globo. No pica. Pero muchas especies llevan en el hígado, en los ovarios y en la piel una de las toxinas más potentes que se conocen: la tetrodotoxina. Paraliza los nervios y puede parar la respiración, y no existe ningún antídoto. Aun así, en Japón es un manjar llamado fugu. Solo pueden prepararlo cocineros con una licencia especial, que se forman durante años para retirar las partes tóxicas sin contaminar la carne. Un error con el cuchillo, y el plato más caro de la carta se convierte en el último. Y por si fuera poco, cuando se siente amenazado se hincha como un balón de pinchos.

| # | Tiempo | Qué se ve | Rótulo / texto | Transición | Buscar |
|---|---|---|---|---|---|
| 12.1 | 8:38–8:46 | Pez globo nadando con normalidad | **#2 PEZ GLOBO** · ficha: *Takifugu* spp., ☠☠☠☠ (tóxico) | *Whoosh* | `pufferfish swimming`, `takifugu` |
| 12.2 | 8:46–8:58 | Esquema del pez con el hígado, los ovarios y la piel resaltados en rojo | «Tetrodotoxina» | Gráfico | (gráfico propio) |
| 12.3 | 8:58–9:08 | Pantalla negra con el texto grande | «NO HAY ANTÍDOTO» | Golpe de sonido | — |
| 12.4 | 9:08–9:22 | Cocinero cortando pescado con precisión; plato de fugu en pétalos | «Cocineros con licencia» | Corte | `japanese chef cutting fish`, `fugu sashimi` |
| 12.5 | 9:22–9:35 | Pez globo hinchándose | — | Cámara lenta | `pufferfish inflating` |

---

## BLOQUE 13 · #1 Pez piedra (9:35–10:25)

**NARRACIÓN (`14-n1-pez-piedra.wav`)**

> Y el número uno: el pez piedra, el pez más venenoso que se conoce. Mira esta imagen… ¿Lo ves? Exacto: casi nadie lo ve. Parece una roca cubierta de algas y se queda inmóvil en el fondo, en aguas poco profundas del Índico y del Pacífico. Tiene trece espinas en el lomo, y cuando alguien lo pisa, el propio peso de la persona hace que se claven y descarguen el veneno. El dolor se describe como el peor que se puede sentir. Llega a ser tan insoportable que hay quien ha pedido que le amputen la pierna. Puede causar parálisis y problemas en el corazón, y por eso es uno de los pocos peces que tienen un antídoto propio. Hoy las muertes son muy raras… siempre que llegues a tiempo al hospital.

| # | Tiempo | Qué se ve | Rótulo / texto | Transición | Buscar |
|---|---|---|---|---|---|
| 13.1 | 9:35–9:42 | Fondo rocoso con algas, sin moverse | **#1 PEZ PIEDRA** | *Whoosh* + silencio musical de 1 s | `stonefish camouflage`, `rocky reef bottom` |
| 13.2 | 9:42–9:50 | Mismo plano: ¿lo ves? → zoom y un contorno rojo revela al pez | «¿Lo ves?» | Zoom de revelación | `stonefish` |
| 13.3 | 9:50–9:58 | Ficha | ficha: *Synanceia verrucosa*, ☠☠☠☠☠ | — | — |
| 13.4 | 9:58–10:08 | Esquema del lomo con 13 espinas en rojo; un pie bajando | «13 espinas» | Gráfico | (gráfico propio) |
| 13.5 | 10:08–10:18 | Pez piedra de frente, abriendo la boca | «El peor dolor» | Zoom lento | `stonefish close up mouth` |
| 13.6 | 10:18–10:25 | Ambulancia o ampolla de antídoto | «Tiene antídoto propio» | Corte | `ambulance`, `antivenom vial` |

---

## BLOQUE 14 · Cierre (10:25–10:50)

**NARRACIÓN (`15-cierre.wav`)**

> Así que ya lo sabes: en el mar, lo más peligroso no siempre es lo más grande. A veces es una roca que no es una roca. Ahora dime en los comentarios: ¿cuál de estos diez te daría más miedo encontrarte? Y si te ha gustado, en el siguiente vídeo te enseño los animales a los que la evolución diseñó fatal. Te espera aquí.

| # | Tiempo | Qué se ve | Rótulo / texto | Transición | Buscar |
|---|---|---|---|---|---|
| 14.1 | 10:25–10:35 | Montaje rápido de los 10 peces (1 s cada uno) | — | Cortes al ritmo | (planos ya usados) |
| 14.2 | 10:35–10:42 | Pez piedra camuflado | «¿Cuál te da más miedo? 👇» | Corte | — |
| 14.3 | 10:42–10:50 | **Pantalla final** de YouTube: vídeo recomendado + botón de suscripción | — | Fundido | — |

---

## Descripción para YouTube

```
Los 10 peces más venenosos (y tóxicos) del océano: desde el pez conejo hasta el pez piedra, el pez más venenoso que se conoce. Dos de ellos viven en las costas de España.

⏱️ Capítulos
0:00 Intro
0:30 Venenoso vs. tóxico
0:50 #10 Pez conejo
1:45 #9 Blenio colmillo
2:40 #8 Tiburón de Groenlandia
3:40 #7 Pez gato estriado
4:35 #6 Cabracho
5:40 #5 Pez araña
6:40 #4 Pastinaca
7:35 #3 Pez león
8:38 #2 Pez globo
9:35 #1 Pez piedra

⚠️ La información de primeros auxilios es general. Ante cualquier picadura, consulta a un profesional sanitario.

📚 Fuentes
- (añadir aquí las fichas consultadas: FishBase, Wikipedia, artículos científicos, etc.)

🎞️ Créditos de imágenes: (copiar de creditos.md)

#animales #peces #datoscuriosos #océano #sabíasque
```

> Ajustar los minutos de los capítulos al tiempo real del montaje.

**Etiquetas:** peces venenosos, peces más venenosos del mundo, pez piedra, pez globo, fugu, pez araña, pez león, cabracho, pastinaca, animales venenosos, curiosidades del mar

## Datos que conviene comprobar antes de grabar

El guion evita cifras dudosas, pero conviene confirmar estos puntos con una fuente fiable (por ejemplo FishBase o artículos revisados) y apuntarla en la descripción:

1. **Tiburón de Groenlandia, «más de 400 años»:** la estimación publicada en *Science* en 2016 fue de unos 392 ± 120 años. «Algunos superan los cuatrocientos» entra en ese margen.
2. **Pez león, «18 espinas» e invasión «desde los años 80»:** la cifra de espinas es la habitual (13 dorsales, 3 anales y 2 pélvicas). La primera observación en Florida suele situarse en 1985.
3. **Blenio colmillo, veneno con «sustancias parecidas a los opioides»:** estudio de Casewell y otros en *Current Biology* (2017).
4. **Pez piedra, «hay quien ha pedido que le amputen la pierna»:** es una anécdota muy citada sobre la intensidad del dolor. Se puede suavizar a «el dolor es tan fuerte que se describe como insoportable» si no se encuentra una fuente.
