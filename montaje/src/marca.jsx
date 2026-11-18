import React from "react";
import { AbsoluteFill, staticFile, useVideoConfig } from "remotion";
import { tema } from "./tema";
import { Globo, Grad } from "./logos";

// Identidad final del canal, sacada del final de la intro: lupa (aro, mango y brillo de la intro) con el planeta
// dentro del cristal (degradado + continentes reales en negro, vista del Atlántico) y «ALUCÍNATE / CON EL MUNDO».
const AROS = "#13233A";
const FONDO = "#0B1220";
const VERDE = "#7EDC86";
const CONT = ["norteamerica", "sudamerica", "europa", "africa"];

// Planeta con continentes (centro 0,0; radio r)
const PlanetaReal = ({ r, id }) => (
  <g>
    <Globo r={r} rot={20} w={Math.max(2, r / 45)} fill={`url(#gA${id})`} line="rgba(255,255,255,.16)" />
    {CONT.map((k) => <image key={k} href={staticFile(`intro/continente-${k}.png`)} x={-r} y={-r} width={2 * r} height={2 * r} />)}
  </g>
);

// Icono: lupa con el planeta dentro (viewBox 600×600). Mismas proporciones que la lupa de la intro.
export const IconoLupa = ({ size = 600, id = "a" }) => {
  const r = 190;
  const k = r / 125; // la lupa de la intro tiene radio 125
  const ri = r - 11 * k; // el borde del planeta queda bajo el aro (que va de r−14k a r+14k): nunca asoma ni deja hueco
  return (
    <svg width={size} height={size} viewBox="0 0 640 640" style={{ overflow: "visible" }}>
      <defs>
        <Grad id={`gA${id}`} /><Grad id={`gT${id}`} angle={-45} />
        <clipPath id={`cl${id}`}><circle cx={250} cy={250} r={ri} /></clipPath>
        <radialGradient id={`cr${id}`} cx="35%" cy="30%" r="75%">
          <stop offset="0%" stopColor="#fff" stopOpacity="0.16" /><stop offset="60%" stopColor="#fff" stopOpacity="0.03" /><stop offset="100%" stopColor="#fff" stopOpacity="0.1" />
        </radialGradient>
      </defs>
      <g transform="translate(250 250)">
        <circle r={r + 14 * k} fill="none" stroke={`url(#gA${id})`} strokeWidth={4 * k} />
        <g transform="rotate(45)"><rect x={r * 0.9} y={-38 * k} width={225 * k} height={76 * k} rx={34 * k} fill={AROS} stroke={`url(#gT${id})`} strokeWidth={6 * k} /></g>
      </g>
      <g clipPath={`url(#cl${id})`}>
        <g transform="translate(250 250)"><PlanetaReal r={ri} id={id} /></g>
        <circle cx={250} cy={250} r={ri} fill={`url(#cr${id})`} />
      </g>
      <g transform="translate(250 250)">
        <circle r={r} fill="none" stroke={AROS} strokeWidth={28 * k} />
        <circle r={r - 14 * k} fill="none" stroke="rgba(255,255,255,.3)" strokeWidth={3 * k} />
        <path d={`M ${-r * 0.62} ${-r * 0.42} A ${r * 0.75} ${r * 0.75} 0 0 1 ${-r * 0.18} ${-r * 0.72}`} stroke="#fff" strokeWidth={9 * k} strokeLinecap="round" fill="none" opacity={0.45} />
      </g>
    </svg>
  );
};

const Nombre = ({ escala = 1, c1 = "#ffffff", c2 = VERDE, alinear = "center" }) => (
  <div style={{ textAlign: alinear }}>
    <div style={{ fontFamily: tema.fuente.titulo, fontWeight: 800, fontSize: 150 * escala, lineHeight: 1.12, paddingTop: 6 * escala, color: c1 }}>ALUCÍNATE</div>
    <div style={{ fontFamily: tema.fuente.texto, fontWeight: 500, fontSize: 54 * escala, letterSpacing: 22 * escala, color: c2,
      paddingLeft: alinear === "center" ? 22 * escala : 4 * escala, marginTop: 2 * escala }}>CON EL MUNDO</div>
  </div>
);

// 1) Avatar 800×800, sin texto; margen para el recorte circular
export const Avatar = () => (
  <AbsoluteFill style={{ background: FONDO, alignItems: "center", justifyContent: "center" }}>
    <div style={{ transform: "translate(26px, 26px)" }}><IconoLupa size={600} id="av" /></div>
  </AbsoluteFill>
);

// Lupa sola, fondo transparente (marca de agua y otros usos)
export const IconoTransparente = ({ ancho }) => {
  const { width: w } = useVideoConfig();
  const width = ancho || w;
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
      <div style={{ transform: `translate(${width * 0.02}px, ${width * 0.02}px)` }}><IconoLupa size={width} id="it" /></div>
    </AbsoluteFill>
  );
};

// 2) Logo completo apilado: lupa encima + nombre centrado
export const LogoCompleto = ({ fondo = false }) => (
  <AbsoluteFill style={{ background: fondo ? FONDO : "transparent", alignItems: "center", justifyContent: "center", flexDirection: "column" }}>
    <div style={{ marginBottom: -24, transform: "translateX(20px)" }}><IconoLupa size={470} id="lc" /></div>
    <Nombre />
  </AbsoluteFill>
);

