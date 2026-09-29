const assert = require('assert');
const { analyzeMood } = require('../src/main');

function test(input, expected) {
  const result = analyzeMood(input);
  assert.strictEqual(result, expected, `Input: "${input}"`);
}

test('I love sunny days', '😊');
test('I am sad and lonely', '😞');
test('This is terrible and I hate it', '😠');
test('Just an ordinary day', '😐');
test('', '😐');

console.log('All tests passed');
