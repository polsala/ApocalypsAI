#!/usr/bin/env node
import { readFileSync } from "fs";

function generateQrAscii(text: string): string {
  let top = "";
  let bottom = "";
  for (const ch of text) {
    const code = ch.charCodeAt(0) & 0b1111; // lowest 4 bits
    const tl = (code & 0b0001) ? "#" : " ";
    const tr = (code & 0b0010) ? "#" : " ";
    const bl = (code & 0b0100) ? "#" : " ";
    const br = (code & 0b1000) ? "#" : " ";
    top += tl + tr;
    bottom += bl + br;
  }
  return top + "\n" + bottom;
}

// CLI handling
if (require.main === module) {
  const args = process.argv.slice(2);
  let input = "";
  if (args.length > 0) {
    input = args.join(" ");
  } else {
    // read from stdin
    try {
      input = readFileSync(0, "utf8").trim();
    } catch (_) {
      console.error("No input provided.");
      process.exit(1);
    }
  }
  console.log(generateQrAscii(input));
}

// Export for tests
export { generateQrAscii };
