const assert = require('assert');
const { getRandomEmoji } = require('../src/emoji');

function testWithMockedRandom(mockValue, expectedEmoji) {
  const originalRandom = Math.random;
  Math.random = () => mockValue;
  const result = getRandomEmoji();
  Math.random = originalRandom;
  assert.strictEqual(result, expectedEmoji);
}

testWithMockedRandom(0, "😀");

testWithMockedRandom(0.9999, "🤖");

console.log("All tests passed.");
