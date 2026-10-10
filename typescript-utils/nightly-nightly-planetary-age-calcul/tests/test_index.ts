import { computePlanetaryAges } from "../src/index";

function approxEqual(a: number, b: number, epsilon = 0.01): boolean {
  return Math.abs(a - b) < epsilon;
}

// Mock rationale: Use a fixed reference date to make the test deterministic.
const birth = new Date("2000-01-01T00:00:00Z");
const asOf = new Date("2020-01-01T00:00:00Z"); // Exactly 20 Earth years later

const ages = computePlanetaryAges(birth, asOf);

// Earth should be exactly 20 years.
if (!approxEqual(ages["Earth"], 20)) {
  console.error(`Earth age mismatch: expected 20, got ${ages["Earth"]}`);
  process.exit(1);
}

// Mercury age = 20 / 0.2408467 ≈ 83.07
if (!approxEqual(ages["Mercury"], 20 / 0.2408467)) {
  console.error(`Mercury age mismatch: expected ${20 / 0.2408467}, got ${ages["Mercury"]}`);
  process.exit(1);
}

// Venus age = 20 / 0.61519726 ≈ 32.51
if (!approxEqual(ages["Venus"], 20 / 0.61519726)) {
  console.error(`Venus age mismatch: expected ${20 / 0.61519726}, got ${ages["Venus"]}`);
  process.exit(1);
}

console.log("All planetary age tests passed.");
process.exit(0);
