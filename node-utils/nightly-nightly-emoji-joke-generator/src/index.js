#!/usr/bin/env node

const jokes = [
  "Why don't scientists trust atoms? Because they make up everything! 🤣",
  "I told my computer I needed a break, and it said 'No problem, I'll go to sleep.' 😴",
  "Why did the scarecrow win an award? Because he was outstanding in his field! 🌾"
];

function getJoke() {
  const idx = Math.floor(Math.random() * jokes.length);
  return jokes[idx];
}

if (require.main === module) {
  console.log(getJoke());
}

module.exports = { getJoke };
