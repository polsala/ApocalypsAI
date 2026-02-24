#!/usr/bin/env node

type PlanetInfo = { name: string; period: number; emoji: string };

const planets: PlanetInfo[] = [
  { name: "Mercury", period: 0.2408467, emoji: "☿" },
  { name: "Venus", period: 0.61519726, emoji: "♀" },
  { name: "Earth", period: 1.0, emoji: "🌍" },
  { name: "Mars", period: 1.8808158, emoji: "♂" },
  { name: "Jupiter", period: 11.862615, emoji: "♃" },
  { name: "Saturn", period: 29.447498, emoji: "♄" },
  { name: "Uranus", period: 84.016846, emoji: "♅" },
  { name: "Neptune", period: 164.79132, emoji: "♆" },
];

export function calculatePlanetaryAges(birth: Date, asOf: Date = new Date()): Record<string, number> {
  const earthAge = (asOf.getTime() - birth.getTime()) / (1000 * 60 * 60 * 24 * 365.25);
  const result: Record<string, number> = {};
  for (const p of planets) {
    result[p.name] = parseFloat((earthAge / p.period).toFixed(2));
  }
  return result;
}

export function formatAgesWithEmoji(ages: Record<string, number>): Record<string, string> {
  const formatted: Record<string, string> = {};
  for (const p of planets) {
    const age = ages[p.name];
    formatted[p.name] = `${age} ${p.emoji} ${p.name}`;
  }
  return formatted;
}

// CLI handling
if (require.main === module) {
  const arg = process.argv[2];
  if (!arg) {
    console.error("Usage: nightly-planetary-age-calculator <YYYY-MM-DD>");
    process.exit(1);
  }
  const birth = new Date(arg);
  if (isNaN(birth.getTime())) {
    console.error("Invalid date format. Use YYYY-MM-DD.");
    process.exit(1);
  }
  const ages = calculatePlanetaryAges(birth);
  const output = formatAgesWithEmoji(ages);
  console.log(JSON.stringify(output, null, 2));
}
