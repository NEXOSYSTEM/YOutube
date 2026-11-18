import React from "react";
import { AbsoluteFill, Img, Sequence, Audio, staticFile, useCurrentFrame, useVideoConfig, interpolate, spring, Easing, random } from "remotion";
import { tema } from "./tema";
import { Media, clamp, C } from "./base";

const Fondo = ({ children, style }) => (
  <AbsoluteFill style={{ background: `radial-gradient(ellipse at 50% 35%, ${C.fondo2} 0%, ${C.fondo} 70%)`, ...style }}>{children}</AbsoluteFill>
);

const Particulas = ({ n = 60 }) => {
  const f = useCurrentFrame();
  const { width, height } = useVideoConfig();
  return (
    <AbsoluteFill>
      {Array.from({ length: n }).map((_, i) => {
        const x = random(`x${i}`) * width;
        const sp = 0.3 + random(`v${i}`) * 0.9;
        const y = (random(`y${i}`) * height - f * sp + height * 2) % height;
        const r = 1.5 + random(`r${i}`) * 3.5;
        return <div key={i} style={{ position: "absolute", left: x, top: y, width: r, height: r, borderRadius: r, background: "rgba(180,230,255,.55)", filter: "blur(.6px)" }} />;
      })}
    </AbsoluteFill>
  );
};

const Pop = ({ at, s = "pop", v = 0.3 }) => (
  <Sequence from={Math.max(0, Math.round(at))} durationInFrames={60}><Audio src={staticFile(`sfx/${s}.wav`)} volume={v} /></Sequence>
);

