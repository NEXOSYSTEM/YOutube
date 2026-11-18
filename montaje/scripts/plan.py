"""Construye montaje/src/data/plan.json a partir de escenas.json + _catalogo.json + tiempos.json.

- Duración de cada bloque = su audio (+0,3 s de silencio en el largo).
- Escenas repartidas en proporción a los tiempos del guion; planos de 3–5 s (largo) o 1,5–3 s (Shorts).
- Enlaza (hardlink) audios y material en montaje/public/ para que Remotion los sirva.
- Genera material/2026-11-18-semana-01/creditos.md con la escena en la que se usa cada archivo.
"""
import json, math, os, random, re, sys

RAIZ = os.environ.get("ALUCINATE_RAIZ") or os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
import sys as _s, os as _o; _s.path.insert(0, _o.path.dirname(_o.path.abspath(__file__))); import semana as S  # rutas de la semana
MAT = S.MAT
PUB = f"{RAIZ}/montaje/public"
FPS = int(os.environ.get("VIDEO_FPS", "25"))  # 25 fps por defecto (decisión de Luis, 2026-11-18)
GAP = 0.3
ESC = json.load(open(f"{RAIZ}/montaje/src/data/escenas.json", encoding="utf-8"))
CAT = json.load(open(f"{MAT}/_catalogo.json", encoding="utf-8"))
TIE = json.load(open(f"{RAIZ}/montaje/src/data/tiempos.json", encoding="utf-8"))
ITEMS = CAT["items"]
rnd = random.Random(42)

KEYWORDS = set("""veneno venenoso venenosos venenosa venenosas tóxico tóxica tóxicos toxinas tetrodotoxina antídoto mortal matarte mata
dolor dolorosas dolorosos insoportable parálisis espinas espina aguijón colmillos opioides urgencias socorrista caliente
españa islandia japón índico pacífico atlántico caribe mediterráneo ártico cuatrocientos dieciocho trece diez nueve ocho siete seis
cinco cuatro tres dos uno conejo blenio groenlandia gato cabracho araña pastinaca león globo piedra fugu hákarl
ornitorrinco peluche espolón huevos electricidad semanas celo miedo pisas pisa lo pisa invadido plaga""".split())

usage = {}  # page -> set(escenas)
cursor = {}  # pool -> índice


def link(src_rel_mat=None, src_abs=None, dst_rel=None):
    src = src_abs or f"{MAT}/{src_rel_mat}"
    dst = f"{PUB}/{dst_rel}"
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.exists(dst) and os.stat(dst).st_ino != os.stat(src).st_ino:
        os.remove(dst)  # el original cambió (p. ej. audio regenerado): rehacer el enlace
    if not os.path.exists(dst):
        os.link(src, dst)
    return dst_rel


import subprocess as _sp
try:
    import imageio_ffmpeg as _iio
    _FF = _iio.get_ffmpeg_exe()
except Exception:
    _FF = None


def fondo_desenfocado(file):
    dst_rel = f"material/_desenfoque/{os.path.splitext(file)[0]}.jpg"
    dst = f"{PUB}/{dst_rel}"
    if not os.path.exists(dst) and _FF:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        _sp.run([_FF, "-y", "-loglevel", "error", "-i", f"{MAT}/{file}", "-vf",
                 "scale=640:-2,boxblur=24:3,eq=brightness=-0.22:saturation=1.1", "-frames:v", "1", "-q:v", "4", dst])
    return dst_rel


def media(page, scene_id):
    it = ITEMS[page]
    usage.setdefault(page, set()).add(scene_id)
    rel = link(it["file"], dst_rel=f"material/{it['file']}")
    m = {"src": rel, "video": it["video"], "w": it["w"], "h": it["h"], "dur": it.get("dur", 0), "entero": es_animal(page)}
    if m["entero"] and not it["video"]:
        m["bg"] = fondo_desenfocado(it["file"])  # fondo ya desenfocado con ffmpeg: Remotion no calcula blur por fotograma
    return m


CUR_PATH = f"{RAIZ}/montaje/src/data/curacion.json"
CUR = json.load(open(CUR_PATH, encoding="utf-8")) if os.path.exists(CUR_PATH) else {"pools": {}, "queries": {}}
BY_FILE = {it["file"]: page for page, it in ITEMS.items()}
CUR["excluir_pages"] = [page for f, page in BY_FILE.items() if any(f.startswith(e + "_") for e in CUR.get("excluir", []))]