// 3) Logo horizontal claro (para fondos blancos): lupa pequeña a la izquierda, texto oscuro
export const LogoHorizontalClaro = () => (
  <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", flexDirection: "row", gap: 20 }}>
    <IconoLupa size={380} id="lh" />
    <Nombre alinear="left" c1="#0B1220" c2="#1F6B8A" escala={0.95} />
  </AbsoluteFill>
);

// 4) Banner 2560×1440 (zona segura centrada 1546×423)
export const BannerFinal = ({ guias = false }) => {
  const W = 2560, H = 1440, sw = 1546, sh = 423;
  const x0 = (W - sw) / 2, y0 = (H - sh) / 2;
  const R = 640;
  return (
    <AbsoluteFill style={{ background: `radial-gradient(ellipse at 45% 50%, #16304f 0%, #0f1c33 35%, ${FONDO} 70%)` }}>
      <svg width={W} height={H} style={{ position: "absolute" }}>
        <defs><Grad id="gAbn2" /></defs>
        {Array.from({ length: 180 }).map((_, i) => (
          <circle key={i} cx={(i * 733) % W} cy={(i * 397) % H} r={0.9 + (i % 4) * 0.6} fill="#cfe9ff" opacity={0.1 + (i % 6) / 22} />
        ))}
        <g transform={`translate(${W + 140} ${H / 2})`}>
          <circle r={R + 50} fill="url(#gAbn2)" opacity={0.1} />
          <PlanetaReal r={R} id="bn2" />
          <circle r={R} fill="none" stroke="rgba(255,255,255,.25)" strokeWidth={4} />
        </g>
        {guias && <rect x={x0} y={y0} width={sw} height={sh} fill="none" stroke="#f0f" strokeWidth={5} strokeDasharray="22 12" />}
      </svg>
      <div style={{ position: "absolute", left: x0, top: y0, width: sw, height: sh, display: "flex", alignItems: "center", justifyContent: "center", gap: 46 }}>
        <div style={{ flex: "none", marginTop: 24 }}><IconoLupa size={390} id="bn" /></div>
        <div>
          <Nombre escala={0.82} alinear="left" />
          <div style={{ fontFamily: tema.fuente.texto, fontWeight: 600, fontSize: 40, color: "#cfe0ea", marginTop: 16, marginLeft: 4 }}>Curiosidades del mundo que no te vas a creer</div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

// Hoja resumen con todo junto
const Caja = ({ titulo, w, h, bg = FONDO, children }) => (
  <div style={{ display: "flex", flexDirection: "column", gap: 10 }}>
    <div style={{ width: w, height: h, background: bg, borderRadius: 20, overflow: "hidden", position: "relative", boxShadow: "0 6px 24px rgba(0,0,0,.25)" }}>{children}</div>
    <div style={{ fontFamily: tema.fuente.texto, fontWeight: 700, fontSize: 26, color: "#22303d" }}>{titulo}</div>
  </div>
);
const Escalado = ({ w, h, s, children }) => (
  <div style={{ width: w, height: h, transform: `scale(${s})`, transformOrigin: "0 0", position: "absolute", left: 0, top: 0 }}>{children}</div>
);
const AJEDREZ = "repeating-conic-gradient(#e6e9ee 0% 25%, #ffffff 0% 50%) 50% / 40px 40px";

export const HojaResumen = () => (
  <AbsoluteFill style={{ background: "#f3f5f8", padding: 50, gap: 30, display: "flex", flexDirection: "column" }}>
    <div style={{ fontFamily: tema.fuente.titulo, fontWeight: 800, fontSize: 56, color: "#0B1220" }}>Alucínate con el mundo · identidad del canal</div>
    <div style={{ display: "flex", gap: 36 }}>
      <Caja titulo="avatar-800.png (recorte circular)" w={460} h={460} bg="transparent">
        <div style={{ width: 460, height: 460, borderRadius: 230, overflow: "hidden", position: "relative" }}><Escalado w={800} h={800} s={0.575}><Avatar /></Escalado></div>
      </Caja>
      <Caja titulo="logo-completo-oscuro.png" w={460} h={460}><Escalado w={1200} h={1200} s={0.3833}><LogoCompleto fondo /></Escalado></Caja>
      <Caja titulo="logo-completo.png (transparente)" w={460} h={460} bg="#3a5068"><Escalado w={1200} h={1200} s={0.3833}><LogoCompleto /></Escalado></Caja>
      <Caja titulo="marca-agua-150.png" w={460} h={460} bg={AJEDREZ}>
        <div style={{ position: "absolute", left: 155, top: 155, width: 150, height: 150 }}><Escalado w={150} h={150} s={1}><IconoTransparente ancho={150} /></Escalado></div>
      </Caja>
    </div>
    <div style={{ display: "flex", gap: 36, alignItems: "flex-start" }}>
      <Caja titulo="logo-horizontal-claro.png (transparente)" w={720} h={240} bg={AJEDREZ}><Escalado w={1800} h={600} s={0.4}><LogoHorizontalClaro /></Escalado></Caja>
      <Caja titulo="banner-2560x1440.jpg (rosa = zona segura)" w={1168} h={657}><Escalado w={2560} h={1440} s={0.45625}><BannerFinal guias /></Escalado></Caja>
    </div>
  </AbsoluteFill>
);
