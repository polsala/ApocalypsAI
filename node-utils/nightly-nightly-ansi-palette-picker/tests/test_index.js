// Mock rationale: deterministic offline test of color mapping
const assert = require('assert');
const { getAnsiCode } = require('../src/index.js');

// Test known mappings
assert.strictEqual(getAnsiCode('black'), 0, 'black should map to 0');
assert.strictEqual(getAnsiCode('TeAl'), 6, 'case‑insensitive teal should map to 6');
assert.strictEqual(getAnsiCode('orange'), 208, 'orange should map to 208');

// Test unsupported color returns null
assert.strictEqual(getAnsiCode('unknowncolor'), null, 'unknown colors should return null');

console.log('All tests passed.');