// Título animado
export const Titulo = ({ sc }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const words = sc.title.split(" ");
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", inset: 0, filter: "brightness(.45) blur(2px)" }}><Media m={sc.bg} len={sc.len} kb={{ mode: "in", amt: 0.12 }} /></div>
      <Particulas />
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", padding: 120 }}>
        <div style={{ textAlign: "center", maxWidth: 1500 }}>
          {words.map((w, i) => {
            const sp = spring({ frame: f - 6 - i * 4, fps, config: { damping: 12 } });
            const hl = ["10", "VENENOSOS"].includes(w);
            return <span key={i} style={{ display: "inline-block", margin: "0 18px", ...tema.rotulo(hl ? 150 : 118, hl ? C.acento : "#fff"),
              transform: `translateY(${interpolate(sp, [0, 1], [80, 0])}px) scale(${interpolate(sp, [0, 1], [0.6, 1])})`, opacity: sp }}>{w}</span>;
          })}
        </div>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

// Pantalla dividida
export const Dividida = ({ sc, vertical }) => {
  const f = useCurrentFrame();
  const { width, height } = useVideoConfig();
  const p = interpolate(f, [0, 12], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  const half = width / 2;
  const lab = (t, side) => {
    const sp = interpolate(f, [10 + (side ? 6 : 0), 20 + (side ? 6 : 0)], [0, 1], clamp);
    return <div style={{ position: "absolute", bottom: 280, left: side ? half : 0, width: half, textAlign: "center", opacity: sp,
      transform: `translateY(${(1 - sp) * 30}px)` }}><span style={{ ...tema.rotulo(t.length < 4 ? 220 : 62, side ? C.acento : "#fff") }}>{t}</span></div>;
  };
  return (
    <AbsoluteFill style={{ background: C.fondo }}>
      <div style={{ position: "absolute", left: 0, top: 0, width: half, height, overflow: "hidden", transform: `translateX(${(p - 1) * half}px)` }}>
        <Media m={sc.left} len={sc.len} kb={{ mode: "in", amt: 0.1 }} />
      </div>
      <div style={{ position: "absolute", left: half, top: 0, width: half, height, overflow: "hidden", transform: `translateX(${(1 - p) * half}px)` }}>
        <Media m={sc.right} len={sc.len} kb={{ mode: "out", amt: 0.1 }} />
      </div>
      <div style={{ position: "absolute", left: half - 5, top: 0, width: 10, height, background: C.acento, transform: `scaleY(${p})`, boxShadow: "0 0 30px rgba(255,214,10,.7)" }} />
      {lab(sc.lt, 0)}{lab(sc.rt, 1)}
    </AbsoluteFill>
  );
};

// Contador de puesto «#10» que gira
export const Contador = ({ sc }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const sp = spring({ frame: f, fps, config: { damping: 13, stiffness: 120 } });
  return (
    <Fondo>
      <Particulas n={40} />
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", perspective: 1200 }}>
        <div style={{ ...tema.rotulo(420, C.acento), transform: `rotateY(${interpolate(sp, [0, 1], [540, 0])}deg) scale(${interpolate(sp, [0, 1], [0.3, 1])})`,
          textShadow: "0 0 60px rgba(255,214,10,.55)" }}>#{sc.value}</div>
      </AbsoluteFill>
      <Pop at={0} s="whoosh" v={0.6} /><Pop at={12} s="impacto" v={0.5} />
    </Fondo>
  );
};

// Mapa animado (equirectangular NASA Blue Marble)
export const Mapa = ({ sc }) => {
  const f = useCurrentFrame();
  const W = 1920, H = 960;
  const px = (lon) => ((lon + 180) / 360) * W;
  const py = (lat) => ((90 - lat) / 180) * H;
  const z = sc.zones.map(([lo0, lo1, la0, la1, label]) => ({ cx: px((lo0 + lo1) / 2), cy: py((la0 + la1) / 2), rx: ((lo1 - lo0) / 360) * W / 2, ry: ((la1 - la0) / 180) * H / 2, label }));
  const cx = sc.arrow ? (z[0].cx + z[z.length - 1].cx) / 2 : z.reduce((a, b) => a + b.cx, 0) / z.length;
  const cy = sc.arrow ? (z[0].cy + z[z.length - 1].cy) / 2 : z.reduce((a, b) => a + b.cy, 0) / z.length;
  const zoom = interpolate(f, [0, sc.len], [1.0, sc.arrow ? 1.15 : 1.6], { ...clamp, easing: Easing.inOut(Easing.sin) });
  const pulse = 0.6 + 0.4 * Math.sin(f / 6);
  const arrowP = interpolate(f, [25, 70], [0, 1], clamp);
  let path = null;
  if (sc.arrow && z.length > 1) {
    const a = z[0], b = z[1];
    path = `M ${a.cx} ${a.cy} Q ${(a.cx + b.cx) / 2} ${Math.min(a.cy, b.cy) - 260} ${b.cx} ${b.cy}`;
  }
  return (
    <AbsoluteFill style={{ background: "#020a12", alignItems: "center", justifyContent: "center", overflow: "hidden" }}>
      <div style={{ position: "relative", width: W, height: H, transform: `scale(${zoom})`, transformOrigin: `${cx}px ${cy}px` }}>
        {sc.map && <Img src={staticFile(sc.map.src)} style={{ width: W, height: H, filter: "brightness(.62) saturate(.8) contrast(1.1)" }} />}
        <svg width={W} height={H} style={{ position: "absolute", left: 0, top: 0 }}>
          {z.map((q, i) => {
            const s = interpolate(f, [6 + i * 22, 22 + i * 22], [0, 1], { ...clamp, easing: Easing.out(Easing.back(2)) });
            return (
              <g key={i} transform={`translate(${q.cx} ${q.cy}) scale(${s})`}>
                <ellipse rx={q.rx} ry={q.ry} fill={C.peligro} opacity={0.32 + 0.12 * pulse} />
                <ellipse rx={q.rx} ry={q.ry} fill="none" stroke={C.peligro} strokeWidth={4} opacity={0.9} />
                <text y={-q.ry - 16} textAnchor="middle" style={{ fontFamily: tema.fuente.titulo, fontWeight: 800, fontSize: 40, fill: "#fff", stroke: "#000", strokeWidth: 6, paintOrder: "stroke" }}>{q.label}</text>
              </g>
            );
          })}
          {path && <path d={path} fill="none" stroke={C.acento} strokeWidth={9} strokeLinecap="round" pathLength={1} strokeDasharray={1} strokeDashoffset={1 - arrowP} style={{ filter: "drop-shadow(0 0 10px rgba(255,214,10,.8))" }} />}
        </svg>
      </div>
      {sc.zones.map((_, i) => <Pop key={i} at={6 + i * 22} v={0.25} />)}
      {path && <Pop at={25} s="riser" v={0.35} />}
    </AbsoluteFill>
  );
};

// Comparativa de tamaño: blenio frente a un dedo
const PezSilueta = ({ w = 300, color = C.agua, boca = 0 }) => (
  <svg width={w} height={w * 0.45} viewBox="0 0 200 90">
    <path d={`M10 45 Q60 ${5 - boca * 10} 130 25 L190 5 L175 45 L190 85 L130 65 Q60 ${85 + boca * 10} 10 45 Z`} fill={color} />
    <circle cx="35" cy="38" r="6" fill="#000" /><circle cx="37" cy="36" r="2" fill="#fff" />
  </svg>
);

export const Tamano = ({ sc }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const a = spring({ frame: f - 4, fps, config: { damping: 14 } });
  const b = spring({ frame: f - 18, fps, config: { damping: 14 } });
  return (
    <Fondo>
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", gap: 80, flexDirection: "row", paddingTop: 80 }}>
        <div style={{ transform: `translateY(${(1 - a) * 300}px)`, textAlign: "center" }}>
          <svg width="230" height="620" viewBox="0 0 230 620">
            <rect x="20" y="20" width="190" height="640" rx="95" fill="#e8b897" stroke="#000" strokeWidth="8" />
            <rect x="52" y="44" width="126" height="150" rx="56" fill="#f6dccb" stroke="#b58b70" strokeWidth="5" />
            <path d="M40 330 Q115 350 190 330 M40 460 Q115 480 190 460" stroke="#b58b70" strokeWidth="6" fill="none" />
          </svg>
          <div style={{ ...tema.rotulo(54) }}>Tu dedo ≈ 8 cm</div>
        </div>
        <div style={{ transform: `scale(${b})`, textAlign: "center" }}>
          <PezSilueta w={260} color={C.acento} />
          <div style={{ ...tema.rotulo(54, C.acento) }}>Blenio ≈ 5–10 cm</div>
        </div>
      </AbsoluteFill>
      <Pop at={4} v={0.25} /><Pop at={18} v={0.3} />
    </Fondo>
  );
};

// Animación: un pez grande se traga al blenio, se marea y lo escupe
export const Traga = ({ sc }) => {
  const f = useCurrentFrame();
  const L = sc.len;
  const t = f / L;
  const bigX = interpolate(t, [0, 0.3, 0.75, 1], [-700, 330, 330, 260], clamp);
  const boca = interpolate(t, [0.18, 0.28, 0.32, 0.62, 0.7], [0, 1, 0, 0, 1], clamp);
  const smallVis = t < 0.3 || t > 0.68;
  const smallX = t > 0.68 ? interpolate(t, [0.68, 1], [900, 1500], clamp) : 960;
  const dizzy = t > 0.38 && t < 0.7;
  const wob = dizzy ? Math.sin(f / 3) * 8 : 0;
  return (
    <Fondo>
      <Particulas n={30} />
      <div style={{ position: "absolute", left: bigX, top: 330, transform: `rotate(${wob}deg)`, transformOrigin: "40% 50%" }}>
        <svg width="760" height="420" viewBox="0 0 200 110" style={{ transform: "scaleX(-1)" }}>
          <path d={`M10 55 Q60 ${0 - boca * 20} 130 30 L195 5 L178 55 L195 105 L130 80 Q60 ${110 + boca * 20} 10 55 Z`} fill="#3d6e8f" stroke="#0a1a28" strokeWidth="3" />
          <circle cx="40" cy="42" r="8" fill="#fff" /><circle cx="40" cy="42" r="4" fill="#000" />
        </svg>
        {dizzy && <svg width="200" height="200" viewBox="-100 -100 200 200" style={{ position: "absolute", left: 560, top: -90, transform: `rotate(${f * 12}deg)` }}>
          <path d="M0 0 m-60 0 a60 60 0 1 1 120 0 a45 45 0 1 1 -90 0 a30 30 0 1 1 60 0 a15 15 0 1 1 -30 0" fill="none" stroke={C.acento} strokeWidth="8" />
        </svg>}
      </div>
      {smallVis && <div style={{ position: "absolute", left: smallX, top: 470 }}><PezSilueta w={170} color={C.acento} /></div>}
      <Pop at={L * 0.28} s="impacto" v={0.35} /><Pop at={L * 0.68} s="whoosh-corto" v={0.5} />
    </Fondo>
  );
};

// Contador de años +400
export const Anos = ({ sc }) => {
  const f = useCurrentFrame();
  const v = Math.round(interpolate(f, [8, 70], [0, sc.value], { ...clamp, easing: Easing.out(Easing.cubic) }));
  const done = f > 70;
  const { fps } = useVideoConfig();
  const sp = spring({ frame: f - 70, fps, config: { damping: 8 } });
  return (
    <AbsoluteFill>
      <div style={{ position: "absolute", inset: 0, filter: "brightness(.35) blur(3px)" }}><Media m={sc.bg} len={sc.len} kb={{ mode: "in", amt: 0.1 }} /></div>
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", flexDirection: "column" }}>
        <div style={{ ...tema.rotulo(330, C.acento), transform: `scale(${done ? 1 + 0.12 * (1 - sp) : 1})`, fontVariantNumeric: "tabular-nums" }}>{done ? "+" : ""}{v}</div>
        <div style={{ ...tema.rotulo(110) }}>AÑOS</div>
      </AbsoluteFill>
      <Pop at={6} s="riser" v={0.4} /><Pop at={70} s="impacto" v={0.55} />
    </AbsoluteFill>
  );
};

// Primeros auxilios en 3 pasos
export const Pasos = ({ sc }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const n = sc.steps.length;
  return (
    <Fondo>
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center", flexDirection: "column", gap: 34, paddingBottom: 60 }}>
        <div style={{ ...tema.rotulo(70, C.acento), marginBottom: 10 }}>SI TE PICA:</div>
        {sc.steps.map((s, i) => {
          const at = 10 + (i * (sc.len - 30)) / n;
          const sp = spring({ frame: f - at, fps, config: { damping: 14 } });
          return (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 30, width: 1250, background: C.tarjeta, borderRadius: 22, padding: "22px 34px",
              borderLeft: `12px solid ${i === n - 1 ? C.peligro : C.agua}`, transform: `translateX(${(1 - sp) * -1600}px)`, opacity: sp }}>
              <div style={{ ...tema.rotulo(88, i === n - 1 ? C.peligro : C.acento), width: 90, textAlign: "center" }}>{i + 1}</div>
              <div style={{ fontFamily: tema.fuente.texto, fontWeight: 800, fontSize: 54, color: "#fff" }}>{s}</div>
            </div>
          );
        })}
      </AbsoluteFill>
      {sc.steps.map((_, i) => <Pop key={i} at={10 + (i * (sc.len - 30)) / n} v={0.35} />)}
    </Fondo>
  );
};

