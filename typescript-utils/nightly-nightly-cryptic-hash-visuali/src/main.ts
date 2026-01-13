#!/usr/bin/env node

import { visualizeHash } from './hashVisualizer';

function main(): void {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.error('Usage: nightly-cryptic-hash-visualizer <string>');
    process.exit(1);
  }
  const input = args.join(' ');
  console.log(visualizeHash(input));
}

main();

