const { encode } = require('../src/index');
const assert = require('assert');

// Mock rationale: simple deterministic cases, no external resources.
const cases = [
  { input: 'ab c', expected: 'Ashen Bunker / Cinder' },
  { input: 'Hello', expected: 'Hollow Eclipse Lurker Lurker Obsidian' },
  { input: 'Stay safe', expected: 'Scavenge Toxic Ashen Y...'} // placeholder will be replaced below
];

// Build the expected string for the third case programmatically to avoid typo errors.
const thirdExpected = ['S','t','a','y',' ','s','a','f','e']
  .map(ch => {
    const upper = ch.toUpperCase();
    const map = {
      A: 'Ashen', B: 'Bunker', C: 'Cinder', D: 'Dust', E: 'Eclipse', F: 'Feral', G: 'Grit', H: 'Hollow', I: 'Irradiated', J: 'Junk', K: 'Kale', L: 'Lurker', M: 'Mire', N: 'Nexus', O: 'Obsidian', P: 'Purge', Q: 'Quake', R: 'Rubble', S: 'Scavenge', T: 'Toxic', U: 'Utopia', V: 'Vault', W: 'Wasteland', X: 'Xenon', Y: 'Yield', Z: 'Zephyr', ' ': '/'
    };
    return map[upper] || upper;
  })
  .join(' ');

cases[2].expected = thirdExpected;

cases.forEach(({input, expected}) => {
  const result = encode(input);
  assert.strictEqual(result, expected, `Encoding failed for "${input}"`);
});

console.log('All tests passed.');
