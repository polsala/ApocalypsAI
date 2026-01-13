#!/usr/bin/env node
import { argv } from 'process';

type Color = 'red' | 'green' | 'yellow';
const colorCodes: Record<Color, string> = {
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
};
const reset = '\x1b[0m';

function mulberry32(a: number): () => number {
  return function() {
    let t = (a += 0x6d2b79f5);
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function getRandomColor(rng: () => number): Color {
  const colors: Color[] = ['red', 'green', 'yellow'];
  const idx = Math.floor(rng() * colors.length);
  return colors[idx];
}

const font: Record<string, string[]> = {
  A: [
    '  #  ',
    ' # # ',
    '#####',
    '#   #',
    '#   #',
  ],
  B: [
    '#### ',
    '#   #',
    '#### ',
    '#   #',
    '#### ',
  ],
  // Add more letters as needed. For now only A, B and space are defined.
  ' ': [
    '     ',
    '     ',
    '     ',
    '     ',
    '     ',
  ],
};

export function render(text: string, seed?: number): string {
  const rng = seed !== undefined ? mulberry32(seed) : mulberry32(Date.now() & 0xffffffff);
  const chars = text.toUpperCase().split('');
  const lines = Array(5).fill('');
  for (const ch of chars) {
    const pattern = font[ch] || font[' '];
    const color = getRandomColor(rng);
    const code = colorCodes[color];
    for (let i = 0; i < 5; i++) {
      lines[i] += code + pattern[i] + reset + ' ';
    }
  }
  return lines.join('\n');
}

function main() {
  const args = argv.slice(2);
  if (args.length === 0) {
    console.error('Usage: node main.ts "text" [--seed <number>]');
    process.exit(1);
  }
  const text = args[0];
  let seed: number | undefined;
  const seedIdx = args.indexOf('--seed');
  if (seedIdx !== -1 && args[seedIdx + 1]) {
    seed = parseInt(args[seedIdx + 1], 10);
  }
  const output = render(text, seed);
  console.log(output);
}

if (require.main === module) {
  main();
}

