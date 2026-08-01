#!/usr/bin/env node
import { createInterface } from 'readline';

export function shannonEntropy(str: string): number {
  if (!str) return 0;
  const freq: Record<string, number> = {};
  for (const ch of str) {
    freq[ch] = (freq[ch] ?? 0) + 1;
  }
  const len = str.length;
  let entropy = 0;
  for (const count of Object.values(freq)) {
    const p = count / len;
    entropy -= p * Math.log2(p);
  }
  return entropy;
}

export function rating(entropy: number): { emoji: string; level: string } {
  if (entropy <= 1.5) return { emoji: '🟢', level: 'Low' };
  if (entropy <= 3.0) return { emoji: '🟡', level: 'Medium' };
  return { emoji: '🔥', level: 'High' };
}

// CLI handling
async function main() {
  const args = process.argv.slice(2);
  let input = args.join(' ');
  if (!input) {
    // read from stdin
    const rl = createInterface({ input: process.stdin, terminal: false });
    for await (const line of rl) {
      input += line;
    }
    rl.close();
  }
  const entropy = shannonEntropy(input);
  const { emoji, level } = rating(entropy);
  console.log(`Entropy: ${entropy.toFixed(2)} bits/char`);
  console.log(`Rating: ${emoji} (${level})`);
}

if (require.main === module) {
  main();
}
