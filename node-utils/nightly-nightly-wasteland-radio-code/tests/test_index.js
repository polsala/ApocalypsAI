const assert = require('assert');
const { translate } = require('../src/index');

// Mock rationale: deterministic mapping, no external calls
function testSimple() {
  const result = translate('AB');
  assert.strictEqual(result, 'Ash Bunker');
}

function testLowerCase() {
  const result = translate('ab');
  assert.strictEqual(result, 'Ash Bunker');
}

function testDigits() {
  const result = translate('2021');
  assert.strictEqual(result, 'Two Zero Two One');
}

function testIgnoreUnknown() {
  const result = translate('A! B?');
  assert.strictEqual(result, 'Ash Bunker');
}

function run() {
  testSimple();
  testLowerCase();
  testDigits();
  testIgnoreUnknown();
  console.log('All tests passed');
}

run();
