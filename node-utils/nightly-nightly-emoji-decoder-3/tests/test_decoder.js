// test_decoder.js
const assert = require("assert");
const { decodeEmojis } = require("../src/decoder");

// Mock rationale: deterministic mapping test
assert.strictEqual(decodeEmojis("🍎🍌🍒"), "ABC");

// Unknown emoji should become '?'
assert.strictEqual(decodeEmojis("🚀"), "?");

// Mixed known and unknown
assert.strictEqual(decodeEmojis("🍎🚀🍌"), "A?B");

console.log("All tests passed.");
