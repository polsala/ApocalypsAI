#!/usr/bin/env node

const qrcode = require('qrcode-terminal');

/**
 * Generate an ASCII QR code for the given text.
 * @param {string} text - Text to encode.
 * @returns {Promise<string>} - Promise that resolves to the ASCII QR code.
 */
function generateQR(text) {
  return new Promise((resolve) => {
    qrcode.generate(text, { small: true }, (qr) => {
      resolve(qr);
    });
  });
}

// If executed directly, act as a CLI.
if (require.main === module) {
  const input = process.argv.slice(2).join(' ');
  if (!input) {
    console.error('Usage: qr-ink <text>');
    process.exit(1);
  }
  generateQR(input).then((qr) => console.log(qr));
}

module.exports = { generateQR };
