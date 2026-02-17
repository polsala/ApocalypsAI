import { calculatePlanetaryAges } from "../src/index";
import assert from 'assert';

function approxEqual(a: number, b: number, epsilon = 0.01) {
  return Math.abs(a - b) < epsilon;
}

// Test known values for an Earth age of 30 years
const ages = calculatePlanetaryAges(30);
assert(approxEqual(ages['Mercury'], 124.6));
assert(approxEqual(ages['Venus'], 48.73));
assert(approxEqual(ages['Earth'], 30));
assert(approxEqual(ages['Mars'], 15.95));
assert(approxEqual(ages['Jupiter'], 2.53));
assert(approxEqual(ages['Saturn'], 1.02));
assert(approxEqual(ages['Uranus'], 0.36));
assert(approxEqual(ages['Neptune'], 0.18));
assert(approxEqual(ages['Pluto'], 0.12));

// Test error handling for negative input
let threw = false;
try {
  calculatePlanetaryAges(-5);
} catch (e) {
  threw = true;
}
assert(threw, 'Should throw on negative age');

console.log('All tests passed');
