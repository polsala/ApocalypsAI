#!/usr/bin/env node
const CODE_MAP = {
  A: 'Ash', B: 'Bunker', C: 'Cinder', D: 'Dust', E: 'Ember',
  F: 'Feral', G: 'Grit', H: 'Hollow', I: 'Irradiated', J: 'Junk',
  K: 'Kite', L: 'Loom', M: 'Mire', N: 'Nexus', O: 'Obsidian',
  P: 'Purge', Q: 'Quake', R: 'Rubble', S: 'Scavenge', T: 'Toxic',
  U: 'Utopia', V: 'Vortex', W: 'Wasteland', X: 'Xenon', Y: 'Yield', Z: 'Zephyr',
  '0': 'Zero', '1': 'One', '2': 'Two', '3': 'Three', '4': 'Four',
  '5': 'Five', '6': 'Six', '7': 'Seven', '8': 'Eight', '9': 'Nine'
};

function translate(text) {
  return text
    .toUpperCase()
    .split('')
    .filter(ch => CODE_MAP[ch] !== undefined)
    .map(ch => CODE_MAP[ch])
    .join(' ');
}

// CLI handling
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.error('Usage: node src/index.js <text>');
    process.exit(1);
  }
  const input = args.join(' ');
  console.log(translate(input));
}

module.exports = { translate };
