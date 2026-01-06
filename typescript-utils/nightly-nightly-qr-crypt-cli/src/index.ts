// src/index.ts

/**
 * Apply a Caesar‑cipher shift to a string.
 * Non‑alphabetic characters are left unchanged.
 */
function caesarShift(input: string, shift: number): string {
  const normalizedShift = ((shift % 26) + 26) % 26; // ensure 0‑25
  return input.replace(/[a-zA-Z]/g, (char) => {
    const base = char <= "Z" ? 65 : 97;
    const code = char.charCodeAt(0) - base;
    const shifted = (code + normalizedShift) % 26;
    return String.fromCharCode(shifted + base);
  });
}

/**
 * Generate a QR‑code‑style placeholder for the shifted text.
 * In a real implementation this could call a library like `qrcode-terminal`.
 */
export function generateQr(text: string, shift: number = 1): string {
  const shifted = caesarShift(text, shift);
  // Placeholder QR representation – deterministic and offline.
  return `QR:${shifted}`;
}

/**
 * Simple CLI entry point.
 *   node dist/index.js "some text" -s 2
 */
function parseArgs(args: string[]): { text: string; shift: number } {
  if (args.length === 0) {
    throw new Error("No input text provided.");
  }
  const text = args[0];
  let shift = 1;
  const sIndex = args.findIndex((a) => a === "-s" || a === "--shift");
  if (sIndex !== -1 && sIndex + 1 < args.length) {
    const parsed = parseInt(args[sIndex + 1], 10);
    if (!isNaN(parsed)) {
      shift = parsed;
    }
  }
  return { text, shift };
}

function main(argv: string[]): void {
  try {
    const { text, shift } = parseArgs(argv);
    const output = generateQr(text, shift);
    console.log(output);
  } catch (err) {
    console.error((err as Error).message);
    process.exit(1);
  }
}

if (require.main === module) {
  // Strip the first two entries (node executable and script path)
  main(process.argv.slice(2));
}
