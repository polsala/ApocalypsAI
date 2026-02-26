const emojiMap = [
  '🐶','🐱','🐭','🐹','🐰','🦊','🐻','🐼','🐨','🐯','🦁','🐮','🐷','🐸','🐵','🐔','🐧','🐦','🐤','🐣','🐥','🐺','🐗','🐴','🐝','🐛'
];

function encode(text) {
  return text.toUpperCase().split('').map(ch => {
    const idx = ch.charCodeAt(0) - 65;
    return idx >= 0 && idx < 26 ? emojiMap[idx] : ch;
  }).join('');
}

function decode(emojis) {
  const chars = Array.from(emojis);
  return chars.map(c => {
    const idx = emojiMap.indexOf(c);
    return idx !== -1 ? String.fromCharCode(65 + idx) : '?';
  }).join('');
}

if (require.main === module) {
  const [, , cmd, input] = process.argv;
  if (!cmd || !input) {
    console.error('Usage: node index.js <encode|decode> <text>');
    process.exit(1);
  }
  if (cmd === 'encode') {
    console.log(encode(input));
  } else if (cmd === 'decode') {
    console.log(decode(input));
  } else {
    console.error('Unknown command');
    process.exit(1);
  }
}

module.exports = { encode, decode };
