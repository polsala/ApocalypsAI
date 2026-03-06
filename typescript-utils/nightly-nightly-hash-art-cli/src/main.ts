import { createHash } from "crypto";
import { argv, exit } from "process";

/**
 * Mapping from hexadecimal digit to a Unicode block character.
 * This provides a compact visual representation while keeping the output
 * deterministic and easily reversible for debugging.
 */
const HEX_TO_BLOCK: Record<string, string> = {
  "0": "▁",
  "1": "▂",
  "2": "▃",
  "3": "▄",
  "4": "▅",
  "5": "▆",
  "6": "▇",
  "7": "█",
  "8": "▏",
  "9": "▎",
  a: "▍",
  b: "▌",
  c: "▋",
  d: "▊",
  e: "▉",
  f: "■",
};

/**
 * Compute the SHA‑256 hash of `input` and convert each hex digit to its
 * corresponding block character.
 */
export function hashToArt(input: string): string {
  const hash = createHash("sha256").update(input, "utf8").digest("hex");
  let art = "";
  for (const ch of hash) {
    const block = HEX_TO_BLOCK[ch];
    // Fallback to the original character if mapping is missing (should never happen)
    art += block ?? ch;
  }
  return art;
}

// CLI handling – when the file is executed directly
if (require.main === module) {
  const args = argv.slice(2);
  if (args.length === 0) {
    console.error("Usage: node main.js <string-to‑hash>");
    exit(1);
  }
  const input = args.join(" ");
  console.log(hashToArt(input));
}
