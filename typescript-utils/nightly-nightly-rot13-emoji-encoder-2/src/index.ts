export function rot13(input: string): string {
  return input.replace(/[a-zA-Z]/g, (c) => {
    const base = c <= "Z" ? 65 : 97;
    return String.fromCharCode(((c.charCodeAt(0) - base + 13) % 26) + base);
  });
}
\nconst emojiMap: string[] = [
  "😀", "😁", "😂", "🤣", "😃", "😄", "😅", "😆", "😉", "😊",
  "😋", "😎", "😍", "😘", "🥰", "😗", "😙", "😚", "🙂", "🤗",
  "🤩", "🤔", "🤨", "😐", "😑", "😶"
];
\nexport function toEmoji(input: string): string {
  return input.replace(/[a-z]/gi, (ch) => {
    const lower = ch.toLowerCase();
    const idx = lower.charCodeAt(0) - 97; // 'a' => 0
    return emojiMap[idx] ?? ch;
  });
}
\n// CLI entry point
if (require.main === module) {
  const args = process.argv.slice(2);
  const raw = args.length ? args.join(" ") : "";
  if (!raw) {
    console.error("Usage: node src/index.js <text>");
    process.exit(1);
  }
  const transformed = toEmoji(rot13(raw));
  console.log(transformed);
}
