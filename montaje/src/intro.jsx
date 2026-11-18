import React from "react";
import { AbsoluteFill, Sequence, Audio, Img, staticFile, useCurrentFrame, useVideoConfig, spring, interpolate, Easing } from "remotion";
import { tema } from "./tema";
import { Huella, Globo, Grad, G } from "./logos";
import MAPA_ORTO from "./data/mapa-intro.json";

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" };
const NAVY = "#0b2236";
const MAPA = "material/mapas/01_land_ocean_ice_2048_jpg.jpg";
const S = ({ at, s, v = 0.4 }) => (
  <Sequence from={Math.round(at)} durationInFrames={80}><Audio src={staticFile(`sfx/${s}.wav`)} volume={v} /></Sequence>
);

const Fondo = ({ children }) => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{ background: `radial-gradient(circle at 50% 45%, ${tema.color.fondo2}, ${tema.color.fondo} 70%)` }}>
      <svg width="1920" height="1080" style={{ position: "absolute" }}>
        {Array.from({ length: 90 }).map((_, i) => (
          <circle key={i} cx={(i * 733) % 1920} cy={(i * 397 + f * (0.2 + (i % 5) * 0.1)) % 1080} r={1 + (i % 4) * 0.6} fill="#bfefff" opacity={0.2 + (i % 7) / 14} />
        ))}
      </svg>
      {children}
    </AbsoluteFill>
  );
};

// ====== Intro «lupa buscadora» ======
// Lupa hueca (aro + mango). Recorre el planeta con pausas, como si buscara; cada elemento aparece en NEGRO
// sobre el planeta cuando el centro de la lupa pasa por él (pop + tic). A través del cristal se ve aumentado.
// Fases: huellas → (giro) → continentes + ruta + pin → (giro) → «¿?». Final: planeta fuera, lupa rebota, nombre en barrido.

const AROS = "#13233A";
const R_PLANETA = 220;
const SC = R_PLANETA / 280; // los elementos están dibujados para un planeta de 280 px
const R_LUPA = 125;
const AUMENTO = 1.25;
const T = { fijo: 26, lupa: 22, enLupa: 40, g1: 92, g2: 150, fin: 194, quieto: 230, total: 248 };
const SPIN = 9;

// 5 huellas dispersas, con ángulos variados (coordenadas para un planeta de 280 px)
const HUELLAS = [[-150, 95, -20], [70, -150, 35], [150, 55, -65], [-75, -70, 15], [15, 160, 80]];
// Continentes reales (NASA Blue Marble, proyección ortográfica lon −20 / lat 20); orden de búsqueda
const U = 280;
const ORDEN = ["europa", "africa", "sudamerica", "norteamerica"];
const CONT = ORDEN.map((k) => ({ k, c: MAPA_ORTO.continentes[k].c.map((v) => v * U) }));
const RUTA = MAPA_ORTO.ruta.map(([x, y]) => [x * U, y * U]);
const MEXICO = MAPA_ORTO.mexico.map((v) => v * U);
const DUDAS = [["¿", -120, -95, 140], ["?", 130, -35, 160], ["¿?", -20, 135, 120]];

// recorrido con pausas: en cada tramo la lupa acelera, frena y se queda un instante quieta
const recorrido = (pts, p) => {
  const n = pts.length - 1;
  const k = Math.min(n - 1, Math.floor(p * n));
  const t = Math.min(1, (p * n - k) / 0.72);
  const e = Easing.inOut(Easing.cubic)(t);
  return [pts[k][0] + (pts[k + 1][0] - pts[k][0]) * e, pts[k][1] + (pts[k + 1][1] - pts[k][1]) * e];
};

const posLupa = (f) => {
  const huellas = HUELLAS.map(([x, y]) => [x, y]);
  const ini = huellas[0];
  if (f < T.enLupa) return ini;
  if (f < T.g1) return recorrido(huellas, interpolate(f, [T.enLupa, T.g1 - 4], [0, 1], clamp));
  if (f < T.g1 + SPIN) return huellas[huellas.length - 1];
  const mapa = [huellas[huellas.length - 1], ...CONT.map((k) => k.c), MEXICO];
  if (f < T.g2) return recorrido(mapa, interpolate(f, [T.g1 + SPIN, T.g2 - 4], [0, 1], clamp));
  if (f < T.g2 + SPIN) return MEXICO;
  const dudas = [MEXICO, ...DUDAS.map(([, x, y]) => [x, y])];
  return recorrido(dudas, interpolate(f, [T.g2 + SPIN, T.fin - 4], [0, 1], clamp));
};

