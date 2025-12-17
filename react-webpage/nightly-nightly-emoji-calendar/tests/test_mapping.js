const assert = require('assert');
const { getEmojiForDate } = require('../src/emojiMapper');

function test() {
  const date1 = new Date('2023-08-01');
  assert.strictEqual(getEmojiForDate(date1), '😀', 'Day 1 should be 😀');
  const date31 = new Date('2023-08-31');
  assert.strictEqual(getEmojiForDate(date31), '🥳', 'Day 31 should be 🥳');
  console.log('All tests passed.');
}

test();
