import { getApocalypseName } from "../src/colorNamer";
import assert from "assert";

function test(hex: string, expected: string) {
  const result = getApocalypseName(hex);
  assert.strictEqual(result, expected, `Hex ${hex} should map to ${expected}`);
}

// Mock rationale: deterministic palette ensures fixed mapping.

test("#ff4500", "Molten Ember"); // exact match to palette entry
test("#228b22", "Radioactive Ash"); // forestgreen
test("#000080", "Sooty Night"); // midnightblue
test("#9acd32", "Fungal Glow"); // yellowgreen

console.log("All tests passed");
