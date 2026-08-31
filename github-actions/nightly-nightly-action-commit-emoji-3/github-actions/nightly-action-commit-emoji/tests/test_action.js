const { selectEmoji } = require('../src/index.js');
const assert = require('assert');

// Short message → rocket
assert.strictEqual(selectEmoji('Fix bug'), '🚀');

// Medium length message → star
assert.strictEqual(
  selectEmoji('Add feature to improve user onboarding flow'),
  '🌟'
);

// Long message → turtle
assert.strictEqual(
  selectEmoji('Refactor the entire authentication subsystem to support multi‑factor authentication and improve security posture across all services'),
  '🐢'
);

console.log('All tests passed');
