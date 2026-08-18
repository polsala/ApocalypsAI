const assert = require('assert');
const { encode, decode } = require('../src/index');

function testRoundTrip(str) {
  const enc = encode(str);
  const dec = decode(enc);
  assert.strictEqual(dec, str);
}

// Round‑trip tests
testRoundTrip('');
testRoundTrip('Hello');
testRoundTrip('🚀🌟'); // Unicode characters

// Known mapping test: character 'f' -> hex 66 -> emojis for '6' and '6'
assert.strictEqual(encode('f'), '😅😅');

console.log('All tests passed');
