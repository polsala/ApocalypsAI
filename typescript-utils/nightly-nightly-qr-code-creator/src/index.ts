#!/usr/bin/env node
import QRCode from 'qrcode-terminal';

function generateQRCode(text: string): string {
  let output = '';
  QRCode.generate(text, { small: true }, (qr) => {
    output = qr;
  });
  return output;
}

// CLI handling
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.error('Usage: qr-code <text>');
    process.exit(1);
  }
  const text = args.join(' ');
  const qr = generateQRCode(text);
  console.log(qr);
}

export { generateQRCode };
