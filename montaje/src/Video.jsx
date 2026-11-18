import React, { createContext, useContext } from "react";
export const PostCtx = createContext(false);
export const CapasCtx = createContext(false); // true: solo rótulos/subtítulos/gráficos (la base de vídeo la monta ffmpeg)
import { AbsoluteFill, Sequence, Audio, OffthreadVideo, staticFile, useCurrentFrame, interpolate } from "remotion";
import { tema } from "./tema";
import { Media, Entrada, Acabado, Rotulo, Puesto, Ficha, Circulo, SubtitulosLargo, SubtitulosShort, Sfx, clamp, C } from "./base";
import * as G from "./graficos";
import { IconoLupa } from "./marca";

const OVERLAP = 8; // fotogramas de solape para las transiciones con movimiento

const Grafico = ({ sc, vertical }) => {
  switch (sc.graphic) {
    case "title": return <G.Titulo sc={sc} />;
    case "split": return <G.Dividida sc={sc} vertical={vertical} />;
    case "counter": return <G.Contador sc={sc} />;
    case "map": return <G.Mapa sc={sc} />;
    case "size": return <G.Tamano sc={sc} />;
    case "swallow": return <G.Traga sc={sc} />;
    case "years": return <G.Anos sc={sc} />;
    case "steps": return <G.Pasos sc={sc} />;
    case "step": return <G.Paso sc={sc} />;
    case "organs": return <G.Organos sc={sc} />;
    case "black": return <G.Negro sc={sc} />;
    case "spines": return <G.Espinas sc={sc} vertical={vertical} />;
    case "calendar": return <G.Calendario sc={sc} />;
    case "montage": return <G.Repaso sc={sc} />;
    case "end": return <G.Final sc={sc} />;
    default: return null;
  }
};

const Efectos = ({ sc }) => {
  const f = useCurrentFrame();
  return (
    <>
      {sc.dark && <AbsoluteFill style={{ background: "rgba(0,0,0,.45)" }} />}
      {sc.redtint && <AbsoluteFill style={{ background: C.peligro, mixBlendMode: "multiply", opacity: interpolate(f, [0, 8], [0, 0.75], clamp) }} />}
      {sc.soft && <AbsoluteFill style={{ background: "#000", opacity: interpolate(f, [0, 15, sc.len - 15, sc.len], [1, 0.25, 0.25, 1], clamp) }} />}
      {(sc.circle || sc.reveal) && <Circulo start={Math.round(sc.len * (sc.reveal ? 0.5 : 0.35))} len={sc.len} reveal={sc.reveal} />}
    </>
  );
};

const Escena = ({ sc, vertical }) => {
  const f = useCurrentFrame();
  const post = useContext(PostCtx);
  const soloCapas = useContext(CapasCtx);
  const textInGraphic = ["black"].includes(sc.graphic);
  const blur = sc.blur ? 4 + 4 * Math.sin(f / 7) : 0;
  return (
    <AbsoluteFill>
      <AbsoluteFill style={{ filter: `${post ? "" : tema.grade}${blur ? ` blur(${blur}px)` : ""}` || undefined }}>
        {sc.graphic && sc.graphic !== "step" ? <Grafico sc={sc} vertical={vertical} /> : null}
        {sc.graphic === "step" ? <Grafico sc={sc} vertical={vertical} /> : null}
        {!sc.graphic && !soloCapas && sc.shots.map((sh, i) => {
          const from = i === 0 ? 0 : sh.from - (sh.trans === "cut" ? 0 : OVERLAP);
          const len = sh.len + (sh.from - from) + (i === sc.shots.length - 1 ? 0 : 0);
          return (
            <Sequence key={i} from={from} durationInFrames={len}>
              <Entrada tipo={i === 0 ? "cut" : sh.trans}>
                <Media m={sh.media} len={len} kb={sh.kb} vertical={vertical} />
              </Entrada>
            </Sequence>
          );
        })}
      </AbsoluteFill>
      <Efectos sc={sc} />
      {sc.text && !textInGraphic && sc.graphic !== "years" && (
        <Sequence from={8} durationInFrames={Math.min(sc.len - 8, 95)}>
          <Rotulo text={sc.text} len={Math.min(sc.len - 8, 95)} vertical={vertical} y={vertical && sc.graphic === "step" ? 820 : undefined} />
        </Sequence>
      )}
    </AbsoluteFill>
  );
};

const Bloque = ({ b, vertical }) => (
  <AbsoluteFill>
    {b.scenes.map((sc, i) => (
      <Sequence key={i} from={sc.from} durationInFrames={sc.len}>
        <Escena sc={sc} vertical={vertical} />
      </Sequence>
    ))}
    {b.rank && (
      <Sequence from={0} durationInFrames={62}><Puesto text={b.rank} /></Sequence>
    )}
    {b.ficha && (
      <Sequence from={b.fichaAt ?? 40} durationInFrames={130}><Ficha ficha={b.ficha} len={130} /></Sequence>
    )}
  </AbsoluteFill>
);

