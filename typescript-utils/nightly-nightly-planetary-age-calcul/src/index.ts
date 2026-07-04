#!/usr/bin/env node
import { argv } from 'process';

type Planet = {
  name: string;
  orbitalPeriod: number; // Earth years
};

const planets: Planet[] = [
  { name: 'Mercury', orbitalPeriod: 0.2408467 },
  { name: 'Venus', orbitalPeriod: 0.61519726 },
  { name: 'Earth', orbitalPeriod: 1 },
  { name: 'Mars', orbitalPeriod: 1.8808158 },
  { name: 'Jupiter', orbitalPeriod: 11.862615 },
  { name: 'Saturn', orbitalPeriod: 29.447498 },
  { name: 'Uranus', orbitalPeriod: 84.016846 },
  { name: 'Neptune', orbitalPeriod: 164.79132 },
];

export function calculatePlanetaryAges(earthAge: number): Record<string, number> {
  const result: Record<string, number> = {};
  for (const p of planets) {
    result[p.name] = parseFloat((earthAge / p.orbitalPeriod).toFixed(2));
  }
  return result;
}

function printAges(age: number) {
  const ages = calculatePlanetaryAges(age);
  console.log(`Your age on different planets (Earth age: ${age} years):`);
  for (const [planet, planetaryAge] of Object.entries(ages)) {
    console.log(`- ${planet}: ${planetaryAge} years`);
  }
}

// Simple CLI parsing
if (require.main === module) {
  if (argv.length < 3) {
    console.error('Usage: nightly-planetary-age-calculator <earth-age>');
    process.exit(1);
  }
  const age = Number(argv[2]);
  if (isNaN(age) || age < 0) {
    console.error('Please provide a valid non‑negative number for age.');
    process.exit(1);
  }
  printAges(age);
}