// primer fotograma en que el centro de la lupa pasa por (x, y) dentro de [desde, hasta]
const MEMO = {};
const encontrado = (x, y, desde, hasta) => {
  const key = `${x},${y},${desde}`;
  if (MEMO[key] === undefined) {
    MEMO[key] = null;
    for (let k = desde; k <= hasta; k++) { const [lx, ly] = posLupa(k); if (Math.hypot(lx - x, ly - y) < 30) { MEMO[key] = k; break; } }
  }
  return MEMO[key];
};
const pop = (f, t0) => (t0 === null || f < t0 ? 0 : spring({ frame: f - t0, fps: 30, config: { damping: 8, stiffness: 180 } }));

const Escondido = ({ f }) => {
  const sale = (t) => interpolate(f, [t - 2, t + 6], [1, 0], clamp);
  const huellasOp = sale(T.g1), mapaOp = sale(T.g2);
  const finRuta = encontrado(...MEXICO, T.g1 + SPIN, T.g2);
  const pr = finRuta === null ? 0 : interpolate(f, [finRuta - 22, finRuta], [0, 1], clamp);
  return (
    <g transform={`scale(${SC})`}>
      {f < T.g1 + 6 && HUELLAS.map(([x, y, rot], i) => {
        const a = pop(f, encontrado(x, y, T.enLupa, T.g1));
        return <g key={i} opacity={huellasOp} transform={`translate(${x} ${y}) rotate(${rot}) scale(${0.3 * a})`}><Huella fill="#050505" /></g>;
      })}
      {f >= T.g1 && f < T.g2 + 6 && (
        <g opacity={mapaOp}>
          {CONT.map(({ k, c }, i) => {
            const a = pop(f, encontrado(...c, T.g1 + SPIN, T.g2));
            return <image key={k} href={staticFile(`intro/continente-${k}.png`)} x={-U} y={-U} width={2 * U} height={2 * U}
              transform={`translate(${c[0]} ${c[1]}) scale(${a}) translate(${-c[0]} ${-c[1]})`} />;
          })}
          {pr > 0 && (() => {
            const pts = RUTA.slice(0, Math.max(2, Math.round(pr * RUTA.length)));
            const d = `M ${pts.map(([x, y]) => `${x.toFixed(1)} ${y.toFixed(1)}`).join(" L ")}`;
            return <g><path d={d} fill="none" stroke="#050505" strokeWidth={13} strokeLinecap="round" strokeDasharray="18 14" />
              <path d={d} fill="none" stroke="#ffffff" strokeWidth={7} strokeLinecap="round" strokeDasharray="18 14" /></g>;
          })()}
          {(() => { const a = pop(f, finRuta); const [px, py] = MEXICO; return (
            <g transform={`translate(${px} ${py}) scale(${a * 1.2})`}>
              <path d="M0 0 C -24 -32 -24 -56 0 -62 C 24 -56 24 -32 0 0Z" fill={tema.color.peligro} stroke="#fff" strokeWidth={4} />
              <circle cy={-43} r={8} fill="#fff" />
            </g>); })()}
        </g>
      )}
      {f >= T.g2 && DUDAS.map(([c, x, y, sz], i) => {
        const a = pop(f, encontrado(x, y, T.g2 + SPIN, T.fin));
        return <text key={i} opacity={sale(T.fin + 2)} x={x} y={y + sz / 3} textAnchor="middle" fill="#050505" style={{ fontFamily: tema.fuente.titulo, fontWeight: 800, fontSize: sz }}
          transform={`translate(${x} ${y}) scale(${a}) translate(${-x} ${-y})`}>{c}</text>;
      })}
    </g>
  );
};

