#!/usr/bin/env node
import { readFileSync } from 'fs';
import { renderBarChart } from './graph';

function parseNumbers(input: string): number[] {
  return input
    .trim()
    .split(/[\s,]+/)
    .filter(Boolean)
    .map((s) => Number(s))
    .filter((n) => !isNaN(n) && n >= 0);
}

function main() {
  const args = process.argv.slice(2);
  let data = '';
  if (args.length > 0 && args[0] !== '-') {
    try {
      data = readFileSync(args[0], 'utf8');
    } catch {
      console.error(`Cannot read file: ${args[0]}`);
      process.exit(1);
    }
  } else {
    data = readFileSync(0, 'utf8'); // STDIN
  }
  const values = parseNumbers(data);
  if (values.length === 0) {
    console.error('No valid numbers provided.');
    process.exit(1);
  }
  const color = args.includes('--color');
  const chart = renderBarChart(values, { color });
  console.log(chart);
}

if (require.main === module) {
  main();
}
