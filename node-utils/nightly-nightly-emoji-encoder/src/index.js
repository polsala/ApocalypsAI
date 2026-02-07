// nightly-emoji-encoder\n// Encode and decode strings to a whimsical emoji alphabet.\n\nconst base64Chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
\n// 64‑unique emojis (simple, no variation selectors)\nconst emojiAlphabet = [
  "😀","😁","😂","🤣","😃","😄","😅","😆",
  "😉","😊","😋","😎","😍","😘","🥰","😗",
  "😙","😚","🙂","🤗","🤩","🤔","🤨","😐",
  "😑","😶","🙄","😏","😣","😥","😮","🤐",
  "😯","😪","😫","🥱","😴","🤤","😷","🤒",
  "🤕","🤑","🤠","😈","👿","👹","👺","🤡",
  "💩","👻","💀","👽","🤖","🎃","😺","😸",
  "😹","😻","😼","😽","🙀","😿","😾","🐶"
];
\n/**\n * Encode a UTF‑8 string into an emoji sequence.\n * @param {string} input\n * @returns {string} Emoji string (padding '=' characters are preserved)\n */
function encode(input) {
  const base64 = Buffer.from(input, "utf8").toString("base64");
  let result = "";
  for (const ch of base64) {
    if (ch === "=") {
      result += "="; // preserve padding
    } else {
      const idx = base64Chars.indexOf(ch);
      if (idx === -1) throw new Error(`Invalid Base64 character: ${ch}`);
      result += emojiAlphabet[idx];
    }
  }
  return result;
}
\n/**\n * Decode an emoji sequence back to the original UTF‑8 string.\n * @param {string} emojiStr\n * @returns {string} Decoded text\n */
function decode(emojiStr) {
  let base64 = "";
  for (const ch of emojiStr) {
    if (ch === "=") {
      base64 += "=";
    } else {
      const idx = emojiAlphabet.indexOf(ch);
      if (idx === -1) throw new Error(`Invalid emoji character: ${ch}`);
      base64 += base64Chars[idx];
    }
  }
  return Buffer.from(base64, "base64").toString("utf8");
}
\n// CLI handling\nif (require.main === module) {
  const [, , command, argument] = process.argv;
  if (!command || !argument) {
    console.error("Usage: node src/index.js <encode|decode> <text>");
    process.exit(1);
  }
  try {
    if (command === "encode") {
      console.log(encode(argument));
    } else if (command === "decode") {
      console.log(decode(argument));
    } else {
      console.error("Unknown command. Use 'encode' or 'decode'.");
      process.exit(1);
    }
  } catch (err) {
    console.error("Error:", err.message);
    process.exit(1);
  }
}
\nmodule.exports = { encode, decode };
