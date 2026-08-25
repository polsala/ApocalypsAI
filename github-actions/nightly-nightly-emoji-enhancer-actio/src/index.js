const core = require('./core');

function getRandomEmoji(seed) {
  const emojis = ['😀','🚀','🌟','🔥','💧','🧩','🦄','🎲','📚','⚡'];
  const idx = Math.abs(seed) % emojis.length;
  return emojis[idx];
}

function run() {
  const text = core.getInput('text');
  const seedInput = core.getInput('seed');
  const seed = seedInput ? parseInt(seedInput, 10) : Date.now();
  const emoji = getRandomEmoji(seed);
  const enhanced = `${emoji} ${text}`;
  core.setOutput('enhanced_text', enhanced);
}

run();
