import React from "react";
import { Composition, Still, AbsoluteFill, Img, staticFile } from "remotion";
import { Largo, Short } from "./Video";
import { tema } from "./tema";
import { HojaLogos, LogoSuelto, LogoAnimado, Banner, Intro } from "./logos";
import { Avatar, IconoTransparente, LogoCompleto, LogoHorizontalClaro, BannerFinal, HojaResumen } from "./marca";
import { IntroLupa, IntroOrbita, IntroCorta, INTRO_LUPA_TOTAL, INTRO_LUPA_FIN } from "./intro";
import plan from "./data/plan.json";

const C = tema.color;
// Música opcional: pon aquí la ruta (dentro de public/) de una pista de la biblioteca de audio de YouTube, p. ej. "musica/tension.mp3".
const MUSICA = "musica/fondo-largo.wav"; // música propia sintetizada (montaje/scripts/sonido_musica.py)
const MUSICA_SHORT = "musica/fondo-short.wav";

// ---------- Miniaturas ----------
const Miniatura = ({ img, texto, sub, pos = "50% 50%", flecha = true, circulo = { x: 640, y: 400, rx: 330, ry: 210 }, vertical = false, color = C.acento }) => (
  <AbsoluteFill style={{ background: "#000" }}>
    <Img src={staticFile(img)} style={{ width: "100%", height: "100%", objectFit: "cover", objectPosition: pos, filter: "contrast(1.25) saturate(1.4) brightness(1.02)" }} />
    <AbsoluteFill style={{ background: "radial-gradient(ellipse at 50% 55%, rgba(0,0,0,0) 35%, rgba(0,0,0,.8) 100%)" }} />
    {circulo && (
      <svg width="100%" height="100%" style={{ position: "absolute" }}>
        <ellipse cx={circulo.x} cy={circulo.y} rx={circulo.rx} ry={circulo.ry} fill="none" stroke={C.peligro} strokeWidth={vertical ? 22 : 16} style={{ filter: "drop-shadow(0 0 10px #000)" }} />
        {flecha && <g style={{ filter: "drop-shadow(0 0 8px #000)" }}>
          <path d={`M ${circulo.x + circulo.rx + 230} ${circulo.y - circulo.ry - 60} L ${circulo.x + circulo.rx * 0.72 + 20} ${circulo.y - circulo.ry * 0.5}`} stroke={C.peligro} strokeWidth="26" strokeLinecap="round" />
          <path d={`M ${circulo.x + circulo.rx * 0.72} ${circulo.y - circulo.ry * 0.5} l 80 -10 l -48 -62 z`} fill={C.peligro} stroke={C.peligro} strokeWidth="14" strokeLinejoin="round" />
        </g>}
      </svg>
    )}
    <AbsoluteFill style={{ alignItems: vertical ? "center" : "flex-start", justifyContent: vertical ? "flex-start" : "flex-start", padding: vertical ? "220px 40px" : "36px 50px" }}>
      <div style={{ ...tema.rotulo(vertical ? 150 : 132, color), WebkitTextStroke: `${vertical ? 14 : 12}px #000`, textAlign: vertical ? "center" : "left", transform: "rotate(-3deg)" }}>{texto}</div>
      {sub && <div style={{ ...tema.rotulo(vertical ? 76 : 58), marginTop: 10, textAlign: vertical ? "center" : "left" }}>{sub}</div>}
    </AbsoluteFill>
  </AbsoluteFill>
);

const thumbs = plan.thumbs || {};

