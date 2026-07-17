#!/usr/bin/env node
import { readFileSync } from 'fs';

/**
 * Convert a single character to an 8‑character block string.
 * 1 → █, 0 → space.
 */
function charToBlocks(ch: string): string {
  const code = ch.charCodeAt(0);
  const bin = code.toString(2).padStart(8, '0');
  return bin.replace(/1/g, '█').replace(/0/g, ' ');
}

/**
 * Convert an entire string into a multiline block pattern.
 */
export function textToBlockPattern(text: string): string {
  return text.split('').map(charToBlocks).join('\n');
}

// CLI entry point
if (require.main === module) {
  const args = process.argv.slice(2);
  let input = args.join(' ');
  if (!input) {
    // Read from STDIN if no arguments were provided
    try {
      input = readFileSync(0, 'utf-8').trim();
    } catch {
      console.error('No input provided.');
      process.exit(1);
    }
  }
  const output = textToBlockPattern(input);
  console.log(output);
}
