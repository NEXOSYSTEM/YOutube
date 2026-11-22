# Largo · Mié 25-nov 18:00 · Informática · Qué pasa DENTRO de una IA cuando le preguntas algo

*Escrito el 22/11/2026 · 16:9 · Voz ElevenLabs «Thimsen» (Flash v2.5) x1,25. Semana de tecnología. Lo anuncia el Short del mismo día («Por qué la IA se inventa cosas»).*

## Ficha

| Campo | Valor |
|---|---|
| **Título** | Qué pasa DENTRO de una IA cuando le preguntas algo |
| **Títulos alternativos** | «La IA no piensa: esto es lo que hace de verdad» · «Así funciona ChatGPT por dentro (explicado fácil)» |
| **Duración objetivo** | ≈6,5 min (≈1.280 palabras a x1,25 más intro y pausas; norma de largos de 6 a 8 min como máximo) |
| **Estructura** | Gancho → intro lupa → 6 pasos del viaje de la pregunta, con un contador de palabras en pantalla → reenganche («¿por qué se inventa cosas?») → cierre con pregunta |
| **Estilo** | Animación propia como base (la pregunta se rompe en fichas de colores que entran en un «cerebro» de luces) · vídeo real de apoyo: centros de datos, tarjetas gráficas, bibliotecas, personas escribiendo en el móvil · IA de imagen solo para los planos del «cerebro» si la animación propia no queda bien · sin Veo |
| **Miniatura** | Cabeza de robot transparente con fichas de colores dentro. Texto en 2 colores: «¿QUÉ PIENSA?» en amarillo + «LA IA» en blanco |
| **Música** | Electrónica suave y curiosa (biblioteca de YouTube), −22 dB bajo la voz |

---

## BLOQUE 0 · Gancho (0:00–0:25)

> Le escribes a una inteligencia artificial: «¿Por qué el cielo es azul?». En un par de segundos te responde con un texto perfecto. Parece que piensa, que entiende, que sabe. Pero lo que pasa de verdad ahí dentro es mucho más raro. La IA no busca la respuesta en ningún sitio. Hace una sola cosa, millones de veces: adivinar cuál es la siguiente palabra. Hoy te enseño, paso a paso, qué pasa en esos dos segundos.

| # | Qué se ve | Rótulo |
|---|---|---|
| 0.1 | Móvil: alguien escribe «¿Por qué el cielo es azul?» | — |
| 0.2 | La respuesta aparece palabra a palabra | — |
| 0.3 | Zoom dentro del móvil: un remolino de fichas de colores | **¿QUÉ PASA AQUÍ DENTRO?** |

## BLOQUE 1 · Intro lupa (8 s) + la idea clave

> *(Intro lupa con su sonido.)* Antes de empezar, una idea que lo cambia todo. Cuando tu móvil te sugiere la siguiente palabra mientras escribes un mensaje, está haciendo una versión muy pequeña de lo mismo. Si escribes «buenos», te propone «días». Una IA como ChatGPT, Gemini o Claude es ese mismo autocompletado, pero entrenado con muchísimo más texto y muchísimo más grande. Tan grande que, adivinando palabra a palabra, puede escribir una redacción, un poema o un programa.

| # | Qué se ve | Rótulo |
|---|---|---|
| 1.1 | Intro lupa | — |
| 1.2 | Teclado del móvil sugiriendo «días» después de «buenos» | «El autocompletado de tu móvil…» |
| 1.3 | El mismo teclado crece hasta ocupar un edificio | «…pero gigante» |

## BLOQUE 2 · Paso 1: la pregunta se rompe en trocitos

> Lo primero que hace la IA con tu pregunta es romperla en trocitos. Los ordenadores no entienden letras, entienden números, así que el texto se corta en piezas que se llaman tokens. Un token puede ser una palabra entera, como «cielo», o un trozo, como «azul» y una «es» suelta. A cada trozo le da un número. Tu pregunta, que para ti son seis palabras, para la IA es una fila de unos diez números. Por eso, a veces, estas IA se equivocan en cosas tan tontas como contar cuántas letras erre tiene una palabra: no ven las letras, ven trozos.

| # | Qué se ve | Rótulo |
|---|---|---|
| 2.1 | La pregunta se parte en fichas de colores | «Tokens» |
| 2.2 | Cada ficha se convierte en un número | — |
| 2.3 | La palabra «ferrocarril» partida en 3 fichas | «No ve letras, ve trozos» |

## BLOQUE 2b · ¿Dónde se hace todo esto?

> Y una cosa que casi nadie sabe: todo esto no pasa dentro de tu móvil. Cuando pulsas enviar, tu pregunta viaja por internet hasta un centro de datos, un edificio lleno de ordenadores que puede estar en otro país. Allí la esperan unas tarjetas gráficas muy especiales, primas de las que usan los videojuegos, pero mucho más potentes. ¿Por qué tarjetas gráficas? Porque para dibujar un videojuego hay que hacer millones de cuentas sencillas a la vez, y eso es justo lo que necesita una IA. Cada palabra que lee o escribe obliga a hacer miles de millones de multiplicaciones. Una sola tarjeta de estas puede costar lo mismo que un coche, y para que una IA grande conteste rápido a millones de personas hacen falta miles. Por eso, cuando se cae internet, la IA también deja de funcionar: tu móvil solo es la ventana.

