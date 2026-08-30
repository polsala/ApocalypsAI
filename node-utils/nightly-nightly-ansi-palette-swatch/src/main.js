// nightly-ansi-palette-swatch
// Prints the 256‑color ANSI palette with optional color codes.

const process = require('process');

/**
 * Convert an xterm 256‑color index to its RGB components.
 * @param {number} n - Color index (0‑255)
 * @returns {{r:number,g:number,b:number}}
 */
function indexToRGB(n) {
  if (n < 16) {
    // Standard and high‑intensity colors – use a static table.
    const table = [
      [0, 0, 0], [128, 0, 0], [0, 128, 0], [128, 128, 0],
      [0, 0, 128], [128, 0, 128], [0, 128, 128], [192, 192, 192],
      [128, 128, 128], [255, 0, 0], [0, 255, 0], [255, 255, 0],
      [0, 0, 255], [255, 0, 255], [0, 255, 255], [255, 255, 255]
    ];
    return { r: table[n][0], g: table[n][1], b: table[n][2] };
  } else if (n >= 16 && n <= 231) {
    // 6×6×6 color cube.
    const i = n - 16;
    const r = Math.floor(i / 36);
    const g = Math.floor((i % 36) / 6);
    const b = i % 6;
    const level = [0, 95, 135, 175, 215, 255];
    return { r: level[r], g: level[g], b: level[b] };
  } else if (n >= 232 && n <= 255) {
    // Grayscale ramp.
    const gray = 8 + (n - 232) * 10;
    return { r: gray, g: gray, b: gray };
  }
  // Fallback (should never happen).
  return { r: 0, g: 0, b: 0 };
}

/**
 * Convert RGB to a hex string.
 * @param {{r:number,g:number,b:number}} rgb
 * @returns {string}
 */
function rgbToHex({ r, g, b }) {
  const toHex = (v) => v.toString(16).padStart(2, '0');
  return `#${toHex(r)}${toHex(g)}${toHex(b)}`;
}

/**
 * Parse command‑line arguments.
 * @returns {{format:string|null}}
 */
function parseArgs() {
  const args = process.argv.slice(2);
  const result = { format: null };
  args.forEach(arg => {
    if (arg.startsWith('--format=')) {
      const fmt = arg.split('=')[1];
      if (['hex', 'rgb'].includes(fmt)) {
        result.format = fmt;
      }
    }
  });
  return result;
}

function printPalette(format) {
  const cols = 16;
  for (let row = 0; row < 16; row++) {
    let line = '';
    for (let col = 0; col < cols; col++) {
      const idx = row * cols + col;
      const block = `\x1b[38;5;${idx}m█\x1b[0m`;
      let suffix = '';
      if (format === 'hex') {
        const hex = rgbToHex(indexToRGB(idx));
        suffix = ` ${hex}`;
      } else if (format === 'rgb') {
        const { r, g, b } = indexToRGB(idx);
        suffix = ` rgb(${r},${g},${b})`;
      }
      line += block + suffix + ' ';
    }
    console.log(line.trimEnd());
  }
}

const { format } = parseArgs();
printPalette(format);
