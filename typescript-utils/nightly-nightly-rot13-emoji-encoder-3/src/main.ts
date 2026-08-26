/*
 * nightly-rot13-emoji-encoder
 *
 * This module provides two exported functions:
 *   - rot13: classic ROT13 cipher
 *   - encodeToEmoji: ROT13 + per‑letter emoji mapping
 *
 * It also includes a tiny CLI that reads a string from the first argument
 * or from STDIN and prints the encoded result.
 */

export function rot13(input: string): string {
  return input.replace(/[a-zA-Z]/g, (c) => {
    const base = c <= "Z" ? 65 : 97;
    const code = ((c.charCodeAt(0) - base + 13) % 26) + base;
    return String.fromCharCode(code);
  });
}

const emojiMap: string[] = [
  "🅰️", // a
  "🅱️", // b
  "🌜", // c
  "🌛", // d
  "📧", // e
  "🎏", // f
  "🌀", // g
  "♓", // h
  "ℹ️", // i
  "🕹️", // j
  "🔑", // k
  "🛴", // l
  "〽️", // m
  "♑", // n
  "⚽", // o
  "🅿️", // p
  "🍳", // q
  "🌈", // r
  "💲", // s
  "✝️", // t
  "⛎", // u
  "✅", // v
  "🔱", // w
  "❎", // x
  "🪁", // y
  "⚡", // z
];

export function encodeToEmoji(input: string): string {
  const rot = rot13(input);
  return rot.replace(/[a-zA-Z]/g, (c) => {
    const lower = c.toLowerCase();
    const index = lower.charCodeAt(0) - 97; // 'a' => 0
    return emojiMap[index] ?? c;
  });
}

// ---------- CLI ----------
if (require.main === module) {
  const args = process.argv.slice(2);
  const readStdin = async (): Promise<string> => {
    return new Promise((resolve) => {
      let data = "";
      process.stdin.setEncoding("utf8");
      process.stdin.on("data", (chunk) => (data += chunk));
      process.stdin.on("end", () => resolve(data.trim()))
    });
  };

  (async () => {
    let input: string;
    if (args.length > 0) {
      input = args.join(" ");
    } else {
      input = await readStdin();
    }
    const output = encodeToEmoji(input);
    console.log(output);
  })();
}
