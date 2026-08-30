#!/usr/bin/env node
/**
 * nightly-qr-ansi-art
 * Generate simple QR‑like ASCII art from a string.
 */

export function generate(input: string): string {
  if (input.length === 0) {
    return "";
  }
  const rows = Array.from(input).map(char => {
    const code = char.charCodeAt(0);
    const binary = code.toString(2).padStart(8, "0");
    // map 1 -> █, 0 -> space
    return binary.split("").map(bit => (bit === "1" ? "█" : " ")).join("");
  });
  return rows.join("\n");
}

// CLI entry point
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.error("Usage: nightly-qr-ansi-art <text>");
    process.exit(1);
  }
  const text = args.join(" ");
  console.log(generate(text));
}
