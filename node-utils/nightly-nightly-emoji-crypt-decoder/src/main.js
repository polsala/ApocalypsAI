#!/usr/bin/env node

const fs = require('fs');

// Fixed emojiâtoâletter map
const EMOJI_MAP = {
  'ð':'A','ð':'B','ð':'C','ð':'D','ð':'E','ð':'F','ð':'G','ð':'H','ð¥':'I','ð':'J',
  'ð¥':'K','ð':'L','ð¥':'M','ð¥':'N','ð½':'O','ð¶ï¸':'P','ð§':'Q','ð§':'R','ð':'S','ð¥':'T',
  'ð':'U','ð¥':'V','ð§':'W','ð':'X','ð':'Y','ð¥©':'Z'
};

/**
 * Decode a string of emojis into letters. Unknown emojis become '?'.
 * @param {string} input â Emoji sequence
 * @returns {string} Decoded text
 */
function decode(input) {
  // Array.from correctly splits surrogateâpair emojis
  const chars = Array.from(input);
  return chars.map(ch => EMOJI_MAP[ch] || '?').join('');
}

// CLI handling â when executed directly
if (require.main === module) {
  const args = process.argv.slice(2);
  let input = '' ;
  if (args.length > 0) {
    input = args[0];
  } else {
    // Read from stdin (synchronous for simplicity)
    input = fs.readFileSync(0, 'utf8').trim();
  }
  const output = decode(input);
  console.log(output);
}

module.exports = { decode };

