// nightly-cryptic-emoji-decoder – test suite
// No external network calls; all data is mocked via the implementation itself.

const assert = require("assert");
const { encode, decode } = require("../src/index");

// Test encoding of a known word
assert.strictEqual(encode("HELLO"), "🐧🦁🐔🐔🦁");

// Test decoding back to the original word
assert.strictEqual(decode("🐧🦁🐔🐔🦁"), "HELLO");

// Characters without a mapping should remain unchanged
assert.strictEqual(encode("XYZ"), "XYZ");
assert.strictEqual(decode("🦊🐱"), "FC"); // 🦊 -> F, 🐱 -> C

console.log("All tests passed");
