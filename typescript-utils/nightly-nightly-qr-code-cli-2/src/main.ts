#!/usr/bin/env node
import * as qrcode from 'qrcode-terminal';

export interface QROptions {
  small?: boolean;
}

/**
 * Generate a QR code string for the given text.
 * @param text - Text to encode.
 * @param options - Optional rendering options.
 * @returns QR code as a string.
 */
export function generateQRCode(text: string, options?: QROptions): string {
  let result = '';
  qrcode.generate(text, { small: options?.small ?? false }, (qr) => {
    result = qr;
  });
  return result;
}

// CLI entry point
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.log('Usage: npx ts-node src/main.ts <text> [--small]');
    process.exit(1);
  }
  const text = args[0];
  const small = args.includes('--small');
  const qr = generateQRCode(text, { small });
  console.log(qr);
}