def curado(folder, prefijos):
    """Lista curada a mano: prefijos «NN» de archivos dentro de la carpeta, en orden de preferencia."""
    out = []
    for pre in prefijos:
        ruta = pre if "/" in pre else f"{folder}/{pre}"
        for f, page in BY_FILE.items():
            if f.startswith(f"{ruta}_"):
                out.append(page)
    return out


def pool_list(name):
    if name in CUR.get("pools", {}):
        return curado(name, CUR["pools"][name])
    return [p for p in CAT["pools"].get(name, []) if p in ITEMS]


ESPECIE_V = set()
for _k, _v in CUR.get("videos_especie", {}).items():
    for _pre in _v:
        for _f, _pg in BY_FILE.items():
            if _f.startswith(_pre + "_"):
                ESPECIE_V.add(_pg)


def es_animal(page):
    it = ITEMS[page]
    carpeta = it["file"].split("/")[0]
    return (carpeta in ESC["pools"] and not it["video"]) or page in ESPECIE_V


def from_pool(name, scene_id, avoid=()):
    lst = pool_list(name)
    if not lst:
        return None
    i = cursor.get(name, 0)
    for k in range(len(lst)):
        p = lst[(i + k) % len(lst)]
        if p not in avoid:
            cursor[name] = (i + k + 1) % len(lst)
            return media(p, scene_id)
    cursor[name] = (i + 1) % len(lst)
    return media(lst[i % len(lst)], scene_id)


FALLBACK = {"generico": "0.7"}
incidencias = []


def scene_media(s, n, sid):
    """Devuelve n medios para la escena (sus resultados propios, luego el pool)."""
    out = []
    if s.get("pool"):
        for _ in range(n):
            m = from_pool(s["pool"], sid)
            if m:
                out.append(m)
        return out
    qid = s.get("id_q", s["id"])
    if qid in CUR.get("queries", {}):
        own = curado(CUR["queries"][qid]["folder"], CUR["queries"][qid]["files"])
    else:
        own = [p for p in CAT["queries"].get(qid, []) if p in ITEMS and p not in CUR.get("excluir_pages", [])]
    # vídeos primero (dan más vida), luego imágenes
    own = sorted(own, key=lambda p: (not ITEMS[p]["video"]))
    for i in range(n):
        if own:
            out.append(media(own[i % len(own)], sid))
    if not out:
        folder = s.get("folder")
        if folder in ESC["pools"]:
            incidencias.append(f"Escena {sid}: sin resultados propios para {s.get('q')}; se usa material de «{folder}».")
            return [from_pool(folder, sid) for _ in range(n)]
        fb = [p for p in CAT["queries"].get(FALLBACK.get(folder, "0.7"), []) if p in ITEMS]
        incidencias.append(f"Escena {sid}: sin resultados para {s.get('q')}; se usa un plano genérico de fondo marino.")
        out = [media(fb[i % len(fb)], sid) for i in range(n)] if fb else []
    return out


usos_video = {}
cursor_v = {}


def video_media(page, scene_id):
    """Medio de vídeo; si el clip se repite, empieza en otro punto (cada uso, +5 s)."""
    m = media(page, scene_id)
    n = usos_video.get(page, 0); usos_video[page] = n + 1
    dur = ITEMS[page].get("dur", 0) or 0
    m["start"] = round((n * 5) % max(1, dur - 4), 2) if dur > 8 else 0
    # clips cuyo original empieza con fundido a negro u otro defecto: arrancar más tarde
    for pref, ini in CUR.get("inicio_clip", {}).items():
        if ITEMS[page]["file"].startswith(pref + "_"):
            m["start"] = max(m["start"], ini)
    return m


def videos_de(lista_curada):
    return curado("", lista_curada) if lista_curada else []


def siguiente_video(clave, lista, scene_id):
    if not lista:
        return None
    i = cursor_v.get(clave, 0); cursor_v[clave] = i + 1
    return video_media(lista[i % len(lista)], scene_id)


def kb(i, entero=False):
    modes = ["in", "out", "left", "right", "up", "in", "right", "left"]
    if entero:  # animal entero: solo zoom suave (≤8 %) centrado, sin paneos que corten cabeza o cola
        return {"mode": ["in", "out"][(i + rnd.randint(0, 1)) % 2], "amt": round(rnd.uniform(0.05, 0.08), 3)}
    return {"mode": modes[(i + rnd.randint(0, 7)) % len(modes)], "amt": round(rnd.uniform(0.08, 0.16), 3)}


