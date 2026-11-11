const assert = require('assert');
const { encode, decode } = require('../src/main');

// Mock rationale: deterministic tests using known mappings.
assert.strictEqual(encode('HELLO WORLD'), 'MJQQT BTWQI');
assert.strictEqual(decode('MJQQT BTWQI'), 'HELLO WORLD');

// Round‑trip test with spaces and punctuation
const original = 'THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG!';
const encoded = encode(original);
const decoded = decode(encoded);
assert.strictEqual(decoded, original.toUpperCase());

console.log('All tests passed');