| # | Qué se ve | Rótulo |
|---|---|---|
| 2b.1 | La pregunta sale del móvil y viaja por un mapa hasta un edificio | «Viaja a un centro de datos» |
| 2b.2 | Tarjeta gráfica de videojuegos al lado de una de centro de datos | «Millones de cuentas a la vez» |
| 2b.3 | Pasillo de servidores con luces azules | «Tu móvil es la ventana» |

## BLOQUE 3 · Paso 2: cada trozo tiene su sitio en un mapa

> Ahora viene lo más bonito. Cada uno de esos números se convierte en un punto dentro de un mapa enorme, un mapa con miles de direcciones en vez de dos. En ese mapa, las palabras que se parecen están cerca. «Perro» está al lado de «gato». «Rey» está cerca de «reina». «Madrid» cerca de «París». Y lo curioso es que nadie ha dibujado ese mapa a mano. La IA lo ha construido sola, leyendo, al ver qué palabras suelen aparecer juntas. Así es como «sabe» que el cielo tiene algo que ver con el sol, la luz y los colores.

| # | Qué se ve | Rótulo |
|---|---|---|
| 3.1 | Un mapa de estrellas con palabras: perro y gato juntos, rey y reina juntos | «Un mapa de palabras» |
| 3.2 | «Cielo» se enciende y se iluminan «sol», «luz», «azul» | — |

## BLOQUE 4 · Paso 3: las palabras se miran entre ellas

> El tercer paso es el que hizo que estas IA despegaran. Se llama atención, y lo inventaron investigadores de Google en dos mil diecisiete. La idea es sencilla: cada palabra mira a todas las demás de la frase para entender qué significa ahí. Piensa en la palabra «banco». No es lo mismo «me senté en un banco del parque» que «fui al banco a sacar dinero». Gracias a la atención, «banco» mira a «parque» o a «dinero» y cambia de significado. La IA repite esto en decenas de capas, una detrás de otra, y en cada capa entiende un poco más: primero las palabras, luego las frases, luego la intención de lo que preguntas.

| # | Qué se ve | Rótulo |
|---|---|---|
| 4.1 | Frase del parque: líneas de luz de «banco» a «parque» | «Atención» |
| 4.2 | Frase del dinero: líneas de luz de «banco» a «dinero» | «Misma palabra, otro significado» |
| 4.3 | Capas apiladas como pisos de un edificio | «Decenas de capas» |

## BLOQUE 5 · Paso 4: adivinar la siguiente palabra

> Después de todas esas capas, la IA hace su única tarea: calcula qué palabra debería venir después. No elige una sin más. Hace una lista con miles de candidatas y le pone a cada una una probabilidad. Por ejemplo: «El», un treinta por ciento; «La», un veinte; «Porque», un quince… Escoge una, la añade al texto, y vuelve a empezar todo el proceso con la frase un poco más larga. Palabra a palabra. Por eso ves que la respuesta aparece poco a poco en la pantalla: no es un efecto bonito, es que la está escribiendo en ese momento. Y como a veces no escoge la más probable, si le preguntas lo mismo dos veces, te puede responder distinto. Ese toque de azar es a propósito: si siempre escogiera la palabra más probable, sus textos serían aburridos y repetitivos.

| # | Qué se ve | Rótulo |
|---|---|---|
| 5.1 | Barras de probabilidad con «El», «La», «Porque» | «Adivina la siguiente palabra» |
| 5.2 | La palabra elegida vuela a la respuesta; el ciclo se repite | «Palabra a palabra» |
| 5.3 | Dos móviles con la misma pregunta y respuestas distintas | — |

## BLOQUE 6 · Paso 5: de dónde ha aprendido

> ¿Y cómo ha aprendido a adivinar tan bien? Leyendo. Muchísimo. A estas IA se las entrena con una cantidad de texto enorme: páginas web, libros, artículos, código. Durante el entrenamiento, se le tapa una palabra y tiene que adivinarla. Si falla, se corrigen un poquito sus números internos, que se llaman parámetros. Los modelos grandes tienen miles de millones de parámetros, y ese ajuste se repite billones de veces. Después, personas de verdad valoran sus respuestas, para que aprenda a ser útil y a no decir burradas. Y todo eso pasa en centros de datos llenos de tarjetas gráficas, que gastan tanta electricidad como una pequeña ciudad.

| # | Qué se ve | Rótulo |
|---|---|---|
| 6.1 | Biblioteca infinita con páginas volando hacia el cerebro de luces | «Aprende leyendo» |
| 6.2 | Frase con un hueco: «El cielo es ___» | «Adivina la palabra tapada» |
| 6.3 | Pasillos de servidores y tarjetas gráficas | «Miles de tarjetas gráficas» |

## BLOQUE 6b · ¿Y cuando dibuja o habla?