const Lupa = ({ x, y, giro = 0, escala = 1, r = R_LUPA }) => (
  <g transform={`translate(${x} ${y}) rotate(${giro}) scale(${escala})`}>
    <circle r={r + 14} fill="none" stroke="url(#iA)" strokeWidth={4} />
    {/* mango: arranca bajo el aro (borde superior a 0,9·r, cubierto por el aro) */}
    <g transform="rotate(45)"><rect x={r * 0.9} y={-38} width={250} height={76} rx={34} fill={AROS} stroke="url(#iT)" strokeWidth={6} /></g>
    <circle r={r} fill="none" stroke={AROS} strokeWidth={28} />
    <circle r={r - 14} fill="none" stroke="rgba(255,255,255,.3)" strokeWidth={3} />
    <path d={`M ${-r * 0.62} ${-r * 0.42} A ${r * 0.75} ${r * 0.75} 0 0 1 ${-r * 0.18} ${-r * 0.72}`} stroke="#fff" strokeWidth={9} strokeLinecap="round" fill="none" opacity={0.45} />
  </g>
);

const Nombre = ({ barrido, lema, y, escala = 1 }) => (
  <div style={{ position: "absolute", left: 0, right: 0, top: y, textAlign: "center" }}>
    <div style={{ display: "inline-block", position: "relative", transform: `scale(${escala})`, transformOrigin: "50% 0" }}>
      <div style={{ clipPath: `inset(-30px ${100 - barrido}% -30px -30px)`, textAlign: "center" }}>
        <div style={{ fontFamily: tema.fuente.titulo, fontWeight: 800, fontSize: 150, lineHeight: 1.18, paddingTop: 6, background: `linear-gradient(90deg, ${G[0]}, ${G[1]}, ${G[2]})`, WebkitBackgroundClip: "text", color: "transparent" }}>ALUCÍNATE</div>
        <div style={{ fontFamily: tema.fuente.texto, fontWeight: 500, fontSize: 54, letterSpacing: 22, color: "#ffffff", marginTop: 6, paddingLeft: 22 }}>CON EL MUNDO</div>
      </div>
      <div style={{ position: "absolute", left: `${barrido}%`, top: -10, width: 10, height: 250, background: G[2], opacity: barrido > 2 && barrido < 99 ? 0.9 : 0, filter: "blur(2px)", boxShadow: `0 0 30px ${G[2]}` }} />
      <div style={{ opacity: lema, marginTop: 18, fontFamily: tema.fuente.texto, fontWeight: 600, fontSize: 30, letterSpacing: 5, color: "#9fc3cc" }}>CURIOSIDADES QUE NO TE VAS A CREER</div>
    </div>
  </div>
);

const giroEn = (f, t) => interpolate(f, [t - SPIN / 2, t + SPIN / 2], [0, 360], { ...clamp, easing: Easing.inOut(Easing.cubic) });
const dosBotes = (p) => {
  if (p <= 0 || p >= 1) return 0;
  return p < 0.55 ? Math.sin((p / 0.55) * Math.PI) * 140 : Math.sin(((p - 0.55) / 0.45) * Math.PI) * 60;
};

// Planeta con meridianos muy atenuados
const Planeta = ({ rot }) => <Globo r={R_PLANETA} rot={rot} w={4} line="rgba(255,255,255,.16)" />;

