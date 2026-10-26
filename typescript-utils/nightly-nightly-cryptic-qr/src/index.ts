#!/usr/bin/env node
import QRCode from 'qrcode-terminal';

export interface QROptions {
  border?: boolean;
}

/**
 * Generate an ASCII QR code for the given text.
 * If options.border is true, the QR code is wrapped in a post‑apocalypse styled border.
 */
export function generateAsciiQR(text: string, options: QROptions = {}): string {
  let qr = '';
  QRCode.generate(text, { small: true }, (qrcode) => {
    qr = qrcode;
  });
  if (options.border) {
    const lines = qr.split('\n');
    const width = Math.max(...lines.map(l => l.length));
    const top = '⛧' + '─'.repeat(width) + '⛧';
    const bottom = '⛧' + '─'.repeat(width) + '⛧';
    const bordered = lines.map(l => `⛧${l.padEnd(width)}⛧`).join('\n');
    return `${top}\n${bordered}\n${bottom}`;
  }
  return qr;
}

// CLI entry point
if (require.main === module) {
  const args = process.argv.slice(2);
  const text = args[0] ?? '';
  const border = args.includes('--border');
  if (!text) {
    console.error('Usage: nightly-cryptic-qr <text> [--border]');
    process.exit(1);
  }
  console.log(generateAsciiQR(text, { border }));
}