export const Root = () => (
  <>
    <Still id="MarcaAvatar" component={Avatar} width={800} height={800} />
    <Still id="MarcaIcono" component={IconoTransparente} width={1024} height={1024} />
    <Still id="MarcaMarcaAgua" component={IconoTransparente} width={150} height={150} />
    <Still id="MarcaLogoOscuro" component={LogoCompleto} width={1200} height={1200} defaultProps={{ fondo: true }} />
    <Still id="MarcaLogoTransparente" component={LogoCompleto} width={1200} height={1200} defaultProps={{ fondo: false }} />
    <Still id="MarcaLogoHorizontalClaro" component={LogoHorizontalClaro} width={1800} height={600} />
    <Still id="MarcaBanner" component={BannerFinal} width={2560} height={1440} />
    <Still id="MarcaBannerGuias" component={BannerFinal} width={2560} height={1440} defaultProps={{ guias: true }} />
    <Still id="MarcaHojaResumen" component={HojaResumen} width={2100} height={1340} />
    <Still id="HojaLogos" component={HojaLogos} width={2400} height={1400} />
    <Still id="Banner" component={Banner} width={2560} height={1440} defaultProps={{ v: 4, guias: false }} />
    <Still id="BannerGuias" component={Banner} width={2560} height={1440} defaultProps={{ v: 4, guias: true }} />
    <Composition id="IntroLupa" component={IntroLupa} durationInFrames={INTRO_LUPA_TOTAL} fps={30} width={1920} height={1080} />
    <Composition id="IntroLupaVertical" component={IntroLupa} durationInFrames={INTRO_LUPA_TOTAL - INTRO_LUPA_FIN + 6} fps={30} width={1080} height={1920} defaultProps={{ vertical: true, desde: INTRO_LUPA_FIN - 6 }} />
    <Composition id="IntroCorta" component={IntroCorta} durationInFrames={90} fps={30} width={1920} height={1080} />
    <Composition id="IntroOrbita" component={IntroOrbita} durationInFrames={180} fps={30} width={1920} height={1080} />
    <Composition id="Intro" component={Intro} durationInFrames={120} fps={30} width={1920} height={1080} defaultProps={{ v: 2 }} />
    <Still id="HojaLogos2" component={HojaLogos} width={2400} height={1400} defaultProps={{ vs: [5, 6, 7, 8] }} />
    {[1, 2, 3, 4, 5, 6, 7, 8].map((v) => <Still key={`l${v}`} id={`Logo${v}`} component={LogoSuelto} width={1200} height={1200} defaultProps={{ v, dark: false }} />)}
    {[1, 2, 3, 4, 5, 6, 7, 8].map((v) => <Still key={`lo${v}`} id={`Logo${v}Oscuro`} component={LogoSuelto} width={1200} height={1200} defaultProps={{ v, dark: true }} />)}
    {[1, 2, 3, 4, 5, 6, 7, 8].map((v) => <Composition key={`la${v}`} id={`LogoAnimado${v}`} component={LogoAnimado} durationInFrames={90} fps={30} width={1920} height={1080} defaultProps={{ v }} />)}
    <Composition id="Largo" component={Largo} durationInFrames={plan.largo.len} fps={plan.fps || 30} width={1920} height={1080} defaultProps={{ plan: plan.largo, musica: MUSICA, post: false }} />
    <Composition id="Prueba" component={Largo} durationInFrames={plan.prueba.len} fps={plan.fps || 30} width={1920} height={1080} defaultProps={{ plan: plan.prueba, musica: MUSICA }} />
    {["short01", "short02", "short03"].map((k) => (
      <Composition key={k} id={k.replace("short", "Short")} component={Short} durationInFrames={plan[k].len} fps={plan.fps || 30} width={1080} height={1920} defaultProps={{ plan: plan[k], musica: MUSICA_SHORT }} />
    ))}
    {thumbs.largo && <Still id="MiniaturaLargo" component={Miniatura} width={1280} height={720} defaultProps={thumbs.largo} />}
    {["short01", "short02", "short03"].map((k) => thumbs[k] && (
      <Still key={k} id={`Miniatura${k.replace("short", "Short")}`} component={Miniatura} width={1080} height={1920} defaultProps={{ ...thumbs[k], vertical: true }} />
    ))}
  </>
);