TRANS = ["punch", "slide", "cut", "flash", "punch", "whip"]


def build(blocks, short=False, cuts=None):
    """blocks: lista de (audio, bloque_escenas). cuts: {audio: segundos} para recortar (prueba)."""
    cuts = cuts or {}
    seq, f0, shot_i, captions, sfx = [], 0, 0, [], []
    lo, hi = (1.5, 3.0) if short else (3.0, 5.0)
    for bi, b in enumerate(blocks):
        if b.get("video"):  # bloque de intro: vídeo propio con su sonido, sin narración ni subtítulos
            vrel = link(src_abs=b["video"], dst_rel=f"intro/{os.path.basename(b['video'])}")
            seq.append({"video": vrel, "from": f0, "len": b["frames"], "scenes": [], "rank": None, "ficha": None})
            f0 += b["frames"]
            continue
        a = b["audio"]
        adur = TIE[a]["dur"]
        cut = cuts.get(a)
        use = min(adur, cut) if cut else adur
        bdur = use + (0 if short else GAP)
        bf = round(bdur * FPS)
        scenes = b["scenes"]
        if cut:  # recortar escenas a las que caben
            tot, acc, keep = sum(s["t"] for s in scenes), 0, []
            full = adur
            for s in scenes:
                st = acc / tot * full
                if st < use - 1:
                    keep.append(s)
                acc += s["t"]
            scenes = keep
            tot_keep = sum(s["t"] for s in scenes)
        tot = sum(s["t"] for s in scenes)
        acc = 0
        sc_out = []
        for si, s in enumerate(scenes):
            s0 = round(acc / tot * bf); acc += s["t"]; s1 = round(acc / tot * bf)
            sd = (s1 - s0) / FPS
            g = s.get("graphic")
            if g in ("title", "split", "counter", "map", "size", "swallow", "years", "steps", "organs", "black",
                     "spines", "calendar", "montage", "end"):
                n = 1
            else:
                n = max(1, min(int(sd / lo), round(sd / ((lo + hi) / 2)) or 1))
                while sd / n > hi and n < 12:
                    n += 1
            shots = []
            if g in (None, "step", "title", "years"):
                if g == "years":
                    ms = [from_pool("groenlandia", s["id"])]
                elif g == "step" and not s.get("q"):
                    ms = []
                else:
                    ms = scene_media(s, n if g is None else 1, s["id"])
                if g is None:
                    vesc = videos_de(CUR.get("videos_escena", {}).get(s["id"]))
                    animal = s.get("pool") or (s.get("folder") if s.get("folder") in ESC["pools"] else None)
                    vpool = videos_de(CUR.get("videos_pool", {}).get(animal)) if animal else []
                    fija = s.get("circle") or s.get("reveal") or s.get("hold")
                    # plano de presentación del animal (1.ª escena de su bloque): nunca vídeo de otra especie
                    presenta = si == 0 and (b.get("rank") or short)
                    if presenta and animal:
                        vpool = videos_de(CUR.get("videos_especie", {}).get(animal))
                        if not vpool:
                            fija = True
                    nuevos = []
                    for k in range(n):
                        if vesc:
                            nuevos.append(siguiente_video(f"esc:{s['id']}", vesc, s["id"]))
                        elif vpool and not fija and (k % 3 != 2 or n == 1 and not ms):
                            nuevos.append(siguiente_video(f"pool:{animal}", vpool, s["id"]))
                        else:
                            nuevos.append(ms[k % len(ms)] if ms else siguiente_video(f"pool:{animal}", vpool, s["id"]))
                    ms = nuevos
                ln = s1 - s0
                for k in range(n if g is None else 1):
                    a0 = round(k * ln / (n if g is None else 1)); a1 = round((k + 1) * ln / (n if g is None else 1))
                    m = ms[k] if g is None and k < len(ms) else (ms[k % len(ms)] if ms else None)
                    shots.append({"from": a0, "len": a1 - a0, "media": m, "kb": kb(shot_i, bool(m and m.get("entero"))),
                                  "trans": "cut" if (k == 0 and si == 0) else TRANS[shot_i % len(TRANS)]})
                    shot_i += 1
            extra = {}
            if g == "split":
                for side in ("left", "right"):
                    sd_ = s[side]
                    if sd_.get("pool"):
                        extra[side] = from_pool(sd_["pool"], s["id"])
                    else:
                        sub = dict(sd_, id=f"{s['id']}{side[0]}")
                        ms = scene_media(sub, 1, s["id"])
                        extra[side] = ms[0] if ms else None
            if g == "map":
                extra["map"] = media(CAT["mapa"], s["id"]) if CAT.get("mapa") else None
            if g == "montage":
                order = ["pez-conejo", "blenio", "groenlandia", "pez-gato", "cabracho", "pez-arana", "pastinaca",
                         "pez-leon", "pez-globo", "pez-piedra"]
                extra["montage"] = [from_pool(p, s["id"]) for p in order]
            if g == "title":
                extra["bg"] = shots[0]["media"] if shots else None
                shots = []
            if g == "years":
                extra["bg"] = shots[0]["media"] if shots else None
                shots = []
            if g == "step":
                extra["bg"] = shots[0]["media"] if shots and shots[0]["media"] else None
                shots = []
            sc = {k: v for k, v in s.items() if k not in ("q", "pool", "folder", "t", "left", "right")}
            sc.update({"from": s0, "len": s1 - s0, "shots": shots, **extra})
            sc_out.append(sc)
            # sonido: whoosh corto en cada cambio de escena (no en la escena respetuosa)
            if si > 0 and not s.get("soft"):
                sfx.append({"f": f0 + s0, "s": "whoosh-corto", "v": 0.35})
            if g in ("black", "title"):
                sfx.append({"f": f0 + s0, "s": "impacto", "v": 0.7})
            if s.get("text"):
                sfx.append({"f": f0 + s0 + 8, "s": "pop", "v": 0.25})
        blk = {"audio": f"audio/{a}.wav", "from": f0, "len": bf, "audioLen": round(use * FPS),
               "rank": b.get("rank"), "ficha": b.get("ficha"), "fichaAt": None, "scenes": sc_out, "cut": bool(cut)}
        if b.get("fichaAt"):
            for sc in sc_out:
                if sc["id"] == b["fichaAt"]:
                    blk["fichaAt"] = sc["from"]
        if b.get("rank"):
            sfx.append({"f": f0, "s": "whoosh", "v": 0.6})
            sfx.append({"f": f0 + 6, "s": "impacto", "v": 0.45})
        link(src_abs=f"{S.AUD}/{a}.wav", dst_rel=f"audio/{a}.wav")
        for p in TIE[a]["phrases"]:
            if p["s"] >= use:
                break
            words = [{"w": w["w"], "s": round(f0 + w["s"] * FPS), "e": round(f0 + min(w["e"], use) * FPS),
                      "k": re.sub(r"[^\wáéíóúüñ]", "", w["w"].lower()) in KEYWORDS} for w in p["words"]]
            captions.append({"s": round(f0 + p["s"] * FPS), "e": round(f0 + min(p["e"], use) * FPS), "words": words})
        seq.append(blk)
        f0 += bf
    return {"blocks": seq, "len": f0, "captions": captions, "sfx": sfx}


