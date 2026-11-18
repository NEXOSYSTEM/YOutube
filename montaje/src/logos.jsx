import React from "react";
import { AbsoluteFill, Sequence, Audio, staticFile, useCurrentFrame, useVideoConfig, spring, interpolate, Easing } from "remotion";
import { tema } from "./tema";

// Degradado del logo actual del canal (turquesa → verde → amarillo)
export const G = ["#4FD8E0", "#8EDB8A", "#F2D24B"];
const NAVY = "#0b2236";
const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" };

export const Grad = ({ id, angle = 0 }) => (
  <linearGradient id={id} x1="0" y1="0" x2="1" y2="1" gradientTransform={`rotate(${angle} .5 .5)`}>
    <stop offset="0%" stopColor={G[0]} /><stop offset="50%" stopColor={G[1]} /><stop offset="100%" stopColor={G[2]} />
  </linearGradient>
);

// Huella: 4 dedos + almohadilla. s = progreso de aparición (0..1) por pieza
export const Huella = ({ fill, p = [1, 1, 1, 1, 1], pad = null }) => {
  const toes = [[-118, -70, 40, 52, -20], [-45, -128, 44, 56, -6], [45, -128, 44, 56, 6], [118, -70, 40, 52, 20]];
  return (
    <g>
      {toes.map(([x, y, rx, ry, r], i) => (
        <ellipse key={i} cx={x} cy={y} rx={rx} ry={ry} fill={fill} transform={`rotate(${r} ${x} ${y}) translate(${x} ${y}) scale(${p[i]}) translate(${-x} ${-y})`} />
      ))}
      <g transform={`scale(${p[4]})`}>
        {pad || <path d="M0 -10 C 60 -10 112 40 112 92 C 112 140 70 150 40 140 C 18 132 10 126 0 126 C -10 126 -18 132 -40 140 C -70 150 -112 140 -112 92 C -112 40 -60 -10 0 -10 Z" fill={fill} />}
      </g>
    </g>
  );
};

// Globo terráqueo con meridianos que giran (rot en grados)
export const Globo = ({ r = 110, rot = 0, fill = "url(#gA)", line = "rgba(255,255,255,.75)", w = 5 }) => {
  const mer = [-60, -30, 0, 30, 60].map((d) => ((d + rot) % 180 + 180) % 180 - 90);
  return (
    <g>
      <circle r={r} fill={fill} />
      <clipPath id={`clipG${r}`}><circle r={r} /></clipPath>
      <g clipPath={`url(#clipG${r})`} fill="none" stroke={line} strokeWidth={w}>
        {mer.map((d, i) => <ellipse key={i} rx={Math.abs(Math.sin((d * Math.PI) / 180)) * r} ry={r} />)}
        {[-0.55, 0, 0.55].map((k, i) => <ellipse key={i} cy={k * r} rx={Math.sqrt(1 - k * k) * r} ry={r * 0.12} />)}
      </g>
      <circle r={r} fill="none" stroke={line} strokeWidth={w} />
    </g>
  );
};

const Marca = ({ y, size = 74, color = NAVY, op = 1, sp = 0, mundo = "url(#gT)" }) => (
  <text y={y} textAnchor="middle" style={{ fontFamily: tema.fuente.titulo, fontWeight: 800, fontSize: size, letterSpacing: sp }} opacity={op}>
    <tspan fill={color}>ALUCÍNATE CON EL </tspan><tspan fill={mundo}>MUNDO</tspan>
  </text>
);

