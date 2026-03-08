import { strict as assert } from "assert";
import { rot13, encodeToEmoji } from "../src/main";

// Mock rationale: No external resources are required; tests are pure functions.

function testRot13() {
  assert.equal(rot13("Hello"), "Uryyb");
  assert.equal(rot13("Uryyb"), "Hello"); // ROT13 is its own inverse
  assert.equal(rot13("abcXYZ"), "nopKLM");
}

function testEncodeToEmoji() {
  // Input "HelloWorld" -> ROT13 -> "UryybJbeyq"
  // Expected emoji mapping (see README for mapping table)
  const expected = "⛎🌈🪁🪁🅱️🕹️🅱️📧🪁🍳";
  const result = encodeToEmoji("HelloWorld");
  assert.equal(result, expected);

  // Non‑alphabetic characters should pass through unchanged
  const mixed = "123! @#";
  assert.equal(encodeToEmoji(mixed), mixed);
}

function runAll() {
  testRot13();
  testEncodeToEmoji();
  console.log("All tests passed.");
}

runAll();
