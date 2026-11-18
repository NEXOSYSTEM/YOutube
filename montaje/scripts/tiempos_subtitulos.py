"""Tiempos de frases y palabras para los subtítulos (sin STT).

Reparte el texto en frases cortas (1–2 líneas) y las encaja en el audio:
1) tiempo proporcional al número de caracteres dentro de la zona con voz;
2) cada corte de frase se ajusta a la pausa real más cercana del audio (±0,9 s).
Las palabras se reparten de forma proporcional dentro de su frase.
Salida: montaje/src/data/tiempos.json y los .srt en videos/2026-11-18-semana-01/
"""
import json, os, re, wave
import numpy as np

RAIZ = os.environ.get("ALUCINATE_RAIZ") or os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import semana as S  # rutas de la semana
TXT = S.TXT
AUD = S.AUD
OUTV = f"{RAIZ}/videos/2026-11-18-pruebas"  # los .srt definitivos los escribe plan.py en la carpeta de cada vídeo
GAP = 0.3  # silencio entre bloques del vídeo largo
MAXC = 44  # caracteres por frase (≈ 2 líneas cortas en vertical, 1 línea en horizontal)


def lee_wav(p):
    with wave.open(p) as w:
        sr = w.getframerate()
        a = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
    return a, sr


def pausas(a, sr):
    fr = int(0.02 * sr)
    n = len(a) // fr
    rms = np.sqrt((a[: n * fr].reshape(n, fr) ** 2).mean(1))
    thr = max(0.008, np.percentile(rms, 20) * 1.5)
    sil = rms < thr
    voz = np.where(~sil)[0]
    ini, fin = (voz[0] * 0.02, (voz[-1] + 1) * 0.02) if len(voz) else (0, len(a) / sr)
    gaps, s = [], None
    for i, v in enumerate(sil):
        if v and s is None:
            s = i
        elif not v and s is not None:
            if (i - s) * 0.02 >= 0.12 and s * 0.02 > ini and i * 0.02 < fin:
                gaps.append(((s + i) / 2 * 0.02, (i - s) * 0.02))
            s = None
    return ini, fin, gaps


def frases(texto):
    texto = re.sub(r"\s+", " ", texto.strip())
    partes = re.findall(r"[^.!?…]+(?:[.!?…]+|$)", texto)
    out = []
    for p in partes:
        p = p.strip()
        if not p:
            continue
        while len(p) > MAXC:
            # cortar en coma / punto y coma / dos puntos, si no en el espacio más cercano a la mitad
            cands = [m.end() for m in re.finditer(r"[,;:]\s", p) if 12 <= m.end() <= MAXC + 6]
            if not cands:
                cands = [m.start() for m in re.finditer(r"\s(?:y|que|pero|porque|aunque|con|en|de|para|sin)\s", p) if 14 <= m.start() <= MAXC]
            if not cands:
                STOP = {"el", "la", "los", "las", "un", "una", "de", "del", "y", "en", "a", "al", "que", "se", "su", "sus", "lo", "le", "con", "por", "es", "tan", "muy", "más"}
                cands = [m.start() for m in re.finditer(r"\s", p) if m.start() <= MAXC and p[:m.start()].split()[-1].lower() not in STOP]
                if cands and len(p) <= 2 * MAXC:
                    cands = [min(cands, key=lambda x: abs(x - len(p) / 2))]
                cands = cands[-1:] if cands else [len(p) // 2]
            c = max(cands)
            out.append(p[:c].strip())
            p = p[c:].strip()
        if p:
            if out and len(p) < 10 and len(out[-1]) + len(p) < MAXC + 10:
                out[-1] += " " + p
            else:
                out.append(p)
    return out


def peso(s):
    return len(re.sub(r"[^\wáéíóúüñÁÉÍÓÚÜÑ]", "", s)) + 6 * len(re.findall(r"[,;:.!?…]", s)) + 2


def alinea(nombre):
    texto = open(f"{TXT}/{nombre}.txt", encoding="utf-8").read()
    a, sr = lee_wav(f"{AUD}/{nombre}.wav")
    dur = len(a) / sr
    ini, fin, gaps = pausas(a, sr)
    fs = frases(texto)
    pesos = [peso(f) for f in fs]
    tot = sum(pesos)
    bounds, acc = [], 0
    for pw in pesos[:-1]:
        acc += pw
        bounds.append(ini + (fin - ini) * acc / tot)
    usados, ajust = set(), []
    prev = ini
    for b in bounds:
        best = None
        for gi, (g, gl) in enumerate(gaps):
            if gi in usados or g <= prev + 0.4:
                continue
            d = abs(g - b)
            if d <= 0.9 and (best is None or d - 0.3 * gl < best[0]):
                best = (d - 0.3 * gl, gi, g)
        if best:
            usados.add(best[1]); b = best[2]
        b = max(b, prev + 0.4)
        ajust.append(b); prev = b
    marcas = [ini] + ajust + [fin]
    res = []
    for i, f in enumerate(fs):
        s, e = marcas[i], marcas[i + 1]
        palabras = f.split()
        pw = [peso(w) for w in palabras]
        t, ws = s, []
        for w, p in zip(palabras, pw):
            d = (e - s) * p / sum(pw)
            ws.append({"w": w, "s": round(t, 3), "e": round(t + d, 3)})
            t += d
        res.append({"text": f, "s": round(s, 3), "e": round(e, 3), "words": ws})
    return {"dur": round(dur, 3), "phrases": res}


def srt_time(t):
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def escribe_srt(path, items):
    with open(path, "w", encoding="utf-8") as f:
        for i, (s, e, t) in enumerate(items, 1):
            f.write(f"{i}\n{srt_time(s)} --> {srt_time(e)}\n{t}\n\n")


def main():
    os.makedirs(OUTV, exist_ok=True)
    nombres = sorted(n[:-4] for n in os.listdir(TXT) if n.endswith(".txt"))
    data = {n: alinea(n) for n in nombres}
    json.dump(data, open(f"{RAIZ}/montaje/src/data/tiempos.json", "w"), ensure_ascii=False, indent=1)
    # SRT del largo (con el mismo desfase que el montaje: 0,3 s entre bloques)
    off, items = 0.0, []
    for n in [x for x in nombres if x.startswith("largo")]:
        for p in data[n]["phrases"]:
            items.append((off + p["s"], off + p["e"], p["text"]))
        off += data[n]["dur"] + GAP
    # los .srt definitivos los escribe plan.py en la carpeta de cada vídeo (con el desfase de la intro)
    outs = {"short01": "short01-pez-piedra", "short02": "short02-pez-arana", "short03": "short03-ornitorrinco"}

    for n in nombres:
        print(n, data[n]["dur"], len(data[n]["phrases"]), "frases")


if __name__ == "__main__":
    main()
