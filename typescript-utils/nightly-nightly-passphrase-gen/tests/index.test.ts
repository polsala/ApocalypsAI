import { generatePassphrase } from '../src/index';
import assert from 'assert';

// Test that the generated string follows the expected pattern.
const pass = generatePassphrase();
const parts = pass.split('-');
assert.strictEqual(parts.length, 4, 'Passphrase should have four hyphen‑separated parts');
// Emoji part: non‑empty string (cannot reliably test Unicode range without external libs)
assert.ok(parts[0].length > 0, 'First part should be an emoji');
// Word parts: lowercase alphabetic strings
assert.ok(/^[a-z]+$/.test(parts[1]), 'Second part should be a lowercase word');
assert.ok(/^[a-z]+$/.test(parts[3]), 'Fourth part should be a lowercase word');
// Number part: digits only
assert.ok(/^\d+$/.test(parts[2]), 'Third part should be a number');
console.log('All passphrase tests passed.');
