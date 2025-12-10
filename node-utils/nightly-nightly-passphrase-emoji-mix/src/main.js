#!/usr/bin/env node
const crypto = require('crypto');

const WORDS = [
  'sunny','river','mountain','coffee','galaxy','tiger','whisper','shadow',
  'crystal','ember','storm','pixel','orbit','nova','cobalt','zen',
  'echo','flare','breeze','lunar','saffron','cactus','glimmer','zen'
];

const EMOJIS = ['🌟','🚀','🔥','💧','🧩','🦄','⚡','🍀','🎲','🪐','🧭','🕹️','📚','🎧','🛸','🧪','🪁','🧭'];

function getRandomInt(max) {
  const fake = process.env.FAKE_RANDOM;
  if (fake) {
    const parts = fake.split(',').map(s => parseInt(s, 10));
    const val = parts.shift();
    process.env.FAKE_RANDOM = parts.join(',');
    return val % max;
  }
  return crypto.randomInt(max);
}

function pickRandom(arr) {
  const idx = getRandomInt(arr.length);
  return arr[idx];
}

function generatePassphrase() {
  const words = [];
  for (let i = 0; i < 4; i++) {
    words.push(pickRandom(WORDS));
  }
  const emojis = [];
  for (let i = 0; i < 2; i++) {
    emojis.push(pickRandom(EMOJIS));
  }
  return words.join(' ') + ' ' + emojis.join('');
}

if (require.main === module) {
  console.log(generatePassphrase());
}

module.exports = { generatePassphrase, getRandomInt, pickRandom };
