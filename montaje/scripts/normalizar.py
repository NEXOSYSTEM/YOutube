"""Normalización de audio en dos pasadas (loudnorm medido + lineal) y limitador con margen: −14 LUFS, pico ≤ −1 dBTP tras el AAC.
Copia el vídeo sin recodificar. El limitador va a −2 dBFS porque el AAC sube ~0,5–1 dB los picos reales.
Uso: normalizar.py entrada.mp4 salida.mp4"""
import json, subprocess, sys
import imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
src, dst = sys.argv[1], sys.argv[2]
m = subprocess.run([FF, "-hide_banner", "-i", src, "-vn", "-af", "loudnorm=I=-14:TP=-2:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
j = json.loads(m[m.rindex("{"): m.rindex("}") + 1])
af = (f"loudnorm=I=-14:TP=-2:LRA=11:measured_I={j['input_i']}:measured_TP={j['input_tp']}:measured_LRA={j['input_lra']}"
      f":measured_thresh={j['input_thresh']}:offset={j['target_offset']}:linear=true,aresample=192000,alimiter=limit=0.79:attack=1:release=50:level=false,aresample=48000")
subprocess.run([FF, "-y", "-loglevel", "error", "-i", src, "-c:v", "copy", "-af", af, "-ar", "48000", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", dst], check=True)
