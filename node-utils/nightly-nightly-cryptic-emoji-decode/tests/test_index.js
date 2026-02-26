const { encode, decode } = require('../src/index');
const assert = require('assert');

// Test encoding of the first three letters
assert.strictEqual(encode('ABC'), '🐶🐱🐭');

// Test decoding back to letters
assert.strictEqual(decode('🐶🐱🐭'), 'ABC');

// Test handling of unknown emoji during decode
assert.strictEqual(decode('❓'), '?');

console.log('All tests passed.');