// ---------- Vídeo largo / prueba (16:9) ----------
export const Largo = ({ plan, musica, post = false, soloCapas = false }) => (
  <PostCtx.Provider value={post || soloCapas}><CapasCtx.Provider value={soloCapas}>
    <LargoIn plan={plan} musica={soloCapas ? null : musica} post={post || soloCapas} soloCapas={soloCapas} />
  </CapasCtx.Provider></PostCtx.Provider>
);
const LargoIn = ({ plan, musica, post, soloCapas }) => {
  const f = useCurrentFrame();
  const end = plan.blocks.length ? plan.blocks[plan.blocks.length - 1] : null;
  const endF = end ? end.from + end.len : 0;
  return (
    <AbsoluteFill style={{ background: soloCapas ? "transparent" : C.fondo }}>
      {plan.blocks.map((b, i) => (
        <Sequence key={i} from={b.from} durationInFrames={b.len}>
          {b.video ? (soloCapas ? null : <OffthreadVideo src={staticFile(b.video)} />) : <>
            <Bloque b={b} />
            <Audio src={staticFile(b.audio)} endAt={b.audioLen}
              volume={(fr) => (b.cut ? interpolate(fr, [b.audioLen - 12, b.audioLen], [1, 0], clamp) : 1)} />
          </>}
        </Sequence>
      ))}
      {!soloCapas && <Acabado sinVineta={post} />}
      <SubtitulosLargo captions={plan.captions} />
      <Sfx list={plan.sfx} />
      {plan.credits && plan.credits.length > 0 && (
        <Sequence from={endF} durationInFrames={90}><G.Creditos lines={plan.credits} /></Sequence>
      )}
      {musica && (() => {
        // la intro trae su propia música: la de fondo baja a cero durante ella (fundidos de 0,5 s)
        const intro = plan.blocks.find((b) => b.video);
        const vol = (fr) => {
          if (!intro) return tema.musica.volumen;
          const a = intro.from, z = intro.from + intro.len;
          const k = interpolate(fr, [a - 15, a, z, z + 15], [1, 0, 0, 1], clamp);
          return tema.musica.volumen * k;
        };
        return <Audio src={staticFile(musica)} volume={vol} />;
      })()}
    </AbsoluteFill>
  );
};

// ---------- Shorts (9:16) ----------
const Gancho = ({ text, len }) => {
  const f = useCurrentFrame();
  const out = interpolate(f, [len - 8, len], [1, 0], clamp);
  return (
    <AbsoluteFill style={{ alignItems: "center", paddingTop: 300, opacity: out }}>
      <div style={{ ...tema.rotulo(118), textAlign: "center", maxWidth: 980, transform: `scale(${1 + Math.sin(f / 8) * 0.015})` }}>{text}</div>
    </AbsoluteFill>
  );
};

// Logo pequeño y discreto para los Shorts (esquina superior izquierda, algo transparente)
const LogoEsquina = () => (
  <AbsoluteFill style={{ pointerEvents: "none" }}>
    <div style={{ position: "absolute", left: 36, top: 52, display: "flex", alignItems: "center", gap: 6, opacity: 0.78, filter: "drop-shadow(0 2px 6px rgba(0,0,0,.6))" }}>
      <IconoLupa size={96} id="esq" />
      <div style={{ lineHeight: 1 }}>
        <div style={{ fontFamily: tema.fuente.titulo, fontWeight: 800, fontSize: 30, color: "#fff" }}>ALUCÍNATE</div>
        <div style={{ fontFamily: tema.fuente.texto, fontWeight: 500, fontSize: 13, letterSpacing: 4, color: "#7EDC86", marginTop: 3 }}>CON EL MUNDO</div>
      </div>
    </div>
  </AbsoluteFill>
);

export const Short = ({ plan, musica, logo = true }) => {
  const b = plan.blocks[0];
  const first = b.scenes[0];
  return (
    <AbsoluteFill style={{ background: C.fondo }}>
      <Bloque b={{ ...b, rank: null, ficha: null, scenes: b.scenes.map((s, i) => (i === 0 ? { ...s, text: null } : s)) }} vertical />
      <Audio src={staticFile(b.audio)} />
      <Acabado />
      <Sequence from={0} durationInFrames={first.len}><Gancho text={plan.hook} len={first.len} /></Sequence>
      <SubtitulosShort captions={plan.captions} />
      {logo && <LogoEsquina />}
      <Sfx list={plan.sfx} />
      {musica && <Audio src={staticFile(musica)} volume={tema.musica.volumen * 0.7} />}
    </AbsoluteFill>
  );
};
