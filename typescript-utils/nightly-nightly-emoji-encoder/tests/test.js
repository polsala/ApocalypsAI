// Mock rationale: Using ts-node/register to import TypeScript source without pre‑compilation.
require('ts-node/register');
const { encode, decode } = require('../src/index.ts');
const assert = require('assert');

function testRoundTrip() {
  const original = 'Apocalypse';
  const encoded = encode(original);
  const decoded = decode(encoded);
  assert.strictEqual(decoded, original, 'Round‑trip failed');
}

function testKnownMapping() {
  // 'A' => UTF‑8 0x41 => hex digits '4' and '1'
  const expected = '4️⃣1️⃣';
  const actual = encode('A');
  assert.strictEqual(actual, expected, 'Encoding of single character A is incorrect');
}

function testInvalidDecode() {
  const bad = '❌'; // not in our mapping
  let threw = false;
  try {
    decode(bad);
  } catch (e) {
    threw = true;
  }
  assert.ok(threw, 'Decoder should throw on invalid emoji');
}

// Run tests
try {
  testRoundTrip();
  testKnownMapping();
  testInvalidDecode();
  console.log('All tests passed');
  process.exit(0);
} catch (err) {
  console.error('Test failure:', err.message);
  process.exit(1);
}

