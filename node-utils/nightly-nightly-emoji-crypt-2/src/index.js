// nightly-emoji-crypt – Node.js implementation
// -------------------------------------------------
// This file provides two exported functions: encode(text) and decode(emojiStr).
// It also implements a tiny CLI that reads process.argv.

const CHAR_TO_EMOJI = {
  a: "🐶",
  b: "🐱",
  c: "🐭",
  d: "🐹",
  e: "🐰",
  f: "🦊",
  g: "🐻",
  h: "🐼",
  i: "🐨",
  j: "🐯",
  k: "🦁",
  l: "🐮",
  m: "🐷",
  n: "🐸",
  o: "🐵",
  p: "🐔",
  q: "🐧",
  r: "🐦",
  s: "🐤",
  t: "🦆",
  u: "🦅",
  v: "🦉",
  w: "🦇",
  x: "🐺",
  y: "🐗",
  z: "🐴",
  "0": "0️⃣",
  "1": "1️⃣",
  "2": "2️⃣",
  "3": "3️⃣",
  "4": "4️⃣",
  "5": "5️⃣",
  "6": "6️⃣",
  "7": "7️⃣",
  "8": "8️⃣",
  "9": "9️⃣",
  " ": "🌞"
};

// Build reverse map for decoding
const EMOJI_TO_CHAR = Object.entries(CHAR_TO_EMOJI).reduce((acc, [ch, emoji]) => {
  acc[emoji] = ch;
  return acc;
}, {});

/**
 * Encode a plain‑text string into emojis.
 * @param {string} text
 * @returns {string}
 */
function encode(text) {
  return Array.from(text)
    .map(ch => {
      const lower = ch.toLowerCase();
      return CHAR_TO_EMOJI[lower] || ch; // pass through unknown chars
    })
    .join("");
}

/**
 * Decode an emoji string back to plain text.
 * @param {string} emojiStr
 * @returns {string}
 */
function decode(emojiStr) {
  // The emojis are single Unicode code points (or surrogate pairs) that are not ambiguous.
  // We'll iterate over the string and try to match the longest possible emoji from the map.
  const emojis = Object.keys(EMOJI_TO_CHAR);
  let result = "";
  let i = 0;
  while (i < emojiStr.length) {
    let matched = false;
    // Try to match any emoji at the current position (most emojis are 2 code units long)
    for (const emoji of emojis) {
      if (emojiStr.startsWith(emoji, i)) {
        result += EMOJI_TO_CHAR[emoji];
        i += emoji.length;
        matched = true;
        break;
      }
    }
    if (!matched) {
      // No known emoji – keep the original character
      result += emojiStr[i];
      i += 1;
    }
  }
  return result;
}

// CLI handling
if (require.main === module) {
  const [, , action, ...rest] = process.argv;
  if (!action || !["encode", "decode"].includes(action)) {
    console.error("Usage: node src/index.js <encode|decode> <text>");
    process.exit(1);
  }
  const input = rest.join(" ");
  if (action === "encode") {
    console.log(encode(input));
  } else {
    console.log(decode(input));
  }
}

module.exports = { encode, decode };
