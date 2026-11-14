const assert = require('assert');
const { timeToEmoji } = require('../src/index.js');

// Test exact hour with zero minutes.
assert.strictEqual(timeToEmoji('00:00'), '🕛');
assert.strictEqual(timeToEmoji('12:00'), '🕛');
assert.strictEqual(timeToEmoji('03:00'), '🕒');

// Test hour with minutes that round down.
assert.strictEqual(timeToEmoji('14:32'), '🕑🕖'); // 32 → 30 minutes (index 6) → 🕖

// Test hour with minutes that round up and cause hour overflow.
assert.strictEqual(timeToEmoji('23:58'), '🕛'); // 58 → 60 → hour rolls to 0 → 🕛

// Test typical example from README.
assert.strictEqual(timeToEmoji('14:35'), '🕑🕖');

console.log('All tests passed.');
