import crypto from "crypto";

const mapping: Record<string, string> = {
  "0": "  ",
  "1": "ââ",
  "2": "ââ",
  "3": "ââ",
  "4": "ââ",
  "5": "ââ",
  "6": "ââ",
  "7": "ââ",
  "8": "ââ",
  "9": "ââ",
  "a": "ââ",
  "b": "ââ",
  "c": "ââ",
  "d": "ââ",
  "e": "ââ",
  "f": "ââ"
};

/**
 * Convert a string into deterministic ASCII block art.
 * @param text Input string to be transformed.
 * @returns Multiline string containing the art.
 */
export function hashArt(text: string): string {
  const hash = crypto.createHash("sha256").update(text).digest("hex");
  const patterns = hash.split("").map(ch => mapping[ch]);
  const lines: string[] = [];
  for (let i = 0; i < patterns.length; i += 8) {
    lines.push(patterns.slice(i, i + 8).join(""));
  }
  return lines.join("
");
}

// CLI handling â executed when run directly
if (require.main === module) {
  const input = process.argv[2] ?? "";
  if (!input) {
    console.error("Usage: node main.js <text>");
    process.exit(1);
  }
  console.log(hashArt(input));
}