def credits_md(plan_usage):
    by = sorted(plan_usage.items(), key=lambda kv: ITEMS[kv[0]]["file"])
    lines = ["# Créditos del material — semana 1 (2026-11-18)", "",
             "Solo material con licencia libre: CC0, dominio público, CC BY, CC BY-SA (marcado «BY-SA») y Mixkit Stock Video Free License.",
             "Nada con NC ni ND. Nada de YouTube ni de TikTok. Efectos de sonido: sintetizados por nosotros (montaje/scripts/sfx.py), sin licencia de terceros.", "",
             "| Archivo | Autor | Licencia | Fuente | Escenas |", "|---|---|---|---|---|"]
    for page, sc in by:
        it = ITEMS[page]
        lic = it["license"] + (" · **BY-SA**" if it["rank"] == 2 else "")
        auth = it["author"].replace("|", "/").replace("\n", " ")
        lines.append(f"| {it['file']} | {auth} | {lic} | {page} | {', '.join(sorted(sc))} |")
    unused = [p for p in ITEMS if p not in plan_usage]
    lines += ["", f"Archivos descargados que no se usan en el montaje: {len(unused)} (se pueden borrar o guardar para otros vídeos).", ""]
    lines += ["## Texto para pegar en la descripción de YouTube", "", "```", "🎞️ Imágenes y vídeos (licencias libres):"]
    for page, sc in by:
        it = ITEMS[page]
        if it["rank"] in (1, 2) or (it["src"] == "Wikimedia Commons" and it["rank"] == 0):
            nm = re.sub(r"^File:", "", it["title"])
            lines.append(f"• «{nm}» — {it['author'][:80]} — {it['license']} — {page}")
    lines += ["Clips de vídeo adicionales: Mixkit (Mixkit Stock Video Free License).", "```", ""]
    open(f"{MAT}/creditos.md", "w", encoding="utf-8").write("\n".join(lines))


