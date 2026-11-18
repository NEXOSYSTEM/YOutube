"""Continentes reales en proyección ortográfica para la intro de la lupa.

Fuente: NASA Blue Marble «Land ocean ice 2048» (dominio público, ya descargado de Wikimedia Commons).
Se separa tierra/océano por color, se proyecta en ortográfica centrada en lon −20, lat 20 y se exporta
cada continente como PNG negro con transparencia, más un JSON con centroides y la ruta España → México.
No se descarga nada: se usa el ffmpeg de imageio_ffmpeg y numpy del venv de voz.
"""
import json, os, subprocess
import numpy as np
import imageio_ffmpeg

RAIZ = "/Users/luis/Desktop/Youtube/Alucinateconelmundo"
SRC = f"{RAIZ}/material/2026-11-18-semana-01/mapas/01_land_ocean_ice_2048_jpg.jpg"
OUT = f"{RAIZ}/montaje/public/intro"
FF = imageio_ffmpeg.get_ffmpeg_exe()
N = 880  # lado del PNG (se muestra a 440 px = diámetro del planeta, R=220)
LON0, LAT0 = np.radians(-20), np.radians(20)

# 1) Imagen equirectangular → RGB numpy
W, H = 1920, 960
raw = subprocess.run([FF, "-loglevel", "error", "-i", SRC, "-vf", f"scale={W}:{H}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                     capture_output=True, check=True).stdout
img = np.frombuffer(raw, np.uint8).reshape(H, W, 3).astype(np.int16)
r, g, b = img[..., 0], img[..., 1], img[..., 2]
oceano = (b > r + 12) & (b >= g - 5) & (r < 110)
tierra = ~oceano

# 2) Proyección ortográfica inversa: píxel del disco → lon/lat
ys, xs = np.mgrid[0:N, 0:N]
x = (xs + 0.5) / N * 2 - 1
y = 1 - (ys + 0.5) / N * 2
rho = np.sqrt(x ** 2 + y ** 2)
dentro = rho <= 1
c = np.arcsin(np.clip(rho, 0, 1))
with np.errstate(invalid="ignore", divide="ignore"):
    lat = np.arcsin(np.cos(c) * np.sin(LAT0) + np.where(rho > 0, y * np.sin(c) * np.cos(LAT0) / rho, 0))
    lon = LON0 + np.arctan2(x * np.sin(c), rho * np.cos(c) * np.cos(LAT0) - y * np.sin(c) * np.sin(LAT0))
lond, latd = np.degrees(lon), np.degrees(lat)
lond = (lond + 180) % 360 - 180
px = np.clip(((lond + 180) / 360 * W).astype(int), 0, W - 1)
py = np.clip(((90 - latd) / 180 * H).astype(int), 0, H - 1)
land = dentro & tierra[py, px] & (latd > -60)  # sin la Antártida

zonas = {
    "norteamerica": land & (lond < -25) & (latd > 12),
    "sudamerica": land & (lond < -25) & (latd <= 12),
    "europa": land & (lond >= -25) & (latd >= 36),
    "africa": land & (lond >= -25) & (latd < 36),
}

def proyecta(lo, la):
    lo, la = np.radians(lo), np.radians(la)
    X = np.cos(la) * np.sin(lo - LON0)
    Y = np.cos(LAT0) * np.sin(la) - np.sin(LAT0) * np.cos(la) * np.cos(lo - LON0)
    return float(X), float(-Y)  # unidades de radio; y hacia abajo

os.makedirs(OUT, exist_ok=True)
meta = {"lon0": -20, "lat0": 20, "continentes": {}}
for nombre, m in zonas.items():
    rgba = np.zeros((N, N, 4), np.uint8)
    rgba[..., 3] = (m * 255).astype(np.uint8)
    rgba[..., :3] = 5
    subprocess.run([FF, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgba", "-s", f"{N}x{N}", "-i", "-",
                    "-vf", "boxblur=1:1", "-frames:v", "1", f"{OUT}/continente-{nombre}.png"], input=rgba.tobytes(), check=True)
    yy, xx = np.nonzero(m)
    cxu, cyu = (xx.mean() + 0.5) / N * 2 - 1, (yy.mean() + 0.5) / N * 2 - 1
    meta["continentes"][nombre] = {"c": [round(cxu, 4), round(cyu, 4)], "px": int(m.sum())}
    print(nombre, int(m.sum()), "px", meta["continentes"][nombre]["c"])

# 3) Ruta España (Madrid) → México (CDMX) por el círculo máximo
def gc(a, b, n=40):
    (lo1, la1), (lo2, la2) = [np.radians(v) for v in a], [np.radians(v) for v in b]
    p1 = np.array([np.cos(la1) * np.cos(lo1), np.cos(la1) * np.sin(lo1), np.sin(la1)])
    p2 = np.array([np.cos(la2) * np.cos(lo2), np.cos(la2) * np.sin(lo2), np.sin(la2)])
    om = np.arccos(np.clip(p1 @ p2, -1, 1))
    pts = []
    for t in np.linspace(0, 1, n):
        p = (np.sin((1 - t) * om) * p1 + np.sin(t * om) * p2) / np.sin(om)
        pts.append(proyecta(np.degrees(np.arctan2(p[1], p[0])), np.degrees(np.arcsin(p[2]))))
    return pts

meta["ruta"] = [[round(x, 4), round(y, 4)] for x, y in gc((-3.7, 40.4), (-99.1, 19.4))]
meta["espana"] = [round(v, 4) for v in proyecta(-3.7, 40.4)]
meta["mexico"] = [round(v, 4) for v in proyecta(-99.1, 19.4)]
json.dump(meta, open(f"{RAIZ}/montaje/src/data/mapa-intro.json", "w"), indent=1)
print("ruta", meta["espana"], "→", meta["mexico"])
