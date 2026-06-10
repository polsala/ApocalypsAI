import assert from 'assert';
import { encodeToEmoji, decodeFromEmoji } from '../src/index';

// Test the static mapping for a known string
const sample = 'abc';
// "abc" -> hex 61 62 63 -> "616263"
// Expected emoji sequence: 6️⃣1️⃣6️⃣2️⃣6️⃣3️⃣
const expected = '6️⃣1️⃣6️⃣2️⃣6️⃣3️⃣';
const encoded = encodeToEmoji(sample);
assert.strictEqual(encoded, expected, 'Encoding of "abc" does not match expected emoji sequence');

// Decode back to original
const decoded = decodeFromEmoji(encoded);
assert.strictEqual(decoded, sample, 'Decoding failed to recover original string');

// Full round‑trip with a more complex string
const original = 'Apocalypse! 🌍';
const roundTrip = decodeFromEmoji(encodeToEmoji(original));
assert.strictEqual(roundTrip, original, 'Round‑trip conversion failed for complex string');

console.log('All tests passed.');