// Paso único (Shorts)
export const Paso = ({ sc }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const sp = spring({ frame: f - 2, fps, config: { damping: 12 } });
  return (
    <AbsoluteFill>
      {sc.bg ? <div style={{ position: "absolute", inset: 0, filter: "brightness(.5)" }}><Media m={sc.bg} len={sc.len} kb={{ mode: "in", amt: 0.12 }} vertical /></div> : <Fondo />}
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "flex-start", paddingTop: 470 }}>
        <div style={{ width: 300, height: 300, borderRadius: 150, background: sc.n === 3 ? C.peligro : C.acento, display: "flex", alignItems: "center", justifyContent: "center",
          transform: `scale(${sp})`, boxShadow: "0 0 60px rgba(0,0,0,.6)", border: "10px solid #000" }}>
          {sc.n === 3 ? <svg width="170" height="170" viewBox="0 0 10 10"><path d="M3.5 0h3v3.5H10v3H6.5V10h-3V6.5H0v-3h3.5z" fill="#fff" /></svg>
            : <div style={{ ...tema.rotulo(200, "#000"), WebkitTextStroke: "0", textShadow: "none" }}>{sc.n}</div>}
        </div>
      </AbsoluteFill>
      <Pop at={2} v={0.35} />
    </AbsoluteFill>
  );
};

