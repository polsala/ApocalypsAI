const fs = require('fs');

/**
 * Convert a single character to an 8‑pixel row using █ for 1 and space for 0.
 * @param {string} ch Single character
 * @returns {string} 8‑character string of █ and spaces
 */
function charToRow(ch) {
  const code = ch.charCodeAt(0);
  const binary = code.toString(2).padStart(8, '0');
  return binary.split('').map(bit => (bit === '1' ? '█' : ' ')).join('');
}

/**
 * Generate an ASCII QR‑like representation for the given text.
 * Each character becomes one row of 8 pixels.
 * @param {string} text Input string
 * @returns {string} Multi‑line ASCII art
 */
function generateQR(text) {
  if (typeof text !== 'string') {
    throw new TypeError('Input must be a string');
  }
  return text.split('').map(charToRow).join('\n');
}

// Export for use in other modules / tests
module.exports = { generateQR };

// CLI handling – when the file is executed directly
if (require.main === module) {
  const input = process.argv[2] || '';
  if (!input) {
    console.error('Usage: node src/index.js <text>');
    process.exit(1);
  }
  const output = generateQR(input);
  console.log(output);
}