export const IntroLupa = ({ vertical = false, desde = 0 }) => {
  const f = useCurrentFrame() + desde;
  const { width, height } = useVideoConfig();
  const cx = width / 2, cy = vertical ? height * 0.42 : height / 2;
  const zoomIn = interpolate(f, [0, T.fijo], [9, 1], { ...clamp, easing: Easing.out(Easing.exp) });
  const q = interpolate(f, [T.fin, T.fin + 16], [0, 1], { ...clamp, easing: Easing.inOut(Easing.cubic) });
  const fuera = 1;
  const rot = f * 1.6;
  const ent = interpolate(f, [T.lupa, T.enLupa], [0, 1], { ...clamp, easing: Easing.out(Easing.back(1.2)) });
  const lp = posLupa(f).map((v) => v * SC);
  const bx = f < T.enLupa ? interpolate(ent, [0, 1], [-cx - 300, lp[0]]) : lp[0];
  const by = lp[1];
  const giro = giroEn(f, T.g1 + SPIN / 2) + giroEn(f, T.g2 + SPIN / 2);
  const p = interpolate(f, [T.fin, T.quieto], [0, 1], { ...clamp, easing: Easing.out(Easing.quad) });
  const finX = cx, finY = vertical ? height * 0.32 : cy - 235;
  const lx = f < T.fin ? cx + bx : interpolate(p, [0, 1], [cx + bx, finX]);
  const ly = f < T.fin ? cy + by : interpolate(p, [0, 1], [cy + by, finY]) - dosBotes(interpolate(f, [T.fin, T.quieto], [0, 1], clamp));
  const g = giro + interpolate(f, [T.fin, T.fin + 24], [0, 360], { ...clamp, easing: Easing.out(Easing.cubic) });
  const esc = f < T.fin ? 1 : interpolate(p, [0, 1], [1, vertical ? 1.15 : 1.0]);
  const barrido = interpolate(f, [T.fin + 12, T.fin + 32], [0, 100], { ...clamp, easing: Easing.out(Easing.cubic) });
  const lema = interpolate(f, [T.fin + 28, T.fin + 40], [0, 1], clamp);
  const salida = interpolate(f, [T.total - 6, T.total], [1, 0], clamp);
  const busca = f >= T.lupa && f < T.fin;
  // al final el planeta viaja al centro de la lupa y se encoge al tamaño de la lente (queda de fondo dentro de ella)
  const kLente = ((R_LUPA - 11) * esc) / R_PLANETA; // el borde del planeta queda bajo el aro
  const planeta = zoomIn * (1 + (kLente - 1) * q);
  const pcx = cx + (lx - cx) * q, pcy = cy + (ly - cy) * q;
  // tics: uno por elemento encontrado
  const tics = [
    ...HUELLAS.map(([x, y]) => encontrado(x, y, T.enLupa, T.g1)),
    ...CONT.map((k) => encontrado(...k.c, T.g1 + SPIN, T.g2)),
    ...DUDAS.map(([, x, y]) => encontrado(x, y, T.g2 + SPIN, T.fin)),
  ].filter((t) => t !== null);
  const finRuta = encontrado(...MEXICO, T.g1 + SPIN, T.g2);
  return (
    <AbsoluteFill style={{ background: "#0B1220" }}>
      <svg width={width} height={height} style={{ position: "absolute" }}>
        {Array.from({ length: 70 }).map((_, i) => (
          <circle key={i} cx={(i * 733) % width} cy={(i * 397) % height} r={0.8 + (i % 4) * 0.5} fill="#cfe9ff" opacity={0.1 + (i % 6) / 30} />
        ))}
      </svg>
      <AbsoluteFill style={{ opacity: salida }}>
        <svg width={width} height={height} style={{ position: "absolute" }}>
          <defs>
            <Grad id="iA" /><Grad id="iT" angle={-45} /><Grad id="gA" />
            <clipPath id="lenteHueca"><circle cx={lx} cy={ly} r={R_LUPA - 11} /></clipPath>
            <radialGradient id="cristal" cx="35%" cy="30%" r="75%">
              <stop offset="0%" stopColor="#ffffff" stopOpacity="0.16" /><stop offset="60%" stopColor="#ffffff" stopOpacity="0.03" /><stop offset="100%" stopColor="#ffffff" stopOpacity="0.1" />
            </radialGradient>
          </defs>
          {planeta > 0.01 && (
            <g transform={`translate(${pcx} ${pcy}) scale(${planeta})`}>
              <circle r={R_PLANETA + 36} fill="url(#iA)" opacity={0.13 * (1 - q)} />
              <Planeta rot={rot} />
              <Escondido f={f} />
            </g>
          )}
          {busca && planeta > 0.01 && (
            <g clipPath="url(#lenteHueca)">
              <g transform={`translate(${lx} ${ly}) scale(${AUMENTO}) translate(${-lx} ${-ly})`}>
                <g transform={`translate(${cx} ${cy}) scale(${planeta})`}>
                  <Planeta rot={rot} />
                  <Escondido f={f} />
                </g>
              </g>
            </g>
          )}
          {f >= T.lupa && <circle cx={lx} cy={ly} r={(R_LUPA - 13) * esc} fill="url(#cristal)" />}
          {f >= T.lupa && <Lupa x={lx} y={ly} giro={g} escala={esc} />}
        </svg>
        {f >= T.fin && <Nombre barrido={barrido} lema={lema} y={vertical ? height * 0.475 : cy + 20} escala={vertical ? 0.95 : 1} />}
      </AbsoluteFill>
      {desde === 0 && <>
        <S at={0} s="riser" v={0.3} />
        <S at={T.fijo - 2} s="impacto" v={0.3} />
        <S at={T.lupa} s="whoosh" v={0.45} />
        {tics.map((t, i) => <S key={i} at={t} s="tick" v={0.38} />)}
        {tics.map((t, i) => <S key={`p${i}`} at={t + 1} s="pop" v={0.18} />)}
        {finRuta !== null && <S at={finRuta} s="pop" v={0.4} />}
        <S at={T.g1} s="whoosh-corto" v={0.55} />
        <S at={T.g2} s="whoosh-corto" v={0.55} />
      </>}
      <S at={T.fin - desde} s="whoosh" v={0.5} />
      <S at={T.fin + 12 - desde} s="tick" v={0.3} />
      <S at={T.fin + 24 - desde} s="tick" v={0.25} />
      <S at={T.fin + 30 - desde} s="impacto" v={0.45} />
    </AbsoluteFill>
  );
};
export const INTRO_LUPA_TOTAL = T.total;
export const INTRO_LUPA_FIN = T.fin;

