import { calculatePlanetaryAges, formatAgesWithEmoji } from "../src/index";

function mockDate(dateString: string): Date {
  return new Date(dateString);
}

// Mock rationale: using a fixed 'asOf' date to make test deterministic.
const asOf = mockDate("2023-01-01T00:00:00Z");
const birth = mockDate("2000-01-01T00:00:00Z");

const ages = calculatePlanetaryAges(birth, asOf);
const formatted = formatAgesWithEmoji(ages);

if (Math.abs(ages["Earth"] - 23) > 0.01) {
  throw new Error(`Expected Earth age ~23, got ${ages["Earth"]}`);
}
if (!formatted["Mars"].includes("♂")) {
  throw new Error("Mars emoji missing");
}
console.log("All tests passed");
