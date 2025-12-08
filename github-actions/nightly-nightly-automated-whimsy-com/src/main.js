const quotes = [
  "May your code compile and your tests pass! 🧪",
  "Stay rad, hacker! 🚀",
  "Debugging is like being the detective in a crime movie where you are also the criminal. 🕵️",
  "The cake is a lie... but the muffins are real. 🧁",
  "Optimism is an occupational hazard when you're doing anything real. 🛠️"
];

const emojis = ["✨", "🌈", "👾", "🦄", "🎉"];

const randomItem = (arr) => arr[Math.floor(Math.random() * arr.length)];

console.log(`${randomItem(emojis)} | ${randomItem(quotes)}`);
