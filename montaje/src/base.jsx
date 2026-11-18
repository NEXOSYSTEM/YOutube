import React from "react";
import {
  AbsoluteFill, Img, OffthreadVideo, Loop, Sequence, Audio, staticFile, useCurrentFrame,
  useVideoConfig, interpolate, spring, Easing, random,
} from "remotion";
import { tema } from "./tema";

const C = tema.color;
export const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" };

// ---------- Medio con efecto Ken Burns (imagen o vídeo) ----------
export const Media = ({ m, len, kb = { mode: "in", amt: 0.1 }, style = {}, vertical = false }) => {
  const f = useCurrentFrame();
  const { width: W, height: H, fps: FPSv } = useVideoConfig();
  if (!m) return <AbsoluteFill style={{ background: `radial-gradient(circle at 50% 40%, ${C.fondo2}, ${C.fondo})` }} />;
  const p = interpolate(f, [0, Math.max(1, len)], [0, 1], clamp);
  const e = Easing.inOut(Easing.sin)(p);
  const a = kb.amt;
  let s = 1.06, tx = 0, ty = 0;
  if (kb.mode === "in") s = 1.04 + a * e;
  else if (kb.mode === "out") s = 1.04 + a * (1 - e);
  else {
    s = 1.06 + a * 0.6;
    const d = (a * 0.6 * 100) / 2.4;
    if (kb.mode === "left") tx = interpolate(e, [0, 1], [d, -d]);
    if (kb.mode === "right") tx = interpolate(e, [0, 1], [-d, d]);
    if (kb.mode === "up") ty = interpolate(e, [0, 1], [d * 0.6, -d * 0.6]);
  }
  const aspect = m.w && m.h ? m.w / m.h : 1.6;
  // Regla del canal: el animal se ve ENTERO (cabeza a cola): encuadre «contain» + fondo con la misma imagen desenfocada
  if (m.entero) {
    const z = 1 + Math.min(a, 0.08) * (kb.mode === "out" ? 1 - e : e);
    const src = staticFile(m.src);
    const encaja = Math.abs(aspect - W / H) < 0.04;
    const fg = { width: "100%", height: "100%", objectFit: "contain", transform: `scale(${z})` };
    const bg = { width: "100%", height: "100%", objectFit: "cover", filter: "blur(36px) brightness(0.42) saturate(1.1)", transform: "scale(1.15)" };
    if (m.video) {
      return (
        <AbsoluteFill style={{ overflow: "hidden", background: C.fondo }}>
          {!encaja && <AbsoluteFill><OffthreadVideo src={src} muted startFrom={Math.round((m.start || 0) * FPSv)} style={bg} /></AbsoluteFill>}
          <AbsoluteFill><OffthreadVideo src={src} muted startFrom={Math.round((m.start || 0) * FPSv)} style={fg} /></AbsoluteFill>
        </AbsoluteFill>
      );
    }
    return (
      <AbsoluteFill style={{ overflow: "hidden", background: C.fondo }}>
        {!encaja && <AbsoluteFill><Img src={m.bg ? staticFile(m.bg) : src} style={m.bg ? { width: "100%", height: "100%", objectFit: "cover", transform: "scale(1.1)" } : bg} /></AbsoluteFill>}
        <AbsoluteFill><Img src={src} style={fg} /></AbsoluteFill>
      </AbsoluteFill>
    );
  }
  const portraitInLandscape = !vertical && aspect < 1.15;
  const fill = { width: "100%", height: "100%", objectFit: "cover" };
  const tr = { transform: `scale(${s}) translate(${tx}%, ${ty}%)`, ...fill, ...style };
  const src = staticFile(m.src);
  let el;
  if (m.video) {
    const vf = Math.max(FPSv, Math.floor(((m.dur || 4) - (m.start || 0)) * FPSv) - 2);
    const rate = vf < len ? Math.max(0.6, vf / len) : 1;
    const loopLen = Math.floor(vf / rate);
    const v = <OffthreadVideo src={src} muted playbackRate={rate} startFrom={Math.round((m.start || 0) * FPSv)} style={tr} />;
    el = loopLen < len ? <Loop durationInFrames={loopLen}>{v}</Loop> : v;
  } else {
    el = <Img src={src} style={tr} />;
  }
  if (portraitInLandscape && !m.video) {
    return (
      <AbsoluteFill style={{ overflow: "hidden", background: C.fondo }}>
        <Img src={src} style={{ ...fill, filter: "blur(40px) brightness(0.55)", transform: "scale(1.2)" }} />
        <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
          <Img src={src} style={{ height: "100%", objectFit: "contain", transform: `scale(${s})`, boxShadow: "0 0 80px rgba(0,0,0,.6)" }} />
        </AbsoluteFill>
      </AbsoluteFill>
    );
  }
  return <AbsoluteFill style={{ overflow: "hidden", background: C.fondo }}>{el}</AbsoluteFill>;
};

