import * as process from 'process';

/**
 * Convert a hex colour string (e.g. "#ff00aa" or "ff00aa") to an RGB object.
 */
export function hexToRgb(hex: string): { r: number; g: number; b: number } {
  const clean = hex.replace(/^#/, '');
  if (!/^[0-9a-fA-F]{6}$/.test(clean)) {
    throw new Error(`Invalid hex colour: ${hex}`);
  }
  const r = parseInt(clean.slice(0, 2), 16);
  const g = parseInt(clean.slice(2, 4), 16);
  const b = parseInt(clean.slice(4, 6), 16);
  return { r, g, b };
}

/** Convert an RGB object back to a hex string (always lower‑case, prefixed with #). */
export function rgbToHex(r: number, g: number, b: number): string {
  const toHex = (n: number) => n.toString(16).padStart(2, '0');
  return `#${toHex(r)}${toHex(g)}${toHex(b)}`;
}

/** Invert each RGB channel – a simple (but visually pleasing) complementary colour. */
export function complementary(hex: string): string {
  const { r, g, b } = hexToRgb(hex);
  return rgbToHex(255 - r, 255 - g, 255 - b);
}

/** Adjust brightness by a factor ( >1 = lighter, <1 = darker ). */
export function adjustBrightness(hex: string, factor: number): string {
  const { r, g, b } = hexToRgb(hex);
  const clamp = (n: number) => Math.max(0, Math.min(255, Math.round(n)));
  return rgbToHex(
    clamp(r * factor),
    clamp(g * factor),
    clamp(b * factor)
  );
}

/** Convert to grayscale using the average method. */
export function grayscale(hex: string): string {
  const { r, g, b } = hexToRgb(hex);
  const avg = Math.round((r + g + b) / 3);
  return rgbToHex(avg, avg, avg);
}

/** Helper to print a coloured block in the terminal. */
function colourBlock(hex: string): string {
  const { r, g, b } = hexToRgb(hex);
  return `\u001b[38;2;${r};${g};${b}m█\u001b[0m`;
}

/** Generate the full palette and print it. */
function printPalette(baseHex: string): void {
  const original = baseHex.startsWith('#') ? baseHex : `#${baseHex}`;
  const palette = {
    Original: original,
    Complementary: complementary(original),
    Lighter: adjustBrightness(original, 1.2),
    Darker: adjustBrightness(original, 0.8),
    Grayscale: grayscale(original)
  };
  for (const [name, colour] of Object.entries(palette)) {
    console.log(`${name.padEnd(12)}: ${colour} ${colourBlock(colour)}`);
  }
}

// CLI entry point
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length !== 1) {
    console.error('Usage: node dist/main.js <hex-colour>');
    process.exit(1);
  }
  try {
    printPalette(args[0]);
  } catch (e) {
    console.error((e as Error).message);
    process.exit(1);
  }
}

export default {
  hexToRgb,
  rgbToHex,
  complementary,
  adjustBrightness,
  grayscale
};
