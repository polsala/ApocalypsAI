type RGB = { r: number; g: number; b: number };

const palette: { name: string; rgb: RGB }[] = [
  { name: "Radioactive Ash", rgb: { r: 34, g: 139, b: 34 } }, // forestgreen
  { name: "Molten Ember", rgb: { r: 255, g: 69, b: 0 } }, // orangered
  { name: "Dusty Twilight", rgb: { r: 72, g: 61, b: 139 } }, // darkslateblue
  { name: "Cobalt Wasteland", rgb: { r: 0, g: 71, b: 171 } }, // cobalt
  { name: "Sooty Night", rgb: { r: 25, g: 25, b: 112 } }, // midnightblue
  { name: "Fungal Glow", rgb: { r: 154, g: 205, b: 50 } }, // yellowgreen
];

function hexToRgb(hex: string): RGB {
  const clean = hex.replace(/^#/, "");
  if (!/^[0-9a-fA-F]{6}$/.test(clean)) {
    throw new Error("Invalid hex color");
  }
  const num = parseInt(clean, 16);
  return {
    r: (num >> 16) & 0xff,
    g: (num >> 8) & 0xff,
    b: num & 0xff,
  };
}

function distance(a: RGB, b: RGB): number {
  return Math.sqrt(
    (a.r - b.r) ** 2 + (a.g - b.g) ** 2 + (a.b - b.b) ** 2
  );
}

/**
 * Returns the apocalypse‑themed name closest to the given hex color.
 * @param hex e.g. "#ff4500"
 */
export function getApocalypseName(hex: string): string {
  const rgb = hexToRgb(hex);
  let best = palette[0];
  let bestDist = distance(rgb, best.rgb);
  for (const entry of palette.slice(1)) {
    const d = distance(rgb, entry.rgb);
    if (d < bestDist) {
      best = entry;
      bestDist = d;
    }
  }
  return best.name;
}
