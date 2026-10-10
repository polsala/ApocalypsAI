import { toWasteland } from "../src/index";
import assert from "assert";

function runTests() {
  // Test known conversions
  assert.strictEqual(toWasteland("2023-01-01"), "Year 0, Month 1, Day 1");
  assert.strictEqual(toWasteland("2025-04-01"), "Year 2, Month 4, Day 1");
  assert.strictEqual(toWasteland("2020-12-31"), "Year -3, Month 12, Day 31");

  // Test invalid format handling
  let threw = false;
  try {
    toWasteland("invalid-date");
  } catch (e: any) {
    threw = true;
    assert.strictEqual(e.message, "Invalid date format. Expected YYYY-MM-DD");
  }
  assert.strictEqual(threw, true);

  console.log("All tests passed");
}

runTests();
