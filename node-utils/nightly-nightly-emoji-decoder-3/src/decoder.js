const emojiMap = {
  "😀": "A",
  "😁": "B",
  "😂": "C",
  "🤣": "D",
  "😃": "E",
  "😄": "F",
  "😅": "G",
  "😆": "H",
  "😉": "I",
  "😊": "J"
};

function decodeEmojis(input) {
  return [...input].map(ch => emojiMap[ch] || "?").join("");
}

module.exports = { decodeEmojis };
