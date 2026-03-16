import { strict as assert } from "assert";
import { encode, decode } from "../src/index";

// Mock rationale: No external I/O, pure functions – deterministic.

function testEncodeSimple() {
  const result = encode("abc");
  assert.equal(result, "🅰️🅱️🌜");
}

function testDecodeSimple() {
  const result = decode("🅰️🅱️🌜");
  assert.equal(result, "abc");
}

function testRoundTrip() {
  const original = "Hello 123";
  const encoded = encode(original);
  const decoded = decode(encoded);
  // encode lower‑cases the input, so compare lower‑cased original.
  assert.equal(decoded, original.toLowerCase());
}

function testUnknownCharsPreserved() {
  const input = "@#%";
  const encoded = encode(input);
  assert.equal(encoded, input);
  const decoded = decode(encoded);
  assert.equal(decoded, input);
}

// Execute tests
try {
  testEncodeSimple();
  testDecodeSimple();
  testRoundTrip();
  testUnknownCharsPreserved();
  console.log("All tests passed.");
} catch (e) {
  console.error("Test failure:", e);
  process.exit(1);
}
