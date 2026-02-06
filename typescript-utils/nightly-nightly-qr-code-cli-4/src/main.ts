#!/usr/bin/env node
import * as QRCode from 'qrcode';

/**
 * Generate a terminal‑friendly QR code for the given text.
 * @param text - The input string to encode.
 * @returns A promise that resolves to the QR code string.
 */
export async function generateQRCode(text: string): Promise<string> {
  // Use QRCode.toString with type 'terminal' for ASCII output
  return QRCode.toString(text, { type: 'terminal' });
}

/**
 * CLI entry point.
 */
async function main() {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.error('Usage: nightly-qr-code-cli <text>');
    process.exit(1);
  }
  const text = args.join(' ');
  try {
    const qr = await generateQRCode(text);
    console.log(qr);
  } catch (err) {
    console.error('Failed to generate QR code:', err);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}
