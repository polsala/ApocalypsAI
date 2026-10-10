import { calculatePlanetaryAges } from '../src/index';
import assert from 'assert';

function approxEqual(a: number, b: number, epsilon = 0.01) {
  return Math.abs(a - b) < epsilon;
}

// Mock rationale: deterministic values based on known orbital periods.
const earthAge = 30;
const ages = calculatePlanetaryAges(earthAge);

// Expected values (rounded to 2 decimals)
const expected: Record<string, number> = {
  Mercury: 124.58,
  Venus: 48.73,
  Earth: 30.00,
  Mars: 15.95,
  Jupiter: 2.53,
  Saturn: 1.02,
  Uranus: 0.36,
  Neptune: 0.18,
};

for (const planet of Object.keys(expected)) {
  assert(
    approxEqual(ages[planet], expected[planet]),
    `Age on ${planet} should be ${expected[planet]}, got ${ages[planet]}`
  );
}

console.log('All planetary age calculations passed.');
