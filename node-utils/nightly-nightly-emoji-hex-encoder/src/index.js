#!/usr/bin/env node

const emojis = ['😀','😁','😂','🤣','😃','😄','😅','😆','😉','😊','😋','😎','😍','😘','🥰','🤩'];
const hexToEmoji = {};
const emojiToHex = {};
'0123456789abcdef'.split('').forEach((h, i) => {
  hexToEmoji[h] = emojis[i];
  emojiToHex[emojis[i]] = h;
});

function encode(str) {
  const buf = Buffer.from(str, 'utf8');
  const hex = buf.toString('hex');
  let result = '';
  for (const ch of hex) {
    result += hexToEmoji[ch];
  }
  return result;
}

function decode(emojiStr) {
  let hex = '';
  for (const char of [...emojiStr]) {
    const h = emojiToHex[char];
    if (h === undefined) {
      throw new Error('Invalid emoji in input');
    }
    hex += h;
  }
  return Buffer.from(hex, 'hex').toString('utf8');
}

function main() {
  const [,, cmd, ...args] = process.argv;
  if (!cmd || (cmd !== 'encode' && cmd !== 'decode')) {
    console.error('Usage: node src/index.js <encode|decode> <string>');
    process.exit(1);
  }
  const input = args.join(' ');
  try {
    const output = cmd === 'encode' ? encode(input) : decode(input);
    console.log(output);
  } catch (e) {
    console.error('Error:', e.message);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { encode, decode };