// Esquema del pez globo: hígado, ovarios y piel
export const Organos = ({ sc }) => {
  const f = useCurrentFrame();
  const parts = [
    { k: "Hígado", at: 12, el: <path d="M330 250 Q400 200 470 240 Q480 300 400 320 Q330 310 330 250Z" /> , lx: 400, ly: 180 },
    { k: "Ovarios", at: 40, el: <ellipse cx="560" cy="320" rx="70" ry="40" />, lx: 560, ly: 410 },
    { k: "Piel", at: 68, el: null, lx: 840, ly: 150 },
  ];
  const on = (at) => interpolate(f, [at, at + 10], [0, 1], clamp);
  const pulse = 0.7 + 0.3 * Math.sin(f / 5);
  return (
    <Fondo>
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
        <svg width="1300" height="700" viewBox="0 0 1000 540">
          <g>
            <ellipse cx="480" cy="280" rx="330" ry="200" fill="#1f4a66" stroke={on(68) ? C.peligro : "#6fa3c4"} strokeWidth={on(68) ? 10 * pulse + 4 : 6} />
            {Array.from({ length: 26 }).map((_, i) => { const a = (i / 26) * Math.PI * 2; return <line key={i} x1={480 + Math.cos(a) * 330} y1={280 + Math.sin(a) * 200} x2={480 + Math.cos(a) * 360} y2={280 + Math.sin(a) * 222} stroke="#6fa3c4" strokeWidth="5" />; })}
            <path d="M800 280 L940 170 L920 280 L940 390 Z" fill="#1f4a66" stroke="#6fa3c4" strokeWidth="6" />
            <circle cx="250" cy="220" r="34" fill="#fff" /><circle cx="244" cy="220" r="17" fill="#000" />
            <path d="M150 290 Q170 310 150 330" stroke="#6fa3c4" strokeWidth="8" fill="none" />
          </g>
          {parts.map((p, i) => (
            <g key={i} opacity={on(p.at)}>
              {p.el && React.cloneElement(p.el, { fill: C.peligro, opacity: 0.55 + 0.35 * pulse, stroke: "#fff", strokeWidth: 3 })}
              <text x={p.lx} y={p.ly} textAnchor="middle" style={{ fontFamily: tema.fuente.titulo, fontWeight: 800, fontSize: 46, fill: "#fff", stroke: "#000", strokeWidth: 8, paintOrder: "stroke" }}>{p.k}</text>
            </g>
          ))}
        </svg>
      </AbsoluteFill>
      {parts.map((p, i) => <Pop key={i} at={p.at} v={0.3} />)}
    </Fondo>
  );
};