// ---------- Intro B (alternativa): iconos en órbita → el planeta se convierte en el logo con destello ----------
export const IntroOrbita = () => {
  const f = useCurrentFrame();
  const { fps } = useVideoConfig();
  const ap = spring({ frame: f, fps, config: { damping: 12 } });
  const orbit = f * 3;
  const junta = interpolate(f, [90, 115], [1, 0], { ...clamp, easing: Easing.in(Easing.cubic) });
  const flash = interpolate(f, [115, 118, 128], [0, 1, 0], clamp);
  const logo = spring({ frame: f - 116, fps, config: { damping: 10 } });
  const iconos = [
    (k) => <g transform="scale(.25)"><Huella fill={G[2]} /></g>,
    (k) => <text textAnchor="middle" y={30} fill={G[0]} style={{ fontFamily: tema.fuente.titulo, fontWeight: 800, fontSize: 110 }}>?</text>,
    (k) => <path d="M-60 40 L-10 -50 L20 0 L35 -25 L70 40 Z" fill="#e9f7ef" />,
    (k) => <path d="M0 -55 L14 -14 L55 0 L14 14 L0 55 L-14 14 L-55 0 L-14 -14 Z" fill={G[2]} />,
    (k) => <g><ellipse rx={60} ry={34} fill="#fff" /><circle r={22} fill={G[0]} /><circle r={10} fill={NAVY} /></g>,
  ];
  const salida = interpolate(f, [170, 180], [1, 0], clamp);
  return (
    <Fondo>
      <AbsoluteFill style={{ opacity: salida }}>
        <svg width="1920" height="1080" style={{ position: "absolute" }}>
          <defs><Grad id="gA" /><Grad id="oT" angle={-45} /></defs>
          <g transform={`translate(960 470) scale(${ap * (1 - 0.35 * logo)})`}>
            <ellipse rx={420 * junta + 1} ry={120 * junta + 1} fill="none" stroke="url(#gA)" strokeWidth={4} opacity={0.5 * junta} />
            <Globo r={200} rot={f * 2} w={6} />
            {iconos.map((ic, i) => {
              const a = ((orbit + i * 72) * Math.PI) / 180;
              const x = Math.cos(a) * 420 * junta, y = Math.sin(a) * 120 * junta;
              const front = Math.sin(a) > 0;
              return <g key={i} transform={`translate(${x} ${y}) scale(${(front ? 1.1 : 0.75) * ap})`} opacity={front ? 1 : 0.6}>{ic(i)}</g>;
            })}
          </g>
        </svg>
        <AbsoluteFill style={{ alignItems: "center", justifyContent: "flex-end", paddingBottom: 150 }}>
          <div style={{ transform: `scale(${logo})`, textAlign: "center" }}>
            <div style={{ fontFamily: tema.fuente.titulo, fontWeight: 800, fontSize: 120, color: "#fff", lineHeight: 0.95, WebkitTextStroke: "5px #000", paintOrder: "stroke fill" }}>
              ¡ALUCÍNATE <span style={{ background: `linear-gradient(90deg, ${G[0]}, ${G[1]}, ${G[2]})`, WebkitBackgroundClip: "text", color: "transparent", WebkitTextStroke: "0" }}>CON EL MUNDO!</span>
            </div>
          </div>
        </AbsoluteFill>
        <AbsoluteFill style={{ background: "#fff", opacity: flash }} />
      </AbsoluteFill>
      <S at={0} s="whoosh" v={0.45} /><S at={88} s="riser" v={0.4} /><S at={116} s="impacto" v={0.5} />
    </Fondo>
  );
};