// ---------- Transición de entrada de cada plano ----------
export const Entrada = ({ tipo, children }) => {
  const f = useCurrentFrame();
  const { fps, width } = useVideoConfig();
  let style = {};
  let flash = 0;
  if (tipo === "punch") {
    const sp = spring({ frame: f, fps, config: { damping: 14, stiffness: 180 } });
    style = { transform: `scale(${interpolate(sp, [0, 1], [1.22, 1])})`, filter: `blur(${interpolate(f, [0, 6], [8, 0], clamp)}px)` };
  } else if (tipo === "slide") {
    const x = interpolate(f, [0, 9], [width, 0], { ...clamp, easing: Easing.out(Easing.cubic) });
    style = { transform: `translateX(${x}px)` };
  } else if (tipo === "whip") {
    const x = interpolate(f, [0, 7], [-width, 0], { ...clamp, easing: Easing.out(Easing.exp) });
    style = { transform: `translateX(${x}px)`, filter: `blur(${interpolate(f, [0, 7], [18, 0], clamp)}px)` };
  } else if (tipo === "flash") {
    flash = interpolate(f, [0, 6], [0.85, 0], clamp);
  }
  return (
    <AbsoluteFill style={style}>
      {children}
      {flash > 0 && <AbsoluteFill style={{ background: "#fff", opacity: flash }} />}
    </AbsoluteFill>
  );
};

// ---------- Acabado: viñeta + grano + corrección de color ----------
export const Acabado = ({ fuerte = false, sinVineta = false }) => {
  const f = useCurrentFrame();
  const seed = Math.floor(f / 2) % 6;
  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      {!sinVineta && <AbsoluteFill style={{ background: `radial-gradient(ellipse at 50% 50%, rgba(0,0,0,0) ${fuerte ? 30 : 52}%, rgba(0,0,0,${fuerte ? 0.85 : 0.55}) 100%)` }} />}
      {/* grano prerenderizado (6 fotogramas en bucle): mucho más rápido que generar ruido SVG en cada fotograma */}
      <Img src={staticFile(`grano/g${seed}.png`)} style={{ position: "absolute", width: "100%", height: "100%", objectFit: "cover", opacity: 0.09, mixBlendMode: "overlay" }} />
    </AbsoluteFill>
  );
};

// ---------- Rótulo clave (blanco con borde negro) ----------
export const Rotulo = ({ text, len, vertical = false, y }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const sp = spring({ frame: f, fps, config: { damping: 12, stiffness: 200 } });
  const out = interpolate(f, [len - 8, len], [1, 0], clamp);
  const px = vertical ? 84 : 92;
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "flex-start", paddingTop: y ?? (vertical ? 330 : 120) }}>
      <div style={{ ...tema.rotulo(px), maxWidth: vertical ? 960 : 1500, textAlign: "center",
        transform: `scale(${interpolate(sp, [0, 1], [0.4, 1])}) rotate(${interpolate(sp, [0, 1], [-4, 0])}deg)`, opacity: out }}>
        {text}
      </div>
    </AbsoluteFill>
  );
};

