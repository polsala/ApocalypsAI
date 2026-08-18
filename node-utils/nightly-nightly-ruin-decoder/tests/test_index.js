const assert = require('assert');
const { decode } = require('../src/index');

// Mock rationale: deterministic mapping, no external calls.
function testDecode() {
  const input = '☀☁☂☃★✖✿♞♣♠';
  const expected = 'abcdefghij';
  assert.strictEqual(decode(input), expected, 'Full rune set should decode to abcdefghij');
}

function testPartial() {
  const input = '☀☁XYZ';
  const expected = 'abXYZ';
  assert.strictEqual(decode(input), expected, 'Unknown chars stay unchanged');
}

testDecode();
testPartial();
console.log('All tests passed.');