// Pantalla negra con texto grande
export const Negro = ({ sc }) => {
  const f = useCurrentFrame();
  const shake = f < 12 ? (random(`n${f}`) - 0.5) * 30 * (1 - f / 12) : 0;
  const s = interpolate(f, [0, 5], [1.6, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  return (
    <AbsoluteFill style={{ background: "#000", alignItems: "center", justifyContent: "center" }}>
      <div style={{ ...tema.rotulo(170, C.peligro), transform: `translate(${shake}px,${shake / 2}px) scale(${s})`, textAlign: "center", textShadow: "0 0 50px rgba(230,57,70,.6)" }}>{sc.text}</div>
    </AbsoluteFill>
  );
};

// Esquema del pez piedra con 13 espinas y un pie que baja
export const Espinas = ({ sc, vertical }) => {
  const f = useCurrentFrame();
  const L = sc.len;
  const lit = Math.floor(interpolate(f, [8, L * 0.6], [0, 13], clamp));
  const foot = interpolate(f, [L * 0.55, L * 0.85], [-520, -40], { ...clamp, easing: Easing.in(Easing.quad) });
  const spines = Array.from({ length: 13 }).map((_, i) => {
    const x = 210 + i * 46;
    const y = 250 - Math.sin((i / 12) * Math.PI) * 70;
    return { x, y };
  });
  return (
    <Fondo>
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
        <svg width={vertical ? 1050 : 1400} height={vertical ? 760 : 820} viewBox="0 -260 1000 760" style={{ overflow: "visible" }}>
          <g transform={`translate(560 ${foot})`}>
            <path d="M-90 -400 L-90 -60 Q-100 40 0 50 L170 50 Q220 40 210 -10 Q200 -50 120 -60 L80 -60 L80 -400 Z" fill="#e8b897" stroke="#000" strokeWidth="8" />
          </g>
          <path d="M120 360 Q100 240 220 220 Q500 140 800 230 Q900 270 880 360 Q860 430 500 440 Q170 440 120 360Z" fill="#6b5a46" stroke="#2b2219" strokeWidth="8" />
          {Array.from({ length: 22 }).map((_, i) => <circle key={i} cx={170 + random(`a${i}`) * 680} cy={260 + random(`b${i}`) * 150} r={8 + random(`c${i}`) * 16} fill="#857158" />)}
          <ellipse cx="190" cy="300" rx="18" ry="12" fill="#000" />
          {spines.map((p, i) => (
            <path key={i} d={`M${p.x - 14} ${p.y + 10} L${p.x} ${p.y - 70} L${p.x + 14} ${p.y + 10} Z`} fill={i < lit ? C.peligro : "#a89276"} stroke="#000" strokeWidth="4"
              style={{ filter: i < lit ? "drop-shadow(0 0 10px rgba(230,57,70,.95))" : "none" }} />
          ))}
          <text x="500" y="-170" textAnchor="middle" style={{ fontFamily: tema.fuente.titulo, fontWeight: 800, fontSize: 130, fill: C.acento, stroke: "#000", strokeWidth: 12, paintOrder: "stroke" }}>{lit}</text>
        </svg>
      </AbsoluteFill>
      {Array.from({ length: 13 }).map((_, i) => <Pop key={i} at={8 + (i * (L * 0.6 - 8)) / 13} s="tick" v={0.35} />)}
      <Pop at={L * 0.85} s="impacto" v={0.5} />
    </Fondo>
  );
};

// Calendario: dolor durante semanas
export const Calendario = ({ sc }) => {
  const f = useCurrentFrame();
  const days = 28;
  const n = Math.floor(interpolate(f, [6, sc.len - 20], [0, days], clamp));
  return (
    <Fondo>
      <AbsoluteFill style={{ alignItems: "center", justifyContent: "flex-start", paddingTop: 420 }}>
        <div style={{ background: "#fff", borderRadius: 30, width: 860, padding: 30, boxShadow: "0 30px 80px rgba(0,0,0,.6)" }}>
          <div style={{ background: C.peligro, borderRadius: 18, padding: 18, textAlign: "center", fontFamily: tema.fuente.titulo, fontWeight: 800, fontSize: 64, color: "#fff" }}>
            SEMANA {Math.min(4, Math.floor(n / 7) + 1)}
          </div>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(7, 1fr)", gap: 12, marginTop: 24 }}>
            {Array.from({ length: days }).map((_, i) => (
              <div key={i} style={{ height: 96, borderRadius: 12, background: "#eef2f6", position: "relative", fontFamily: tema.fuente.texto, fontWeight: 700, fontSize: 34, color: "#223", display: "flex", alignItems: "center", justifyContent: "center" }}>
                {i + 1}
                {i < n && <svg width="80" height="80" viewBox="0 0 10 10" style={{ position: "absolute" }}><path d="M1 1 L9 9 M9 1 L1 9" stroke={C.peligro} strokeWidth="1.4" strokeLinecap="round" /></svg>}
              </div>
            ))}
          </div>
        </div>
      </AbsoluteFill>
    </Fondo>
  );
};

// Montaje rápido de los 10 peces
export const Repaso = ({ sc }) => {
  const f = useCurrentFrame();
  const L = sc.montage.length;
  const each = Math.floor(sc.len / L);
  return (
    <AbsoluteFill style={{ background: "#000" }}>
      {sc.montage.map((m, i) => (
        <Sequence key={i} from={i * each} durationInFrames={i === L - 1 ? sc.len - i * each : each}>
          <Media m={m} len={each} kb={{ mode: i % 2 ? "in" : "out", amt: 0.18 }} />
          <AbsoluteFill style={{ padding: 70 }}><div style={{ ...tema.rotulo(150, C.acento) }}>#{10 - i}</div></AbsoluteFill>
          <Pop at={0} s="whoosh-corto" v={0.3} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};

// Pantalla final (zonas para los elementos de YouTube)
export const Final = ({ sc }) => {
  const f = useCurrentFrame();
  const op = interpolate(f, [0, 15], [0, 1], clamp);
  return (
    <Fondo style={{ opacity: op }}>
      <Particulas n={50} />
      <AbsoluteFill style={{ alignItems: "center", paddingTop: 110 }}>
        <div style={{ ...tema.rotulo(84) }}>¿Te atreves con el siguiente?</div>
      </AbsoluteFill>
      <div style={{ position: "absolute", left: 180, top: 330, width: 900, height: 506, borderRadius: 20, border: `6px solid ${C.acento}`, background: "rgba(255,255,255,.04)" }} />
      <div style={{ position: "absolute", left: 1270, top: 390, width: 400, height: 400, borderRadius: 200, border: `6px solid ${C.peligro}`, background: "rgba(255,255,255,.04)" }} />
      <div style={{ position: "absolute", left: 1270, top: 820, width: 400, textAlign: "center", ...tema.rotulo(54) }}>SUSCRÍBETE</div>
    </Fondo>
  );
};

// Créditos finales (3 s, letra pequeña)
export const Creditos = ({ lines }) => (
  <AbsoluteFill style={{ background: C.fondo, padding: "60px 80px" }}>
    <div style={{ fontFamily: tema.fuente.titulo, fontWeight: 800, fontSize: 40, color: C.acento, marginBottom: 18 }}>Créditos de imagen y vídeo (licencias libres · lista completa en la descripción)</div>
    <div style={{ columnCount: 4, columnGap: 40, fontFamily: tema.fuente.texto, fontSize: 17, lineHeight: 1.35, color: "#cfd8e3" }}>
      {lines.map((l, i) => <div key={i} style={{ breakInside: "avoid" }}>{l}</div>)}
    </div>
    <div style={{ position: "absolute", bottom: 40, left: 80, fontFamily: tema.fuente.texto, fontSize: 18, color: "#8aa0b5" }}>Narración: voz sintética (Qwen3-TTS). Efectos de sonido: propios. Alucínate con el mundo · 2026</div>
  </AbsoluteFill>
);
