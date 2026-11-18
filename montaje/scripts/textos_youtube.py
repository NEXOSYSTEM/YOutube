"""Descripción (con capítulos y créditos), etiquetas y miniatura en la carpeta de cada vídeo.
YouTube limita la descripción a 5.000 caracteres: los créditos se agrupan por autor y licencia
(«Autor · CC BY 4.0 · vía Wikimedia Commons»). La lista completa con enlaces va en comentario-creditos.txt
para fijarla como comentario, y en material/2026-11-18-semana-01/creditos.md."""
import json, re, shutil

RAIZ = "/Users/luis/Desktop/Youtube/Alucinateconelmundo"
FPS = json.load(open("/Users/luis/Desktop/Youtube/Alucinateconelmundo/montaje/src/data/plan.json")).get("fps", 30)
PLAN = json.load(open(f"{RAIZ}/montaje/src/data/plan.json", encoding="utf-8"))
CAT = json.load(open(f"{RAIZ}/material/2026-11-18-semana-01/_catalogo.json", encoding="utf-8"))["items"]
CARP = {"largo": "2026-11-18-largo-peces-venenosos", "short01": "2026-11-18-short-pez-piedra",
        "short02": "2026-11-18-short-pez-arana", "short03": "2026-11-18-short-ornitorrinco"}
MINI = {"largo": "largo-peces-venenosos.jpg", "short01": "short01.jpg", "short02": "short02.jpg", "short03": "short03.jpg"}

def ts(fr):
    s = int(fr / FPS); return f"{s // 60}:{s % 60:02d}"

def creditos(fuentes):
    grupos, pd = {}, set()
    for pg in fuentes:
        it = CAT[pg]
        if it["src"] == "Mixkit":
            pd.add("Mixkit (licencia gratuita)"); continue
        lic = it["license"]
        if it["rank"] == 0:  # CC0 / dominio público: no exige atribución, pero se menciona
            a = re.sub(r"\s+", " ", it["author"])[:40]
            pd.add("NOAA" if "NOAA" in it["title"] or "NOAA" in a else ("NASA" if "NASA" in a else a))
            continue
        a = re.sub(r"\s+", " ", it["author"]).strip()[:60]
        grupos.setdefault((a, lic), []).append(pg)
    corto = [f"• {a} · {lic}{' (' + str(len(v)) + ')' if len(v) > 1 else ''}" for (a, lic), v in sorted(grupos.items(), key=lambda x: x[0][0].lower())]
    largo = []
    for (a, lic), v in sorted(grupos.items(), key=lambda x: x[0][0].lower()):
        for pg in v:
            largo.append(f"• «{re.sub(r'^File:', '', CAT[pg]['title'])}» — {a} — {lic} — {pg}")
    return corto, largo, sorted(pd)

def escribe(k, cuerpo, etiquetas, fuentes):
    d = f"{RAIZ}/videos/{CARP[k]}"
    corto, largo, pd = creditos(fuentes)
    cred = ["", "🎞️ Imágenes y vídeos con licencia libre (vía Wikimedia Commons):", *corto]
    if pd:
        cred.append("Dominio público / CC0: " + ", ".join(pd))
    cred += ["Música, efectos y gráficos: originales del canal. Narración: voz sintética.", "Lista completa con enlaces: en el comentario fijado."]
    texto = cuerpo.strip() + "\n" + "\n".join(cred) + "\n"
    if len(texto) > 4900:  # recorte de seguridad (límite de YouTube: 5.000)
        texto = texto[:4850].rsplit("\n", 1)[0] + "\n…(ver comentario fijado)\n"
    open(f"{d}/descripcion.txt", "w", encoding="utf-8").write(texto)
    open(f"{d}/comentario-creditos.txt", "w", encoding="utf-8").write("📚 Créditos de imágenes y vídeos (licencias libres):\n" + "\n".join(largo) + ("\nDominio público / CC0: " + ", ".join(pd) if pd else "") + "\n")
    open(f"{d}/etiquetas.txt", "w", encoding="utf-8").write(", ".join(etiquetas) + "\n")
    shutil.copy(f"{RAIZ}/miniaturas/2026-11-18-semana-01/{MINI[k]}", f"{d}/miniatura.jpg")
    print(k, "descripción", len(texto), "caracteres ·", len(largo), "créditos con enlace")

# ---- Largo ----
L = PLAN["largo"]
caps, n_rank = [], 0
nombres = {"largo-02-intro": "Venenoso vs. tóxico"}
for b in L["blocks"]:
    if b.get("video"):
        continue
    a = b["audio"].split("/")[-1][:-4]
    if a == "largo-01-gancho":
        caps.append((b["from"], "Intro"))
    elif a in nombres:
        caps.append((b["from"], nombres[a]))
    elif b.get("rank"):
        caps.append((b["from"], b["rank"].title().replace("#", "#").replace("De ", "de ")))
caps_txt = "\n".join(f"{ts(f)} {t}" for f, t in caps)
cuerpo_largo = f"""Los 10 peces más venenosos (y tóxicos) del océano: desde el pez conejo hasta el pez piedra, el pez más venenoso que se conoce. Dos de ellos viven en las costas de España.

⏱️ Capítulos
{caps_txt}

⚠️ La información de primeros auxilios es general. Ante cualquier picadura, consulta a un profesional sanitario.

📚 Fuentes
• Tiburón de Groenlandia: Nielsen et al. (2016), Science — edad estimada ≈392 años (272–512).
• Blenio colmillo: Casewell et al. (2017), Current Biology — veneno con péptidos opioides.
• Pez león: Florida Fish and Wildlife Conservation Commission — 18 espinas venenosas; primer registro en Florida en 1985.
• Pez piedra, pez araña, pastinaca, pez globo y cabracho: FishBase y literatura médica sobre picaduras de peces.

#animales #peces #datoscuriosos #océano #sabíasque
"""
etq_largo = ["peces venenosos", "peces más venenosos del mundo", "pez piedra", "pez globo", "fugu", "pez araña", "pez león",
             "cabracho", "pastinaca", "tiburón de Groenlandia", "animales venenosos", "curiosidades del mar", "alucínate con el mundo"]
escribe("largo", cuerpo_largo, etq_largo, L["fuentes"])

# ---- Shorts ----
SH = {
    "short01": ("Este pez parece una piedra… y es el más venenoso del mundo 🪨☠️",
                "El pez piedra es el pez más venenoso que se conoce. Vídeo completo con los 10 peces más venenosos en el canal. #animales #peces #datoscuriosos #shorts",
                ["pez piedra", "pez más venenoso", "animales venenosos", "curiosidades", "shorts", "alucínate con el mundo"]),
    "short02": ("¿Qué pasa si te pica un PEZ ARAÑA en la playa? 🏖️",
                "El pez araña vive enterrado en la arena de muchas playas de España. Información general: ante una picadura, consulta a un profesional sanitario. #animales #playa #peces #sabíasque #shorts",
                ["pez araña", "picadura pez araña", "playas de España", "qué hacer si te pica", "shorts", "alucínate con el mundo"]),
    "short03": ("El ornitorrinco parece un peluche… y tiene VENENO 🦆☠️",
                "El ornitorrinco es uno de los pocos mamíferos venenosos: los machos tienen un espolón con veneno en las patas traseras. #animales #ornitorrinco #datoscuriosos #shorts",
                ["ornitorrinco", "mamíferos venenosos", "animales raros", "curiosidades", "shorts", "alucínate con el mundo"]),
}
for k, (titulo, desc, etq) in SH.items():
    escribe(k, f"Título: {titulo}\n\n{desc}\n", etq, PLAN[k]["fuentes"])