// ---------- Las 4 propuestas (t = progreso 0..1 de la animación; t = 1 → logo final) ----------
export const LogoSVG = ({ v, t = 1, f = 999, fps = 30, dark = false }) => {
  const txt = dark ? "#ffffff" : NAVY;
  const s = (d) => spring({ frame: f - d, fps, config: { damping: 11, stiffness: 160 } });
  const fade = (d, len = 12) => interpolate(f, [d, d + len], [0, 1], clamp);
  const rot = f * 2;
  const W = 1000, H = 1000;
  let body = null;
  if (v === 1) {
    // 1 · Huella clásica renovada (fiel al logo actual)
    body = (
      <g>
        <g transform="translate(500 360) scale(1.25)"><Huella fill="url(#gA)" p={[s(0), s(4), s(8), s(12), s(16)]} /></g>
        <g opacity={fade(26)} transform={`translate(500 ${interpolate(fade(26), [0, 1], [700, 680])})`}><Marca y={0} size={70} color={txt} /></g>
        <rect x={500 - 260 * fade(34)} y={712} width={520 * fade(34)} height={8} rx={4} fill="url(#gT)" />
      </g>
    );
  } else if (v === 2) {
    // 2 · Huella-mundo: la almohadilla es un globo terráqueo
    body = (
      <g>
        <g transform="translate(500 380) scale(1.3)">
          <Huella fill="url(#gA)" p={[s(10), s(13), s(16), s(19), s(0)]} pad={<g transform="translate(0 70)"><Globo r={95} rot={rot} w={4} /></g>} />
        </g>
        <g opacity={fade(28)} transform="translate(500 0)"><Marca y={720} size={70} color={txt} /></g>
      </g>
    );
  } else if (v === 3) {
    // 3 · Ojo curioso: el iris es el mundo (curiosidades)
    const open = interpolate(f, [0, 14], [0.05, 1], { ...clamp, easing: Easing.out(Easing.back(1.6)) });
    body = (
      <g>
        <g transform={`translate(500 380) scale(1 ${open})`}>
          <path d="M-300 0 Q 0 -230 300 0 Q 0 230 -300 0 Z" fill={dark ? "#132c44" : "#fff"} stroke="url(#gA)" strokeWidth="22" strokeLinejoin="round" />
        </g>
        <g transform={`translate(500 380) scale(${s(10)})`}><Globo r={120} rot={rot} w={5} /><circle r={38} fill={NAVY} /><circle cx={-16} cy={-16} r={12} fill="#fff" /></g>
        <g opacity={fade(26)}>
          <text x={500} y={720} textAnchor="middle" style={{ fontFamily: tema.fuente.titulo, fontWeight: 800, fontSize: 130 }} fill="url(#gT)">¡ALUCÍNATE!</text>
          <text x={500} y={800} textAnchor="middle" style={{ fontFamily: tema.fuente.titulo, fontWeight: 800, fontSize: 58, letterSpacing: 14 }} fill={txt}>CON EL MUNDO</text>
        </g>
      </g>
    );
  } else if (v === 5) {
    // 5 · Exclamación-mundo: el punto de «¡!» es el planeta → «¡Alucina!»
    const drop = interpolate(f, [0, 16], [-500, 0], { ...clamp, easing: Easing.out(Easing.bounce) });
    body = (
      <g>
        <g transform={`translate(500 ${330 + drop * 0}) scale(${s(8)})`}>
          <path d="M-70 -260 L70 -260 L42 80 L-42 80 Z" fill="url(#gT)" />
        </g>
        <g transform={`translate(500 ${265 + 190 + drop})`}><Globo r={78} rot={rot} w={4} /></g>
        <g opacity={fade(22)} transform={`translate(500 ${interpolate(fade(22), [0, 1], [700, 680])})`}>
          <text y={0} textAnchor="middle" style={{ fontFamily: tema.fuente.titulo, fontWeight: 800, fontSize: 120 }} fill={txt}>ALUCÍNATE</text>
          <text y={78} textAnchor="middle" style={{ fontFamily: tema.fuente.titulo, fontWeight: 800, fontSize: 56, letterSpacing: 16 }} fill="url(#gT)">CON EL MUNDO</text>
        </g>
      </g>
    );
  } else if (v === 6) {
    // 6 · Lupa: descubrir curiosidades; la lente muestra el planeta
    const sw = interpolate(f, [0, 22], [-40, 0], { ...clamp, easing: Easing.out(Easing.back(1.4)) });
    body = (
      <g>
        <g transform={`translate(470 360) rotate(${sw}) scale(${s(0)})`}>
          <rect x={120} y={120} width={70} height={230} rx={30} transform="rotate(-45 120 120)" fill="url(#gT)" />
          <circle r={190} fill={dark ? "#132c44" : "#eaf7f6"} />
          <g transform={`scale(${1.05 + 0.04 * Math.sin(f / 8)})`}><Globo r={150} rot={rot} w={5} /></g>
          <circle r={190} fill="none" stroke="url(#gA)" strokeWidth={30} />
          <path d="M-120 -90 A 150 150 0 0 1 -40 -150" stroke="#fff" strokeWidth={16} strokeLinecap="round" fill="none" opacity={0.8} />
        </g>
        <g opacity={fade(24)} transform="translate(500 0)"><Marca y={760} size={72} color={txt} /></g>
      </g>
    );
  } else if (v === 7) {
    // 7 · ¡Wow! Planeta que «explota» de asombro (mente alucinada)
    const burst = interpolate(f, [6, 26], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
    const rays = Array.from({ length: 14 });
    body = (
      <g>
        <g transform="translate(500 360)">
          {rays.map((_, i) => {
            const a = (i / rays.length) * Math.PI * 2;
            const r0 = 170, r1 = 170 + (i % 2 ? 70 : 120) * burst;
            return <line key={i} x1={Math.cos(a) * r0} y1={Math.sin(a) * r0} x2={Math.cos(a) * r1} y2={Math.sin(a) * r1} stroke={i % 2 ? G[2] : G[0]} strokeWidth={20} strokeLinecap="round" />;
          })}
          <g transform={`scale(${s(0)})`}><Globo r={150} rot={rot} w={5} />
            <circle cx={-48} cy={-20} r={26} fill="#fff" /><circle cx={48} cy={-20} r={26} fill="#fff" />
            <circle cx={-44} cy={-16} r={12} fill={NAVY} /><circle cx={52} cy={-16} r={12} fill={NAVY} />
            <ellipse cx={0} cy={60} rx={30} ry={38 * s(10)} fill={NAVY} />
          </g>
        </g>
        <g opacity={fade(24)}>
          <text x={500} y={730} textAnchor="middle" style={{ fontFamily: tema.fuente.titulo, fontWeight: 800, fontSize: 130 }} fill="url(#gT)">¡ALUCÍNATE!</text>
          <text x={500} y={806} textAnchor="middle" style={{ fontFamily: tema.fuente.titulo, fontWeight: 800, fontSize: 56, letterSpacing: 14 }} fill={txt}>CON EL MUNDO</text>
        </g>
      </g>
    );
  } else if (v === 8) {
    // 8 · Monograma «A» con el planeta dentro + chispa (versátil para marca de agua)
    body = (
      <g>
        <g transform={`translate(500 400) scale(${s(0)})`}>
          <path d="M0 -300 L250 250 L150 250 L0 -90 L-150 250 L-250 250 Z" fill="url(#gT)" />
          <g transform="translate(0 110)"><Globo r={92} rot={rot} w={4} fill={dark ? "#132c44" : NAVY} line={G[1]} /></g>
          <g transform={`translate(205 -205) rotate(${f * 3}) scale(${s(14)})`}>
            <path d="M0 -60 L14 -14 L60 0 L14 14 L0 60 L-14 14 L-60 0 L-14 -14 Z" fill={G[2]} />
          </g>
        </g>
        <g opacity={fade(24)} transform="translate(500 0)"><Marca y={790} size={70} color={txt} /></g>
      </g>
    );
  } else {
    // 4 · Insignia circular para avatar: globo + huella + texto curvo
    body = (
      <g>
        <g transform={`translate(500 470) scale(${s(0)})`}>
          <circle r={360} fill={NAVY} />
          <circle r={344} fill="none" stroke="url(#gA)" strokeWidth={20} />
          <g transform="translate(0 10)"><Globo r={170} rot={rot} fill="url(#gA)" line="rgba(11,34,54,.55)" w={6} /></g>
          <g transform={`translate(0 40) scale(${0.42 * s(14)})`}><Huella fill="#ffffff" /></g>
          <defs>
            <path id="arcTop" d="M -262 0 A 262 262 0 0 1 262 0" />
            <path id="arcBot" d="M -282 0 A 282 282 0 0 0 282 0" />
          </defs>
          <text style={{ fontFamily: tema.fuente.titulo, fontWeight: 800, fontSize: 70, letterSpacing: 10 }} fill="#fff" opacity={fade(20)}>
            <textPath href="#arcTop" startOffset="50%" textAnchor="middle">¡ALUCÍNATE!</textPath>
          </text>
          <text style={{ fontFamily: tema.fuente.titulo, fontWeight: 800, fontSize: 50, letterSpacing: 12 }} fill={G[2]} opacity={fade(26)}>
            <textPath href="#arcBot" startOffset="50%" textAnchor="middle">CON EL MUNDO</textPath>
          </text>
        </g>
      </g>
    );
  }
  return (
    <svg viewBox={`0 0 ${W} ${H}`} width="100%" height="100%" style={{ overflow: "visible" }}>
      <defs><Grad id="gA" angle={0} /><Grad id="gT" angle={-45} /></defs>
      {body}
    </svg>
  );
};

const NOMBRES = { 1: "1 · Huella renovada", 2: "2 · Huella-mundo", 3: "3 · Ojo curioso", 4: "4 · Insignia (avatar)", 5: "5 · ¡Exclamación-mundo!", 6: "6 · Lupa del descubridor", 7: "7 · Planeta ¡WOW!", 8: "8 · Monograma A" };

// Hoja comparativa 2×2 (fondo claro arriba, oscuro abajo en cada celda)
export const HojaLogos = ({ vs = [1, 2, 3, 4] }) => (
  <AbsoluteFill style={{ background: "#eef2f5", display: "grid", gridTemplateColumns: "1fr 1fr", gridTemplateRows: "1fr 1fr", gap: 24, padding: 24 }}>
    {vs.map((v) => (
      <div key={v} style={{ background: "#fff", borderRadius: 24, position: "relative", overflow: "hidden", display: "flex" }}>
        <div style={{ flex: 1, padding: 30 }}><LogoSVG v={v} /></div>
        <div style={{ flex: 1, padding: 30, background: tema.color.fondo }}><LogoSVG v={v} dark /></div>
        <div style={{ position: "absolute", left: 24, top: 16, fontFamily: tema.fuente.titulo, fontWeight: 800, fontSize: 40, color: NAVY }}>{NOMBRES[v]}</div>
      </div>
    ))}
  </AbsoluteFill>
);

// Logo suelto (para PNG)
export const LogoSuelto = ({ v, dark }) => (
  <AbsoluteFill style={{ background: dark ? tema.color.fondo : "#ffffff", padding: 60 }}><LogoSVG v={v} dark={dark} /></AbsoluteFill>
);

// Intro animada del logo (≈3 s) para el arranque o el cierre de los vídeos
export const LogoAnimado = ({ v = 2 }) => {
  const f = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();
  const out = interpolate(f, [durationInFrames - 10, durationInFrames], [1, 0], clamp);
  const glow = interpolate(f, [20, 40], [0, 1], clamp);
  return (
    <AbsoluteFill style={{ background: `radial-gradient(circle at 50% 45%, ${tema.color.fondo2}, ${tema.color.fondo} 70%)`, opacity: out }}>
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
        <div style={{ width: 900, height: 900, filter: `drop-shadow(0 0 ${30 * glow}px rgba(79,216,224,.45))` }}><LogoSVG v={v} f={f} fps={fps} dark /></div>
      </AbsoluteFill>
      <Sequence from={0}><Audio src={staticFile("sfx/whoosh.wav")} volume={0.5} /></Sequence>
      <Sequence from={14}><Audio src={staticFile("sfx/pop.wav")} volume={0.4} /></Sequence>
      <Sequence from={26}><Audio src={staticFile("sfx/impacto.wav")} volume={0.35} /></Sequence>
    </AbsoluteFill>
  );
};

// ---------- Banner del canal (2560×1440; zona segura 1546×423 en el centro) ----------
export const Banner = ({ v = 2, guias = false }) => {
  const W = 2560, H = 1440, sw = 1546, sh = 423;
  const x0 = (W - sw) / 2, y0 = (H - sh) / 2;
  const stars = Array.from({ length: 140 }).map((_, i) => ({
    x: (i * 733) % W, y: (i * 397) % H, r: 1 + ((i * 7) % 5) * 0.6, o: 0.2 + ((i * 13) % 10) / 20,
  }));
  return (
    <AbsoluteFill style={{ background: `radial-gradient(ellipse at 50% 50%, ${tema.color.fondo2} 0%, ${tema.color.fondo} 65%)` }}>
      <svg width={W} height={H} style={{ position: "absolute" }}>
        <defs><Grad id="bgA" /></defs>
        {stars.map((s, i) => <circle key={i} cx={s.x} cy={s.y} r={s.r} fill="#bfefff" opacity={s.o} />)}
        <g transform={`translate(${W / 2 + 560} ${H / 2})`} opacity={0.18}><Globo r={520} rot={20} fill="url(#bgA)" w={6} /></g>
        <path d={`M0 ${H / 2 + 260} Q ${W / 2} ${H / 2 + 140} ${W} ${H / 2 + 260}`} stroke="url(#bgA)" strokeWidth={6} fill="none" opacity={0.6} />
        {guias && <rect x={x0} y={y0} width={sw} height={sh} fill="none" stroke="#f0f" strokeWidth={4} strokeDasharray="20 10" />}
      </svg>
      <div style={{ position: "absolute", left: x0, top: y0, width: sw, height: sh, display: "flex", alignItems: "center", gap: 50 }}>
        <div style={{ width: 340, height: 340, flex: "none" }}><LogoSVG v={v === 3 || v === 4 ? v : 4} dark /></div>
        <div>
          <div style={{ fontFamily: tema.fuente.titulo, fontWeight: 800, fontSize: 86, lineHeight: 0.95, color: "#fff", whiteSpace: "nowrap" }}>
            ¡ALUCÍNATE <span style={{ background: `linear-gradient(90deg, ${G[0]}, ${G[1]}, ${G[2]})`, WebkitBackgroundClip: "text", color: "transparent" }}>CON EL MUNDO!</span>
          </div>
          <div style={{ fontFamily: tema.fuente.texto, fontWeight: 700, fontSize: 38, color: "#cfe9ee", marginTop: 16 }}>
            Animales, lugares y curiosidades que no te vas a creer
          </div>
          <div style={{ display: "inline-block", marginTop: 22, padding: "8px 22px", borderRadius: 40, background: tema.color.peligro, fontFamily: tema.fuente.titulo, fontWeight: 800, fontSize: 32, color: "#fff" }}>
            VÍDEO NUEVO CADA MARTES · SHORTS JUE, SÁB Y DOM
          </div>
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ---------- Intro de los vídeos (≈4 s): logo animado + lema ----------
export const Intro = ({ v = 2 }) => {
  const f = useCurrentFrame();
  const lema = interpolate(f, [48, 62], [0, 1], clamp);
  return (
    <AbsoluteFill>
      <LogoAnimado v={v} />
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "flex-end", paddingBottom: 110, opacity: lema * interpolate(f, [110, 120], [1, 0], clamp) }}>
        <div style={{ fontFamily: tema.fuente.texto, fontWeight: 800, fontSize: 46, color: "#cfe9ee", letterSpacing: 6, transform: `translateY(${(1 - lema) * 20}px)` }}>
          CURIOSIDADES QUE NO TE VAS A CREER
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
