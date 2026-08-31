const assert = require("assert");
const { computeTotal } = require("../src/index");

// Mock rationale: deterministic sample data
const sample = [
  { name: "Backpack", weight: 5, unit: "kg" },
  { name: "Water Bottle", weight: 2, unit: "lb" },
];

const result = computeTotal(sample);

// Expected calculations:
// 2 lb = 0.907184 kg
// totalKg = 5 + 0.907184 = 5.907184
// 5 kg = 11.0231 lb, plus 2 lb = 13.0231 lb
assert.strictEqual(result.totalKg, 5.907184);
assert.strictEqual(result.totalLb, 13.0231);
console.log("All tests passed");