def credit_lines(plan_usage):
    out = []
    for page in sorted(plan_usage, key=lambda p: ITEMS[p]["author"].lower()):
        it = ITEMS[page]
        if it["src"] == "Mixkit":
            continue
        out.append(f"{it['author'][:40]} · {it['license']}")
    out = sorted(set(out))
    return out + ["Clips: Mixkit (Free License)", "Mapa: NASA (dominio público)"]


def main():
    largo = [b for b in ESC["largo"]]
    intro = CUR.get("intro_largo")
    if intro:
        largo.insert(intro.get("despues_de_bloque", 1), {"video": f"{RAIZ}/{intro['archivo']}", "frames": round(intro["frames"] / 30 * FPS)})  # «frames» está a 30 fps
    plan = {"fps": FPS}
    plan["largo"] = build(largo)
    u_largo = {p: set(s) for p, s in usage.items()}
    plan["largo"]["credits"] = credit_lines(u_largo)
    plan["largo"]["len"] += 3 * FPS  # créditos finales
    plan["largo"]["fuentes"] = sorted(u_largo)
    for k, sh in ESC["shorts"].items():
        antes = {pg: set(v) for pg, v in usage.items()}
        p = build([{"audio": k, "scenes": sh["scenes"]}], short=True)
        p.update({"hook": sh["hook"], "out": sh["out"]})
        p["fuentes"] = sorted(pg for pg, v in usage.items() if any(x.startswith("S") for x in v - antes.get(pg, set())))
        plan[k] = p
    cursor.clear()
    prueba = build([ESC["largo"][0], ESC["largo"][2]],
                   cuts={"largo-01-gancho": 19.45, "largo-03-n10-pez-conejo": 13.0})
    prueba["credits"] = []
    plan["prueba"] = prueba
    # Miniaturas: imagen elegida a mano en curacion.json -> "miniaturas"
    plan["thumbs"] = {}
    for k, cfg in CUR.get("miniaturas", {}).items():
        pages = curado("", [cfg["img"]])
        if pages:
            m = media(pages[0], f"miniatura-{k}")
            plan["thumbs"][k] = {kk: vv for kk, vv in cfg.items() if kk != "img"} | {"img": m["src"]}
    # Créditos solo de lo que sale de verdad en cada vídeo (tras cambiar fotos por vídeo)
    for k in ["largo"] + list(ESC["shorts"]):
        en_video = json.dumps(plan[k]["blocks"], ensure_ascii=False)
        plan[k]["fuentes"] = [pg for pg in plan[k]["fuentes"]
                              if ITEMS.get(pg, {}).get("file", "\0").split("/")[-1] in en_video]
    json.dump(plan, open(f"{RAIZ}/montaje/src/data/plan.json", "w"), ensure_ascii=False, indent=1)
    # SRT de cada vídeo a partir del plan (incluye el desfase de la intro)
    def srt(caps, path):
        def ts(fr):
            ms = round(fr / FPS * 1000)
            return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"
        with open(path, "w", encoding="utf-8") as fh:
            for i, c in enumerate(caps, 1):
                fh.write(f"{i}\n{ts(c['s'])} --> {ts(c['e'])}\n{' '.join(w['w'] for w in c['words'])}\n\n")
    # una carpeta por vídeo, con fecha (decisión de Luis, 2026-11-18)
    CARPETAS = S.CARP
    for k, carpeta in CARPETAS.items():
        os.makedirs(f"{RAIZ}/videos/{carpeta}", exist_ok=True)
    srt(plan["largo"]["captions"], f"{RAIZ}/videos/{S.VID['largo']}.srt")
    for k in ESC["shorts"]:
        srt(plan[k]["captions"], f"{RAIZ}/videos/{CARPETAS[k]}/{plan[k]['out']}.srt")
    credits_md(usage)
    open(f"{RAIZ}/montaje/src/data/incidencias.txt", "w").write("\n".join(sorted(set(incidencias))))
    print("largo", plan["largo"]["len"] / FPS, "s ·", {k: plan[k]["len"] / FPS for k in ESC["shorts"]}, "· prueba", prueba["len"] / FPS)
    print("\n".join(sorted(set(incidencias))))


if __name__ == "__main__":
    main()
