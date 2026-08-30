export function hexToRgb(hex: string): { r: number; g: number; b: number } | null {
  // Remove optional leading '#'
  const cleaned = hex.replace(/^#/, "");
  if (!/^[0-9a-fA-F]{6}$/.test(cleaned)) {
    return null;
  }
  const r = parseInt(cleaned.slice(0, 2), 16);
  const g = parseInt(cleaned.slice(2, 4), 16);
  const b = parseInt(cleaned.slice(4, 6), 16);
  return { r, g, b };
}

function rgbToHue(r: number, g: number, b: number): number {
  // Convert RGB [0‑255] to HSL and return the hue component (0‑360)
  const rp = r / 255;
  const gp = g / 255;
  const bp = b / 255;
  const max = Math.max(rp, gp, bp);
  const min = Math.min(rp, gp, bp);
  const delta = max - min;
  if (delta === 0) return 0; // achromatic
  let hue: number;
  if (max === rp) {
    hue = ((gp - bp) / delta) % 6;
  } else if (max === gp) {
    hue = (bp - rp) / delta + 2;
  } else {
    hue = (rp - gp) / delta + 4;
  }
  hue *= 60;
  if (hue < 0) hue += 360;
  return hue;
}

const hueNameMap: { range: [number, number]; name: string }[] = [
  { range: [0, 30], name: "Red Fury" },
  { range: [30, 90], name: "Orange Blaze" },
  { range: [90, 150], name: "Yellow Sunburst" },
  { range: [150, 210], name: "Green Meadow" },
  { range: [210, 270], name: "Blue Ocean" },
  { range: [270, 330], name: "Indigo Twilight" },
  { range: [330, 360], name: "Violet Dream" },
];

export function getColorName(hex: string): string {
  const rgb = hexToRgb(hex);
  if (!rgb) {
    throw new Error(`Invalid hex colour: ${hex}`);
  }
  const hue = rgbToHue(rgb.r, rgb.g, rgb.b);
  for (const entry of hueNameMap) {
    const [low, high] = entry.range;
    if (hue >= low && hue < high) {
      return entry.name;
    }
  }
  // Fallback (should never happen)
  return "Mystic Shade";
}

// CLI handling
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length !== 1) {
    console.error("Usage: node index.js <hex-colour>");
    process.exit(1);
  }
  try {
    const name = getColorName(args[0]);
    console.log(name);
  } catch (e) {
    console.error((e as Error).message);
    process.exit(1);
  }
}
