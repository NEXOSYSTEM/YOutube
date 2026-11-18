"""Efectos de sonido sintetizados desde cero (obra propia, sin licencias de terceros)."""
import os, wave
import numpy as np

SR = 48000
OUT = "/Users/luis/Desktop/Youtube/Alucinateconelmundo/montaje/public/sfx"
rng = np.random.default_rng(7)


def save(name, x, gain=0.8):
    x = x / (np.abs(x).max() + 1e-9) * gain
    st = np.stack([x, x], 1)
    with wave.open(f"{OUT}/{name}.wav", "w") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((st * 32767).astype(np.int16).tobytes())


def bandsweep(noise, f0, f1, q=2.5):
    # filtro paso banda de 2.º orden con frecuencia variable (barrido)
    n = len(noise); out = np.zeros(n)
    f = np.geomspace(f0, f1, n)
    y1 = y2 = x1 = x2 = 0.0
    for i in range(n):
        w0 = 2 * np.pi * f[i] / SR; al = np.sin(w0) / (2 * q); c = np.cos(w0)
        b0, b2, a0, a1, a2 = al, -al, 1 + al, -2 * c, 1 - al
        y = (b0 * noise[i] + b2 * x2 - a1 * y1 - a2 * y2) / a0
        x2, x1 = x1, noise[i]; y2, y1 = y1, y
        out[i] = y
    return out


def env(n, a, r):
    t = np.linspace(0, 1, n)
    return np.minimum(t / a, 1) * np.clip((1 - t) / r, 0, 1) ** 1.5


def whoosh(d=0.55, f0=300, f1=4500):
    n = int(d * SR); x = bandsweep(rng.standard_normal(n), f0, f1)
    e = np.sin(np.linspace(0, np.pi, n)) ** 2
    return x * e


def impact(d=1.2):
    n = int(d * SR); t = np.arange(n) / SR
    sub = np.sin(2 * np.pi * (55 * t - 20 * t ** 2)) * np.exp(-t * 4)
    click = rng.standard_normal(n) * np.exp(-t * 60) * 0.5
    body = bandsweep(rng.standard_normal(n), 900, 120, q=1.2) * np.exp(-t * 7) * 1.5
    return sub * 1.4 + click + body


def tick():
    n = int(0.05 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * 1800 * t) * np.exp(-t * 120)


def pop():
    n = int(0.12 * SR); t = np.arange(n) / SR
    return np.sin(2 * np.pi * (500 + 900 * t / 0.12) * t) * np.exp(-t * 40)


def riser(d=1.6):
    n = int(d * SR); x = bandsweep(rng.standard_normal(n), 200, 6000, q=4)
    return x * np.linspace(0, 1, n) ** 2


def drone(d=6.0):
    n = int(d * SR); t = np.arange(n) / SR
    x = sum(np.sin(2 * np.pi * f * t + p) for f, p in [(55, 0), (82.4, 1), (110.3, 2)])
    return x * np.minimum(t / 1.5, 1) * np.minimum((d - t) / 1.5, 1)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    save("whoosh", whoosh()); save("whoosh-corto", whoosh(0.3, 600, 6000), 0.6)
    save("impacto", impact(), 0.9); save("tick", tick(), 0.4); save("pop", pop(), 0.5)
    save("riser", riser(), 0.6); save("drone", drone(), 0.5)
    print(sorted(os.listdir(OUT)))
