import { strict as assert } from "assert";
import { convertToWasteland } from "../src/index";

// Mock rationale: deterministic conversion, no external calls.
function testBasic() {
  const out = convertToWasteland("2025-03-14");
  assert.equal(out, "48 Scorch 14");
}

function testEdgeYear() {
  const out = convertToWasteland("2077-01-01");
  assert.equal(out, "0 Dust 1");
}

function testInvalidFormat() {
  let threw = false;
  try {
    convertToWasteland("14-03-2025");
  } catch {
    threw = true;
  }
  assert.equal(threw, true);
}

testBasic();
testEdgeYear();
testInvalidFormat();

console.log("All tests passed.");
