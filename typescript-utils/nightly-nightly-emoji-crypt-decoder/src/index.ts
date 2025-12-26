// Emoji substitution cipher
const encodeMap: Record<string, string> = {
  A: "🅰️",
  B: "🅱️",
  C: "🌜",
  D: "🌛",
  E: "📧",
  F: "🎏",
  G: "🌀",
  H: "♓",
  I: "ℹ️",
  J: "🕹️",
  K: "🔑",
  L: "🦁",
  M: "〽️",
  N: "♑",
  O: "⚽",
  P: "🅿️",
  Q: "🍳",
  R: "🌈",
  S: "💲",
  T: "✝️",
  U: "⛎",
  V: "✅",
  W: "🔱",
  X: "❎",
  Y: "🪁",
  Z: "⚡"
};

const decodeMap: Record<string, string> = Object.entries(encodeMap).reduce(
  (acc, [k, v]) => {
    acc[v] = k;
    return acc;
  },
  {} as Record<string, string>
);

/**
 * Encode a plain‑text string into emojis.
 * Spaces become '/' to keep word boundaries.
 */
export function encode(text: string): string {
  return text
    .toUpperCase()
    .split("")
    .map(ch => {
      if (ch === " ") return "/";
      return encodeMap[ch] ?? ch;
    })
    .join("");
}

/**
 * Decode an emoji string back to plain text.
 * '/' is converted back to a space.
 */
export function decode(emojis: string): string {
  let result = "";
  for (let i = 0; i < emojis.length; ) {
    const slice = emojis.slice(i, i + 2);
    if (slice === "/") {
      result += " ";
      i += 1;
      continue;
    }
    if (decodeMap[slice]) {
      result += decodeMap[slice];
      i += 2;
    } else {
      // Unknown character, keep as‑is (advances by 2 to avoid infinite loop)
      result += slice;
      i += 2;
    }
  }
  return result;
}

// Simple CLI
if (require.main === module) {
  const [, , command, ...rest] = process.argv;
  const input = rest.join(" ");
  if (command === "encode") {
    console.log(encode(input));
  } else if (command === "decode") {
    console.log(decode(input));
  } else {
    console.error("Usage: nightly-emoji-crypt-decoder <encode|decode> <text>");
    process.exit(1);
  }
}
