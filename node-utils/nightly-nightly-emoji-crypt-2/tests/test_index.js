// tests/test_index.js – simple Node.js assertions (no external test framework)
// ---------------------------------------------------------------------------
// Mock rationale: All tests run locally, no network calls, deterministic.

const assert = require('assert');
const { encode, decode } = require('../src/index.js');

function testEncodeDecode() {
  const original = "Hello World 123!";
  const encoded = encode(original);
  const decoded = decode(encoded);
  // The exclamation mark is not in the map, so it should survive unchanged.
  assert.strictEqual(decoded, original.toLowerCase().replace(/ /g, ' '), 'Decoded text should match original (case‑insensitive for mapped chars)');
}

function testPassThrough() {
  const weird = "@#%&*";
  const encoded = encode(weird);
  // No mapping for these symbols, so encode should return the same string.
  assert.strictEqual(encoded, weird, 'Unmapped symbols must pass through unchanged');
  const decoded = decode(encoded);
  assert.strictEqual(decoded, weird, 'Decoding unmapped symbols must also be unchanged');
}

function runTests() {
  try {
    testEncodeDecode();
    testPassThrough();
    console.log('All tests passed.');
    process.exit(0);
  } catch (err) {
    console.error('Test failure:', err.message);
    process.exit(1);
  }
}

runTests();
