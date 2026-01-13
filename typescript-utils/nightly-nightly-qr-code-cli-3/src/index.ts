#!/usr/bin/env node

export function generateQr(text: string): string {
  // Simple deterministic placeholder: each character becomes a block pattern.
  // For each char, we take its char code, mod 4, and map to a 2x2 block.
  const blockMap = [
    "ââ
ââ",
    "ââ
ââ",
    "ââ
ââ",
    "ââ
ââ"
  ];
  let rows: string[] = ["", ""];
  for (const ch of text) {
    const idx = ch.charCodeAt(0) % blockMap.length;
    const block = blockMap[idx].split("
");
    rows[0] += block[0];
    rows[1] += block[1];
  }
  return rows.join("
");
}

// CLI entry point
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.error("Usage: nightly-qr-code-cli <text>");
    process.exit(1);
  }
  const input = args.join(" ");
  console.log(generateQr(input));
}

