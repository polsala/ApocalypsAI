#!/usr/bin/env node

const ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
const SHIFT = 5;

function shiftChar(ch, shift) {
  const idx = ALPHABET.indexOf(ch);
  if (idx === -1) return ch;
  return ALPHABET[(idx + shift + ALPHABET.length) % ALPHABET.length];
}

function encode(text) {
  return text.toUpperCase().split('').map(c => shiftChar(c, SHIFT)).join('');
}

function decode(text) {
  return text.toUpperCase().split('').map(c => shiftChar(c, -SHIFT)).join('');
}

// CLI handling
if (require.main === module) {
  const [,, command, ...rest] = process.argv;
  const input = rest.join(' ');
  if (!command || !input) {
    console.error('Usage: node src/main.js <encode|decode> <text>');
    process.exit(1);
  }
  if (command === 'encode') {
    console.log(encode(input));
  } else if (command === 'decode') {
    console.log(decode(input));
  } else {
    console.error('Unknown command:', command);
    process.exit(1);
  }
}

module.exports = { encode, decode };
