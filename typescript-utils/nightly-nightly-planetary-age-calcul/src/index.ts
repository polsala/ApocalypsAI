import { readFileSync } from "fs";

/**
 * Orbital periods relative to Earth years.
 */
const ORBITAL_PERIODS: Record<string, number> = {
  Mercury: 0.2408467,
  Venus: 0.61519726,
  Earth: 1.0,
  Mars: 1.8808158,
  Jupiter: 11.862615,
  Saturn: 29.447498,
  Uranus: 84.016846,
  Neptune: 164.79132,
  Pluto: 248.00,
};

/**
 * Emoji map for each world.
 */
const EMOJIS: Record<string, string> = {
  Mercury: "☿",
  Venus: "♀",
  Earth: "🌍",
  Mars: "♂",
  Jupiter: "♃",
  Saturn: "♄",
  Uranus: "⛢",
  Neptune: "♆",
  Pluto: "♇",
};

/**
 * Compute ages on all planets.
 * @param birthDate Date of birth.
 * @param asOfDate Date to calculate age at (defaults to now).
 * @returns Mapping of planet name to age in Earth years.
 */
export function computePlanetaryAges(
  birthDate: Date,
  asOfDate: Date = new Date()
): Record<string, number> {
  const secondsDiff = (asOfDate.getTime() - birthDate.getTime()) / 1000;
  const earthYearSeconds = 31557600; // 365.25 days
  const earthYears = secondsDiff / earthYearSeconds;

  const ages: Record<string, number> = {};
  for (const [planet, period] of Object.entries(ORBITAL_PERIODS)) {
    ages[planet] = earthYears / period;
  }
  return ages;
}

/**
 * Pretty‑print the ages with emojis.
 */
function printAges(ages: Record<string, number>) {
  for (const planet of Object.keys(ORBITAL_PERIODS)) {
    const emoji = EMOJIS[planet] ?? "";
    const age = ages[planet];
    console.log(`${emoji} ${planet.padEnd(8)}: ${age.toFixed(2)} years`);
  }
}

/**
 * CLI entry point.
 */
function main() {
  const args = process.argv.slice(2);
  if (args.length < 1) {
    console.error("Usage: node src/index.js <YYYY-MM-DD> [--as-of YYYY-MM-DD]");
    process.exit(1);
  }
  const birthStr = args[0];
  const asOfIdx = args.indexOf("--as-of");
  const asOfStr = asOfIdx !== -1 && args.length > asOfIdx + 1 ? args[asOfIdx + 1] : undefined;

  const birthDate = new Date(birthStr);
  if (isNaN(birthDate.getTime())) {
    console.error("Invalid birthdate format. Use YYYY-MM-DD.");
    process.exit(1);
  }
  const asOfDate = asOfStr ? new Date(asOfStr) : new Date();
  if (isNaN(asOfDate.getTime())) {
    console.error("Invalid --as-of date format. Use YYYY-MM-DD.");
    process.exit(1);
  }

  const ages = computePlanetaryAges(birthDate, asOfDate);
  printAges(ages);
}

if (require.main === module) {
  main();
}