> Hasta ahora hemos hablado de texto, pero muchas IA también entienden fotos, hacen dibujos o hablan con voz. La idea de fondo se parece. Una foto también se puede cortar en trocitos, en pequeños cuadraditos, y cada uno se convierte en números, igual que las palabras. Para dibujar, muchas IA empiezan con una imagen llena de ruido, como la nieve de una tele antigua, y la van limpiando paso a paso, hasta que aparece lo que le has pedido. Y para hablar, convierten el sonido en trocitos y adivinan el siguiente trocito de voz. Siempre el mismo truco: partir las cosas en piezas y adivinar qué pieza viene después.

| # | Qué se ve | Rótulo |
|---|---|---|
| 6b.1 | Una foto de un gato que se parte en cuadraditos con números | «Una foto también son trocitos» |
| 6b.2 | Ruido de tele que se va limpiando hasta mostrar un dibujo | «De ruido a dibujo» |
| 6b.3 | Onda de voz cortada en trocitos | «Siempre el mismo truco» |

## BLOQUE 7 · Reenganche

> Pero si solo adivina palabras… ¿qué pasa cuando no sabe la respuesta? Aquí viene lo más importante del vídeo.

| # | Qué se ve | Rótulo |
|---|---|---|
| 7.1 | Cerebro de luces que parpadea en rojo | **¿Y SI NO LO SABE?** |

## BLOQUE 8 · Paso 6: por qué se inventa cosas

> Cuando la IA no sabe algo, no se calla. Sigue haciendo lo único que sabe hacer: escoger la palabra que mejor suena. Y lo que mejor suena no siempre es verdad. Por eso a veces se inventa un libro que no existe, una fecha o una cita, y te lo dice con total seguridad. A esto se le llama alucinación. No miente a propósito: es que no tiene una forma de comprobar si lo que dice es cierto, solo sabe si suena bien. Las IA de ahora fallan menos, y muchas buscan en internet antes de responder, pero el consejo sigue siendo el mismo: si es algo importante, como salud, dinero o los deberes, compruébalo en una fuente fiable.

| # | Qué se ve | Rótulo |
|---|---|---|
| 8.1 | Respuesta con un título de libro inventado, que se marca en rojo | «Alucinación» |
| 8.2 | Balanza: «suena bien» pesa más que «es verdad» | «Suena bien ≠ es verdad» |
| 8.3 | Lupa sobre una página fiable | «Compruébalo» |

## BLOQUE 8b · Lo que la IA no es

> Y para terminar de entenderla, tres cosas que la IA no es. No es una persona: no tiene sentimientos ni opiniones propias, aunque escriba como si los tuviera, porque ha aprendido de textos escritos por personas. No lo sabe todo al momento: aprendió con textos hasta una fecha, y de lo que pasó después no sabe nada, salvo que busque en internet. Y no se acuerda de ti como un amigo: si no tiene activada una memoria, cada conversación nueva empieza desde cero. Saber esto te ayuda a usarla mejor: es una herramienta muy potente para explicar, resumir o darte ideas, pero la última palabra la tienes tú.

| # | Qué se ve | Rótulo |
|---|---|---|
| 8b.1 | Robot con un corazón tachado | «No siente» |
| 8b.2 | Calendario con una fecha marcada | «Aprendió hasta una fecha» |
| 8b.3 | Chat que se vacía | «Cada chat empieza de cero» |

## BLOQUE 9 · Cierre

> Así que, la próxima vez que una IA te responda, recuerda lo que hay detrás: tu pregunta rota en trocitos, un mapa gigante de palabras, millones de miradas entre ellas y una apuesta, palabra a palabra, sobre qué viene después. Ahora dime en los comentarios: ¿tú usas la IA para estudiar, para trabajar o solo por curiosidad? Y si te ha gustado, suscríbete, que el viernes te cuento cómo sabe tu móvil dónde estás.

| # | Qué se ve | Rótulo |
|---|---|---|
| 9.1 | Resumen rápido de los 6 pasos con iconos | — |
| 9.2 | Pregunta en pantalla | «¿Para qué usas la IA?» |
| 9.3 | Pantalla final con logo y suscripción + Short del mismo día | — |

---

**Fuentes:** Vaswani et al. (2017), *Attention Is All You Need*, Google (mecanismo de atención y arquitectura Transformer); Mikolov et al. (2013), *word2vec* (palabras como puntos en un espacio, «rey/reina»); OpenAI, ayuda «What are tokens?» (tokens y trozos de palabra); Ouyang et al. (2022), *Training language models to follow instructions with human feedback* (valoración humana de las respuestas); OpenAI (2023), *GPT-4 Technical Report*, y Ji et al. (2023), *Survey of Hallucination in Natural Language Generation* (alucinaciones); Agencia Internacional de la Energía (2024), *Electricity 2024* (consumo eléctrico de los centros de datos).

**Nota:** «tanta electricidad como una pequeña ciudad» se comprueba antes del render con la cifra más reciente de la AIE; si no hay fuente clara, se cambia por «muchísima electricidad».
