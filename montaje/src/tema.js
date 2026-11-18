// Tema visual del canal «Alucínate con el mundo»: paleta, tipografía y medidas.
// Todo el canal usa este archivo: si cambias un color aquí, cambia en todos los vídeos.
export const tema = {
  color: {
    fondo: "#05111d", // azul abisal casi negro
    fondo2: "#0b2236",
    acento: "#FFD60A", // amarillo «peligro»: palabras clave, números de puesto
    peligro: "#E63946", // rojo: círculos, calaveras, zonas del mapa
    agua: "#2EC4B6", // turquesa: detalles, barras
    texto: "#FFFFFF",
    borde: "#000000",
    tarjeta: "rgba(5,17,29,0.82)",
  },
  fuente: {
    titulo: "'Avenir Next Condensed', 'Avenir Next', 'Arial Black', Impact, sans-serif",
    texto: "'Avenir Next', 'Helvetica Neue', Arial, sans-serif",
  },
  // Texto grueso blanco con borde negro (rótulos clave)
  rotulo: (px, color = "#FFFFFF") => ({
    fontFamily: "'Avenir Next Condensed', 'Avenir Next', 'Arial Black', Impact, sans-serif",
    fontWeight: 800,
    fontSize: px,
    color,
    WebkitTextStroke: `${Math.max(3, Math.round(px / 11))}px #000`,
    paintOrder: "stroke fill",
    textShadow: `0 ${Math.round(px / 14)}px ${Math.round(px / 5)}px rgba(0,0,0,0.65)`,
    letterSpacing: "0.01em",
    lineHeight: 1.02,
    textTransform: "none",
  }),
  grade: "contrast(1.08) saturate(1.14) brightness(0.98)", // corrección de color básica
  musica: { volumen: 0.08 }, // ≈ −22 dB bajo la voz
};
