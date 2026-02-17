#!/usr/bin/env node

export interface PlanetInfo {
  name: string;
  orbitalPeriod: number; // Earth years
}

const planets: PlanetInfo[] = [
  { name: 'Mercury', orbitalPeriod: 0.2408467 },
  { name: 'Venus', orbitalPeriod: 0.61519726 },
  { name: 'Earth', orbitalPeriod: 1 },
  { name: 'Mars', orbitalPeriod: 1.8808158 },
  { name: 'Jupiter', orbitalPeriod: 11.862615 },
  { name: 'Saturn', orbitalPeriod: 29.447498 },
  { name: 'Uranus', orbitalPeriod: 84.016846 },
  { name: 'Neptune', orbitalPeriod: 164.79132 },
  { name: 'Pluto', orbitalPeriod: 248.00 },
];

export function calculatePlanetaryAges(earthAge: number): Record<string, number> {
  if (typeof earthAge !== 'number' || isNaN(earthAge) || earthAge < 0) {
    throw new Error('earthAge must be a non‑negative number');
  }
  const result: Record<string, number> = {};
  for (const p of planets) {
    result[p.name] = parseFloat((earthAge / p.orbitalPeriod).toFixed(2));
  }
  return result;
}

// CLI handling
if (require.main === module) {
  const arg = process.argv[2];
  const age = Number(arg);
  if (isNaN(age)) {
    console.error('Please provide a valid Earth age as a number.');
    process.exit(1);
  }
  const ages = calculatePlanetaryAges(age);
  console.log(JSON.stringify(ages, null, 2));
}
