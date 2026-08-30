const assert = require('assert');
const { getRandomEmoji } = require('../src/main');

// Mock rationale: provide a single‑emoji list to guarantee deterministic output
const singleEmoji = '🧪';
const result = getRandomEmoji(singleEmoji);
assert.strictEqual(result, '🧪', 'When only one emoji is supplied, it should be returned unchanged');

// Mock rationale: test that whitespace is trimmed and empty entries are ignored
const mixedList = ' 🚀 , ,✨,🔥  ,  ';
const possible = ['🚀', '✨', '🔥'];
const chosen = getRandomEmoji(mixedList);
assert.ok(possible.includes(chosen), 'Chosen emoji should be one of the trimmed entries');

console.log('All tests passed');