// ---------- Intro corta (3 s) para los vídeos largos: planeta → entra en la lupa → nombre ----------
const TC = { zoom: 14, lupa: 8, enLupa: 20, enc: 22, encFin: 38, quieto: 58, total: 90 };
export const IntroCorta = () => {
  const f = useCurrentFrame();
  const { width, height } = useVideoConfig();
  const cx = width / 2, cy = height / 2;
  const zoomIn = interpolate(f, [0, TC.zoom], [9, 1], { ...clamp, easing: Easing.out(Easing.exp) });
  const ent = interpolate(f, [TC.lupa, TC.enLupa], [0, 1], { ...clamp, easing: Easing.out(Easing.back(1.2)) });
  const q = interpolate(f, [TC.enc, TC.encFin], [0, 1], { ...clamp, easing: Easing.inOut(Easing.cubic) });
  const p = interpolate(f, [TC.enc, TC.quieto], [0, 1], { ...clamp, easing: Easing.out(Easing.quad) });
  const finY = cy - 235;
  const lx = interpolate(ent, [0, 1], [-300, cx]);
  const ly = interpolate(p, [0, 1], [cy, finY]) - dosBotes(interpolate(f, [TC.enc, TC.quieto], [0, 1], clamp));
  const g = interpolate(f, [TC.lupa, TC.enLupa], [-200, 0], clamp) + interpolate(f, [TC.enc, TC.enc + 20], [0, 360], { ...clamp, easing: Easing.out(Easing.cubic) });
  const kLente = (R_LUPA - 11) / R_PLANETA;
  const planeta = zoomIn * (1 + (kLente - 1) * q);
  const pcx = cx + (lx - cx) * q, pcy = cy + (ly - cy) * q;
  const barrido = interpolate(f, [TC.enc + 12, TC.enc + 32], [0, 100], { ...clamp, easing: Easing.out(Easing.cubic) });
  const lema = interpolate(f, [TC.enc + 26, TC.enc + 38], [0, 1], clamp);
  const salida = interpolate(f, [TC.total - 6, TC.total], [1, 0], clamp);
  return (
    <AbsoluteFill style={{ background: "#0B1220" }}>
      <svg width={width} height={height} style={{ position: "absolute" }}>
        {Array.from({ length: 70 }).map((_, i) => (
          <circle key={i} cx={(i * 733) % width} cy={(i * 397) % height} r={0.8 + (i % 4) * 0.5} fill="#cfe9ff" opacity={0.1 + (i % 6) / 30} />
        ))}
      </svg>
      <AbsoluteFill style={{ opacity: salida }}>
        <svg width={width} height={height} style={{ position: "absolute" }}>
          <defs>
            <Grad id="iA" /><Grad id="iT" angle={-45} /><Grad id="gA" />
            <radialGradient id="cristalC" cx="35%" cy="30%" r="75%">
              <stop offset="0%" stopColor="#ffffff" stopOpacity="0.16" /><stop offset="60%" stopColor="#ffffff" stopOpacity="0.03" /><stop offset="100%" stopColor="#ffffff" stopOpacity="0.1" />
            </radialGradient>
          </defs>
          <g transform={`translate(${pcx} ${pcy}) scale(${planeta})`}>
            <circle r={R_PLANETA + 36} fill="url(#iA)" opacity={0.13 * (1 - q)} />
            <Globo r={R_PLANETA} rot={f * 2} w={4} line="rgba(255,255,255,.16)" />
          </g>
          {f >= TC.lupa && <circle cx={lx} cy={ly} r={R_LUPA - 13} fill="url(#cristalC)" opacity={q} />}
          {f >= TC.lupa && <Lupa x={lx} y={ly} giro={g} escala={1} />}
        </svg>
        {f >= TC.enc && <Nombre barrido={barrido} lema={lema} y={cy + 20} />}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
export const INTRO_CORTA = TC;
