const emojis = ["ð","ð","ð","ð¥","ð§","ð","ð²","ð§©","â¡","ðª"];

/**
 * Apply ROT13 to a string. Only alphabetic characters are shifted; other characters are left untouched.
 */
export function rot13(input: string): string {
  return input.replace(/[a-zA-Z]/g, (c) => {
    const base = c <= "Z" ? 65 : 97;
    const code = c.charCodeAt(0) - base;
    const rotated = (code + 13) % 26;
    return String.fromCharCode(rotated + base);
  });
}

/**
 * Encode a string with ROT13 and prepend a deterministic emoji to each character.
 * Emoji selection is based on the Unicode code point of the ROT13 character modulo the emoji list length.
 */
export function encodeWithEmoji(input: string): string {
  const transformed = rot13(input);
  let result = "";
  for (const ch of transformed) {
    const emoji = emojis[ch.charCodeAt(0) % emojis.length];
    result += `${emoji}${ch}`;
  }
  return result;
}

// CLI handling
if (require.main === module) {
  const args = process.argv.slice(2);
  const readStdin = async (): Promise<string> => {
    return new Promise((resolve) => {
      let data = "";
      process.stdin.setEncoding("utf8");
      process.stdin.on("data", (chunk) => (data += chunk));
      process.stdin.on("end", () => resolve(data.trim()));
    });
  };

  (async () => {
    let input: string;
    if (args.length > 0) {
      input = args.join(" ");
    } else {
      input = await readStdin();
    }
    if (input.length === 0) {
      console.error("No input provided. Pass a string as an argument or pipe it via STDIN.");
      process.exit(1);
    }
    console.log(encodeWithEmoji(input));
  })();
}

