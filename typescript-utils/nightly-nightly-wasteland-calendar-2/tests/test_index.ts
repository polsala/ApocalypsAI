import { strict as assert } from "assert";
import { convert } from "../src/index";

function test(date: string, expected: string) {
  const result = convert(date);
  assert.equal(result, expected, `convert(${date})`);
}

// Known conversions
test("2000-01-01", "0-Ash-01");
test("2000-01-28", "0-Ash-28");
test("2000-01-29", "0-Dust-01");
test("2025-04-01", "25-Scorch-01");
test("1999-12-31", "Pre-Apocalypse");

// Leap year handling (2024 is a leap year)
test("2024-02-29", "24-Ruin-04");

console.log("All tests passed.");
