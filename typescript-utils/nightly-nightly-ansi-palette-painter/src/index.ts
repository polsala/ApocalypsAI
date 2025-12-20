#!/usr/bin/env node
import { argv } from 'process';

const BASIC_COLORS: Record<string, number> = {
  black: 30,
  red: 31,
  green: 32,
  yellow: 33,
  blue: 34,
  magenta: 35,
  cyan: 36,
  white: 37,
};

export function getAnsiEscape(color: string): string {
  const lower = color.toLowerCase();
  if (lower in BASIC_COLORS) {
    return `\x1b[${BASIC_COLORS[lower]}m`;
  }
  const hex = lower.startsWith('#') ? lower.slice(1) : lower;
  if (/^[0-9a-f]{6}$/.test(hex)) {
    const r = parseInt(hex.slice(0, 2), 16);
    const g = parseInt(hex.slice(2, 4), 16);
    const b = parseInt(hex.slice(4, 6), 16);
    return `\x1b[38;2;${r};${g};${b}m`;
  }
  throw new Error(`Unsupported color: ${color}`);
}

export function paintSample(color: string): string {
  const esc = getAnsiEscape(color);
  const reset = '\x1b[0m';
  return `${esc}█${reset} ${esc}${color}${reset}`;
}

// CLI entry
if (require.main === module) {
  const input = argv[2];
  if (!input) {
    console.error('Usage: ansi-palette-painter <color>');
    process.exit(1);
  }
  try {
    console.log(paintSample(input));
  } catch (e) {
    console.error((e as Error).message);
    process.exit(1);
  }
}
