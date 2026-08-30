#!/usr/bin/env node
/**
 * nightly-ansi-palette-swatch
 * Prints the full 256‑color ANSI palette as colored blocks.
 *
 * Usage:
 *   npx ts-node src/index.ts
 *
 * The script outputs a grid where each cell shows its color code.
 */

export function generatePalette(): string {
  const rows: string[] = [];
  for (let row = 0; row < 16; row++) {
    const cells: string[] = [];
    for (let col = 0; col < 16; col++) {
      const code = row * 16 + col;
      // Background color block with padded code
      const block = `\x1b[48;5;${code}m  ${code.toString().padStart(3, ' ')}  \x1b[0m`;
      cells.push(block);
    }
    rows.push(cells.join(''));
  }
  return rows.join('\n');
}

// If executed directly, print to stdout
if (require.main === module) {
  console.log(generatePalette());
}
