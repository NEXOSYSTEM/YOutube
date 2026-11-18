# Configuración de voz del canal

Actualizado: 2026-11-18

- Motor: Qwen3-TTS 1.7B CustomVoice 8bit vía mlx-audio (voz/.venv, modelos en voz/modelos con HF_HOME)
- Idioma: --lang_code spanish
- Estilo (--instruct, en inglés): "Speak Spanish with a neutral <ACENTO> accent. Neutral, clear narrator tone, no exaggerated emotion. Fairly fast, fluid pace."
- Velocidad final: x1.25 sobre la salida del modelo -> ffmpeg -filter:a atempo=1.25 (aplicar una sola vez sobre el WAV generado)
- Voz: ryan (hombre)
- Acento: España neutro (castellano estándar) -> <ACENTO> = "accent from Spain (standard Castilian)"
- Norma: el modelo solo se carga al generar; sin servidores en segundo plano.
