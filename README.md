# Alucínate con el mundo — sistema de producción del canal

Canal: https://www.youtube.com/@AlucinateconelMundo1 · Nicho: curiosidades del mundo (listas de 8–12 min + Shorts). Idioma: español de España.

Este repositorio guarda **el código, los guiones, las reglas y los informes** del canal. El material pesado (clips, audio, vídeos, modelos de voz, Node y Python portátiles) y las credenciales **no** están aquí: viven solo en el Mac de Luis en `/Users/luis/Desktop/Youtube/Alucinateconelmundo`.

Antes de tocar nada, lee [`REGLAS-DEL-CANAL.md`](REGLAS-DEL-CANAL.md) y [`AGENTS.md`](AGENTS.md).

## Qué hay en cada carpeta

| Carpeta | Contenido |
|---|---|
| `guiones/<fecha>-semana-NN/` | Guion del largo y de los Shorts, con desglose de escenas, y `textos-voz/` (un .txt por bloque de narración) |
| `voz/` | Narración: `narrar.py`, `narrar_frases.py` (frase a frase + control con Whisper), `acortar_pausas.py`, `config-voz.md` |
| `montaje/` | Proyecto Remotion (`src/*.jsx`, `src/data/*.json`) y scripts Python de plan, subtítulos, sonido, comprobación y revisión |
| `subida/` | Subida a YouTube con la Data API (`autorizar.py`, `subir.py`) |
| `informes/`, `investigacion/` | Competencia, monetización y nichos |
| `producir.sh` / `producir.nuevo.sh` | Producción completa de una semana con un comando |
| `ESTADO.md` | Estado en vivo del último trabajo |

## Flujo de un vídeo

1. **Guion** en `guiones/` → Luis lo aprueba (regla 1).
2. **Voz**: `voz/narrar_frases.py` (Qwen3-TTS «ryan», España, x1,25 real, revisada con Whisper).
3. **Material**: `montaje/scripts/buscar_material.py`, `buscar_stock.py`, `buscar_videos.py` (Wikimedia, Openverse, Pixabay, NOAA…). Planos que no existen libres → **Veo** (ver `docs/veo.md`).
4. **Plan y subtítulos**: `tiempos_subtitulos.py` + `plan.py` → `montaje/src/data/`.
5. **Render**: `producir.sh semana-NN` (Remotion + FFmpeg, −14 LUFS) → `videos/<fecha>-<pieza>/`.
6. **Revisión**: `montaje/scripts/revisar.py`.
7. **Subida**: `subida/subir.py`, **solo cuando Luis lo diga**.

## Instalar en otro equipo o en Antigravity

```bash
git clone https://github.com/NEXOSYSTEM/YOutube.git Alucinateconelmundo
cd Alucinateconelmundo
```

Abre la carpeta en Antigravity (File → Open Folder). El agente lee `AGENTS.md` con las reglas.

Para poder renderizar en un equipo nuevo hace falta además (no va en el repo):

- **Node 20+** y `cd montaje && npm ci` (Remotion 4.0.539).
- **Python 3.12** con `mlx-audio` (voz, solo Apple Silicon), `mlx-whisper`, `imageio-ffmpeg`; y `pip install -r subida/requirements.txt` para la subida.
- Modelo Qwen3-TTS 1.7B CustomVoice 8bit (se descarga solo la primera vez).
- `herramientas/claves-stock.txt` (clave de Pixabay) y `credenciales/` (OAuth de YouTube): pídeselas a Luis, nunca al repo.
- Las rutas de los scripts apuntan a `/Users/luis/Desktop/Youtube/Alucinateconelmundo`; en otro equipo cambia la variable `R` de `producir.sh` y `montaje/render.sh`.
