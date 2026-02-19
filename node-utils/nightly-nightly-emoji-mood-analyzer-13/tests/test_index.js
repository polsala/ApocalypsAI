const assert = require("assert");
const { analyzeMood } = require("../src/index");

// Mock rationale: deterministic word lists ensure predictable scores

// Positive sentiment (score > 2)
assert.strictEqual(
  analyzeMood("I love sunny days and wonderful moments"),
  "😄"
);

// Slightly positive (score 1‑2)
assert.strictEqual(
  analyzeMood("It is a good day"),
  "😊"
);

// Neutral (score 0)
assert.strictEqual(
  analyzeMood("The sky is blue"),
  "😐"
);

// Slightly negative (score -1‑-2)
assert.strictEqual(
  analyzeMood("I feel sad and a bit angry"),
  "🙁"
);

// Strongly negative (score < -2)
assert.strictEqual(
  analyzeMood("This is terrible, horrible, and awful"),
  "😞"
);

console.log("All tests passed");