// ---------- Rótulo de puesto «#N NOMBRE» con golpe de zoom ----------
export const Puesto = ({ text }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const m = text.match(/^(#\d+)\s+(.*)$/) || [null, text, ""];
  const sp = spring({ frame: f - 4, fps, config: { damping: 10, stiffness: 220, mass: 0.8 } });
  const shake = f < 14 ? (random(`s${f}`) - 0.5) * 14 * (1 - f / 14) : 0;
  const out = interpolate(f, [52, 62], [1, 0], clamp);
  const bar = interpolate(f, [6, 16], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  return (
    <AbsoluteFill style={{ padding: "70px 90px", opacity: out }}>
      <div style={{ transform: `translate(${shake}px, ${shake * 0.6}px) scale(${interpolate(sp, [0, 1], [2.6, 1])})`, transformOrigin: "0% 0%", display: "flex", alignItems: "flex-end", gap: 26 }}>
        <div style={{ ...tema.rotulo(190, C.acento), lineHeight: 0.85 }}>{m[1]}</div>
        <div style={{ paddingBottom: 14 }}>
          <div style={{ ...tema.rotulo(78) }}>{m[2]}</div>
          <div style={{ height: 10, width: `${bar * 100}%`, background: C.peligro, marginTop: 8, borderRadius: 5 }} />
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ---------- Ficha del animal (abajo a la derecha) ----------
export const Ficha = ({ ficha, len = 150 }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const sp = spring({ frame: f, fps, config: { damping: 16 } });
  const out = interpolate(f, [len - 10, len], [0, 1], clamp);
  const x = interpolate(sp, [0, 1], [560, 0]) + out * 560;
  return (
    <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "flex-end", padding: "0 70px 175px 0" }}>
      <div style={{ transform: `translateX(${x}px)`, background: C.tarjeta, borderLeft: `10px solid ${C.peligro}`, borderRadius: 18,
        padding: "22px 34px 24px", minWidth: 430, boxShadow: "0 18px 50px rgba(0,0,0,.5)", backdropFilter: "blur(6px)" }}>
        <div style={{ fontFamily: tema.fuente.titulo, fontWeight: 800, fontSize: 46, color: C.texto, lineHeight: 1.05 }}>{ficha.comun}</div>
        <div style={{ fontFamily: tema.fuente.texto, fontStyle: "italic", fontSize: 32, color: C.agua, marginTop: 4 }}>{ficha.cient}</div>
        <div style={{ display: "flex", alignItems: "center", gap: 10, marginTop: 14 }}>
          <span style={{ fontFamily: tema.fuente.texto, fontSize: 22, color: "#cfd8e3", fontWeight: 700, letterSpacing: 2, marginRight: 8 }}>PELIGRO</span>
          {[1, 2, 3, 4, 5].map((i) => {
            const on = i <= ficha.skulls;
            const s = spring({ frame: f - 10 - i * 5, fps, config: { damping: 9 } });
            return <span key={i} style={{ fontSize: 40, color: on ? C.peligro : "#8899aa", transform: `scale(${on ? s : 1})`, opacity: on ? 1 : 0.22, filter: on ? "drop-shadow(0 0 8px rgba(230,57,70,.9))" : "grayscale(1)" }}>☠</span>;
          })}
          {ficha.nota && <span style={{ fontFamily: tema.fuente.texto, fontSize: 22, color: C.acento, marginLeft: 10, fontWeight: 700 }}>({ficha.nota})</span>}
        </div>
      </div>
    </AbsoluteFill>
  );
};

// ---------- Círculo rojo y contorno de revelación ----------
export const Circulo = ({ start, len, reveal = false }) => {
  const f = useCurrentFrame() - start;
  if (f < 0) return null;
  const p = interpolate(f, [0, 14], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
  const pulse = 1 + Math.sin(f / 5) * 0.015;
  const per = 2 * Math.PI * 300;
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
      <svg width="900" height="700" viewBox="-450 -350 900 700" style={{ transform: `scale(${pulse})`, overflow: "visible" }}>
        <ellipse rx={reveal ? 400 : 300} ry={reveal ? 260 : 220} fill="none" stroke={C.peligro} strokeWidth={reveal ? 10 : 14}
          strokeDasharray={reveal ? "34 18" : per} strokeDashoffset={reveal ? -f * 2 : per * (1 - p)} opacity={reveal ? p : 1}
          style={{ filter: "drop-shadow(0 0 14px rgba(230,57,70,.9))" }} />
      </svg>
    </AbsoluteFill>
  );
};

// ---------- Subtítulos del vídeo largo (frase de 1–2 líneas, abajo) ----------
export const SubtitulosLargo = ({ captions }) => {
  const f = useCurrentFrame();
  const c = captions.find((x) => f >= x.s && f < x.e + 4);
  if (!c) return null;
  const k = f - c.s;
  const op = interpolate(k, [0, 3], [0, 1], clamp);
  return (
    <AbsoluteFill style={{ justifyContent: "flex-end", alignItems: "center", paddingBottom: 54 }}>
      <div style={{ maxWidth: 1340, textAlign: "center", opacity: op, transform: `translateY(${interpolate(k, [0, 4], [10, 0], clamp)}px)`,
        background: "rgba(0,0,0,0.42)", borderRadius: 14, padding: "8px 26px 12px" }}>
        {c.words.map((w, i) => (
          <span key={i} style={{ fontFamily: tema.fuente.texto, fontWeight: 800, fontSize: 50, color: w.k ? C.acento : "#fff",
            WebkitTextStroke: "2px #000", paintOrder: "stroke fill", textShadow: "0 3px 8px rgba(0,0,0,.8)" }}>
            {w.w}{" "}
          </span>
        ))}
      </div>
    </AbsoluteFill>
  );
};

// ---------- Subtítulos palabra a palabra (Shorts) ----------
export const SubtitulosShort = ({ captions }) => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const c = captions.find((x) => f >= x.s && f < x.e + 3);
  if (!c) return null;
  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "flex-start", paddingTop: 1060 }}>
      <div style={{ width: 940, textAlign: "center", lineHeight: 1.12 }}>
        {c.words.map((w, i) => {
          const vis = f >= w.s;
          const cur = f >= w.s && f < w.e;
          const sp = spring({ frame: f - w.s, fps, config: { damping: 11, stiffness: 260 } });
          return (
            <span key={i} style={{ display: "inline-block", margin: "0 12px", opacity: vis ? 1 : 0,
              transform: `scale(${vis ? interpolate(sp, [0, 1], [0.6, cur ? 1.12 : 1]) : 0.6})`,
              ...tema.rotulo(78, w.k ? C.acento : "#fff") }}>
              {w.w}
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

// ---------- Efectos de sonido ----------
export const Sfx = ({ list }) => (
  <>
    {list.map((s, i) => (
      <Sequence key={i} from={Math.max(0, s.f)} durationInFrames={75}>
        <Audio src={staticFile(`sfx/${s.s}.wav`)} volume={s.v} />
      </Sequence>
    ))}
  </>
);

export { C };
