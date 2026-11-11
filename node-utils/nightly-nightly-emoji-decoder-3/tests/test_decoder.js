const assert = require("assert");
const { decodeEmojis } = require("../src/decoder");

// Mock rationale: deterministic mapping test
assert.strictEqual(decodeEmojis("😀😁😂"), "ABC");
assert.strictEqual(decodeEmojis("😀❓😁"), "A?B");
assert.strictEqual(decodeEmojis(""), "");

console.log("All tests passed");
