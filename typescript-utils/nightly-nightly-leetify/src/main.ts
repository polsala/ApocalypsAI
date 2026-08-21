#!/usr/bin/env ts-node
import * as fs from 'fs';

function parseArgs(args: string[]): { level: number, text: string } {
  let level = 1;
  const textParts: string[] = [];
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (a === '-l' || a === '--level') {
      const next = args[i + 1];
      if (next && !next.startsWith('-')) {
        const parsed = parseInt(next, 10);
        if (!isNaN(parsed)) {
          level = parsed;
        }
        i++;
      }
    } else {
      textParts.push(a);
    }
  }
  const text = textParts.join(' ');
  return { level, text };
}

const leetMaps: Record<number, Record<string, string>> = {
  1: { 'a': '4', 'e': '3', 'i': '1', 'o': '0', 's': '5', 't': '7' },
  2: { 'A': '4', 'E': '3', 'I': '1', 'O': '0', 'S': '5', 'T': '7', 'b': '8', 'g': '9' },
  3: { 'A': '4', 'E': '3', 'I': '1', 'O': '0', 'S': '5', 'T': '7', 'B': '8', 'G': '9', 'Z': '2' }
};

function leetify(text: string, level: number): string {
  const combined: Record<string, string> = {};
  for (let l = 1; l <= level; l++) {
    const map = leetMaps[l];
    if (map) {
      for (const k in map) {
        combined[k] = map[k];
      }
    }
  }
  return text.split('').map(ch => combined[ch] ?? combined[ch.toLowerCase()] ?? ch).join('');
}

// Read input from stdin if piped
let stdinInput = '';
if (!process.stdin.isTTY) {
  stdinInput = fs.readFileSync(0, 'utf8').trim();
}

const args = process.argv.slice(2);
const { level, text } = parseArgs(args);
const finalText = text || stdinInput;

if (finalText) {
  console.log(leetify(finalText, level));
}

// Export for testing
export { leetify, parseArgs };
