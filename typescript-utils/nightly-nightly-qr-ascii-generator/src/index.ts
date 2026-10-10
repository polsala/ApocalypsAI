/**
 * nightly-qr-ascii-generator
 *
 * Convert a string into a deterministic QR‑like ASCII art block.
 * Each character is mapped to a 2×2 block:
 *   - Even Unicode code point → filled block ("██")
 *   - Odd Unicode code point  → empty block ("  ")
 *
 * The blocks are concatenated horizontally, producing two rows of output.
 */

/**
 * Generate the ASCII art for the given text.
 * @param text Input string to encode.
 * @returns Two‑line string containing the ASCII representation.
 */
export function generateAsciiArt(text: string): string {
  // Guard against empty input
  if (text.length === 0) {
    return "";
  }

  let topRow = "";
  let bottomRow = "";

  for (const char of text) {
    const code = char.codePointAt(0) ?? 0;
    const block = code % 2 === 0 ? ["██", "██"] : ["  ", "  "];
    topRow += block[0];
    bottomRow += block[1];
  }

  return `${topRow}\n${bottomRow}`;
}

// CLI handling – only executed when run directly
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.error("Usage: ts-node src/index.ts <text-to-encode>");
    process.exit(1);
  }
  const input = args.join(" ");
  console.log(generateAsciiArt(input));
}
