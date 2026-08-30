#!/usr/bin/env node

const dict = {
  "🌧️": "rain",
  "☢️": "radiation",
  "🧟": "zombie",
  "🪦": "grave",
  "🔥": "fire",
  "💀": "death",
  "⚡": "electric",
  "🌪️": "storm",
  "🛠️": "repair",
  "🚧": "construction"
};

function decode(input) {
  // Decode the input string by matching the longest possible emoji keys.
  const emojis = Object.keys(dict).sort((a, b) => b.length - a.length);
  let result = [];
  let i = 0;
  while (i < input.length) {
    let matched = false;
    for (const emoji of emojis) {
      if (input.startsWith(emoji, i)) {
        result.push(dict[emoji]);
        i += emoji.length;
        matched = true;
        break;
      }
    }
    if (!matched) {
      // Unknown character – represent as a placeholder.
      result.push("?");
      i += 1;
    }
  }
  return result.join(" ");
}

function main() {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.error("Usage: node src/main.js <emoji-string>");
    process.exit(1);
  }
  const input = args[0];
  console.log(decode(input));
}

if (require.main === module) {
  main();
}

module.exports = { decode };
