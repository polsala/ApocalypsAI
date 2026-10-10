// nightly-emoji-decoder
// Decode emojis to letters A‑Z using a fixed mapping.

const fs = require('fs');

// Mapping of 26 distinct emojis to letters A‑Z.
const emojiMap = {
  '😀': 'A',
  '😃': 'B',
  '😄': 'C',
  '😁': 'D',
  '😆': 'E',
  '😅': 'F',
  '😂': 'G',
  '🤣': 'H',
  '😊': 'I',
  '😇': 'J',
  '🙂': 'K',
  '🙃': 'L',
  '😉': 'M',
  '😌': 'N',
  '😍': 'O',
  '🥰': 'P',
  '😘': 'Q',
  '😗': 'R',
  '😙': 'S',
  '😚': 'T',
  '😋': 'U',
  '😛': 'V',
  '😝': 'W',
  '😜': 'X',
  '🤪': 'Y',
  '🤩': 'Z'
};

// Retrieve input either from command‑line argument or stdin.
function getInput() {
  const args = process.argv.slice(2);
  if (args.length > 0) {
    // Join all arguments to support spaces inside a quoted string.
    return args.join(' ');
  }
  // No args – read from stdin synchronously.
  try {
    return fs.readFileSync(0, 'utf8'); // 0 = STDIN
  } catch (e) {
    return '';
  }
}

function decode(input) {
  // Remove line breaks and trim.
  const cleaned = input.replace(/\r?\n/g, '').trim();
  // Spread to correctly handle surrogate pairs (emoji are 2‑code‑unit chars).
  const chars = [...cleaned];
  const result = [];
  for (const ch of chars) {
    if (ch === ' ' || ch === '\t') {
      continue; // ignore whitespace
    }
    if (emojiMap[ch]) {
      result.push(emojiMap[ch]);
    } else {
      result.push('?'); // unknown symbol
    }
  }
  return result.join('');
}

const rawInput = getInput();
const decoded = decode(rawInput);
console.log(decoded);
