#!/usr/bin/env node
const ansiMap = {
  black: 0,
  maroon: 1,
  green: 2,
  olive: 3,
  navy: 4,
  purple: 5,
  teal: 6,
  silver: 7,
  grey: 8,
  red: 9,
  lime: 10,
  yellow: 11,
  blue: 12,
  fuchsia: 13,
  aqua: 14,
  white: 15,
  // extended palette
  orange: 208,
  pink: 213,
  brown: 94,
  gold: 220,
  cyan: 51,
  magenta: 201
};

function normalize(name) {
  return name.trim().toLowerCase();
}

/**
 * Returns the ANSI 256‑color code for a supported color name.
 * @param {string} colorName
 * @returns {number|null} ANSI code or null if unsupported
 */
function getAnsiCode(colorName) {
  const key = normalize(colorName);
  return Object.prototype.hasOwnProperty.call(ansiMap, key) ? ansiMap[key] : null;
}

/**
 * Prints the color name, its ANSI code, and a sample block.
 * @param {string} colorName
 */
function printSample(colorName) {
  const code = getAnsiCode(colorName);
  if (code === null) {
    console.error(`Unsupported color: ${colorName}`);
    process.exit(1);
  }
  const sample = `\x1b[38;5;${code}m█\x1b[0m`;
  console.log(`Color: ${colorName} → ANSI 256 code: ${code}`);
  console.log(`Sample: ${sample}`);
}

// CLI entry point
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length !== 1) {
    console.error('Usage: node src/index.js <color-name>');
    process.exit(1);
  }
  printSample(args[0]);
}

module.exports = { getAnsiCode };
