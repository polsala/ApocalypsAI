#!/usr/bin/env ts-node

/**
 * Nightly Cryptic QR Generator
 * Generates a simple ASCII‑style QR‑like code from a short string.
 */

const symbols = ["##","@@","..","**"] as const;

type Symbol = typeof symbols[number];

function charToBlock(ch: string): [Symbol, Symbol] {
  const code = ch.charCodeAt(0);
  const top = symbols[code % symbols.length];
  const bottom = symbols[(code + 1) % symbols.length];
  return [top, bottom];
}

export function generateQR(text: string): string {
  let topRow = "";
  let bottomRow = "";
  for (const ch of text) {
    const [top, bottom] = charToBlock(ch);
    topRow += top;
    bottomRow += bottom;
  }
  return `${topRow}\n${bottomRow}`;
}

// CLI handling
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.error("Usage: ts-node src/main.ts <text>");
    process.exit(1);
  }
  const input = args.join(" ");
  console.log(generateQR(input));
}
