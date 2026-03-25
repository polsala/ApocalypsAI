const assert = require('assert');
const { analyzeMood } = require('../src/index.js');

function testPositive() {
  const txt = 'I love sunny days and great coffee';
  assert.strictEqual(analyzeMood(txt), '😊');
}

function testNegative() {
  const txt = 'I hate rainy days and terrible coffee';
  assert.strictEqual(analyzeMood(txt), '😞');
}

function testNeutral() {
  const txt = 'The cat sits on the mat.';
  assert.strictEqual(analyzeMood(txt), '😐');
}

testPositive();
testNegative();
testNeutral();
console.log('All tests passed');
