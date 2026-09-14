#!/usr/bin/env node

/**
 * nightly-emoji-encoder-cli
 *
 * Encode and decode strings to a whimsical emoji cipher.
 */

const encodeMap: Record<string, string> = {
  a: "🅰️",
  b: "🅱️",
  c: "🌜",
  d: "🌛",
  e: "📧",
  f: "🎏",
  g: "🌀",
  h: "♓",
  i: "ℹ️",
  j: "🗾",
  k: "🔑",
  l: "👢",
  m: "〽️",
  n: "♑",
  o: "⚽",
  p: "🅿️",
  q: "🇶",
  r: "🌱",
  s: "💲",
  t: "✝️",
  u: "⛎",
  v: "✅",
  w: "🔱",
  x: "❎",
  y: "☯️",
  z: "⚡",
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
  " ": "   " // three spaces for visual separation
};

// Build reverse map for decoding
const decodeMap: Record<string, string> = Object.entries(encodeMap).reduce((acc, [k, v]) => {
  acc[v] = k;
  return acc;
}, {} as Record<string, string>);

/** Encode plain text to emojis */
export function encode(input: string): string {
  return input
    .toLowerCase()
    .split("")
    .map(ch => encodeMap[ch] ?? ch)
    .join("");
}

/** Decode emoji string back to plain text */
export function decode(input: string): string {
  // The decoder works by scanning the input and matching the longest possible emoji token.
  // Since our mapping uses distinct Unicode sequences, a simple replace works.
  let output = input;
  // Sort keys by length descending to avoid partial replacements.
  const emojis = Object.keys(decodeMap).sort((a, b) => b.length - a.length);
  for (const emoji of emojis) {
    const plain = decodeMap[emoji];
    const regex = new RegExp(emoji, "g");
    output = output.replace(regex, plain);
  }
  return output;
}

/** CLI entry point */
function main() {
  const args = process.argv.slice(2);
  if (args.length < 2) {
    console.error("Usage: nemoji <encode|decode> <text>");
    process.exit(1);
  }
  const [command, ...rest] = args;
  const text = rest.join(" ");
  if (command === "encode") {
    console.log(encode(text));
  } else if (command === "decode") {
    console.log(decode(text));
  } else {
    console.error(`Unknown command: ${command}`);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}
