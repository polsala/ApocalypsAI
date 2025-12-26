import { encode, decode } from "../src/index";
import assert from "assert";

function testRoundTrip() {
  const original = "HELLO WORLD";
  const encoded = encode(original);
  const decoded = decode(encoded);
  // encode turns spaces into '/', decode turns them back
  assert.strictEqual(decoded, original);
  console.log("Round‑trip test passed");
}

function testKnownMapping() {
  const encoded = encode("ABC");
  const expected = "🅰️🅱️🌜";
  assert.strictEqual(encoded, expected);
  const decoded = decode(encoded);
  assert.strictEqual(decoded, "ABC");
  console.log("Known mapping test passed");
}

testRoundTrip();
testKnownMapping();
