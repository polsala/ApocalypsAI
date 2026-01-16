#!/usr/bin/env node
import { readFileSync } from 'fs';

/**
 * Convert a single character into a 4‑line, 2‑column block.
 * Each pair of bits (00,01,10,11) becomes a line of two symbols:
 *   0 → space, 1 → █
 */
function charToBlock(char: string): string[] {
  const code = char.charCodeAt(0);
  const bits = code.toString(2).padStart(8, '0');
  const block: string[] = [];
  for (let i = 0; i < 8; i += 2) {
    const pair = bits.slice(i, i + 2);
    const line = pair.split('').map(b => b === '1' ? '█' : ' ').join('');
    block.push(line);
  }
  return block;
}

/**
 * Generate a pseudo‑QR code for the given text.
 * The output is a square grid of ASCII characters.
 */
export function generatePseudoQR(text: string): string {
  const blocks = text.split('').map(charToBlock);
  const rowsPerChar = 4; // each block has 4 lines
  const colsPerChar = 2; // each line has 2 symbols
  const gridSize = Math.ceil(Math.sqrt(blocks.length));

  // Initialise empty grid rows
  const grid: string[][] = [];
  for (let i = 0; i < gridSize * rowsPerChar; i++) {
    grid.push(new Array(gridSize).fill(' '.repeat(colsPerChar)));
  }

  blocks.forEach((block, idx) => {
    const rowBlock = Math.floor(idx / gridSize);
    const colBlock = idx % gridSize;
    for (let r = 0; r < rowsPerChar; r++) {
      const line = block[r] ?? ' '.repeat(colsPerChar);
      const targetRow = rowBlock * rowsPerChar + r;
      grid[targetRow][colBlock] = line;
    }
  });

  return grid.map(row => row.join('')).join('\n');
}

// CLI execution
if (require.main === module) {
  const input = process.argv.slice(2).join(' ');
  if (!input) {
    console.error('Provide text to encode');
    process.exit(1);
  }
  console.log(generatePseudoQR(input));
}
