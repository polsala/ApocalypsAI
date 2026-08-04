#!/usr/bin/env node
import process from 'process';

const leetMap = {
  a: '4', A: '4',
  e: '3', E: '3',
  i: '1', I: '1',
  o: '0', O: '0',
  s: '5', S: '5',
  t: '7', T: '7',
  b: '8', B: '8',
  g: '9', G: '9'
};

/**
 * Convert text to leet‑speak and optionally add static noise.
 * @param {string} text - Input text.
 * @param {{noise?:boolean}} [options] - Configuration object.
 * @returns {string} Stylized text.
 */
export function stylize(text, options = { noise: true }) {
  const base = text.split('').map(ch => leetMap[ch] || ch).join('');
  if (!options.noise) return base;
  const staticChars = ['~', '*', '^', '`'];
  const words = base.split(' ');
  const noisy = words.map((w, i) => {
    if (i === words.length - 1) return w;
    const rand = staticChars[Math.floor(Math.random() * staticChars.length)];
    return w + rand;
  }).join(' ');
  return noisy;
}

// CLI execution block
if (import.meta.url === `file://${process.argv[1]}`) {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.error('Usage: apocstylize <text>');
    process.exit(1);
  }
  const text = args.join(' ');
  console.log(stylize(text));
}
