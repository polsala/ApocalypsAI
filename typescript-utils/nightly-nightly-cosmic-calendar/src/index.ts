interface CosmicDate {
  cosmicYear: number;
  phase: string;
  cycle: number; // Day within the phase
}

const COSMIC_EPOCH_EARTH_DATE = new Date('2000-01-01T00:00:00Z'); // January 1, 2000 UTC
const DAYS_IN_COSMIC_YEAR = 365;

const COSMIC_PHASES = [
  { name: "Nebula Bloom", days: 30 },
  { name: "Void Gaze", days: 30 },
  { name: "Stellar Drift", days: 30 },
  { name: "Comet's Kiss", days: 30 },
  { name: "Dark Matter Harvest", days: 30 },
  { name: "Galactic Whisper", days: 30 },
  { name: "Quantum Ripple", days: 30 },
  { name: "Echoing Singularity", days: 30 },
  { name: "Celestial Alignment", days: 30 },
  { name: "Cosmic Dustfall", days: 30 },
  { name: "Event Horizon", days: 30 },
  { name: "Astral Rebirth", days: 30 },
  { name: "Interstellar Drift", days: 5 } // The remaining days
];

/**
 * Calculates the number of days between two dates.
 * @param date1 The earlier date.
 * @param date2 The later date.
 * @returns The number of full days between date1 and date2.
 */
function getDaysBetween(date1: Date, date2: Date): number {
  const diffTime = Math.abs(date2.getTime() - date1.getTime());
  return Math.floor(diffTime / (1000 * 60 * 60 * 24));
}

/**
 * Converts an Earth date to a Cosmic Date.
 * @param earthDateString An Earth date string (e.g., "YYYY-MM-DD").
 * @returns The corresponding CosmicDate object.
 * @throws Error if the date string is invalid or before the cosmic epoch.
 */
export function earthToCosmic(earthDateString: string): CosmicDate {
  const earthDate = new Date(earthDateString + 'T00:00:00Z'); // Ensure UTC for consistent calculation

  if (isNaN(earthDate.getTime())) {
    throw new Error("Invalid Earth date string provided.");
  }
  if (earthDate < COSMIC_EPOCH_EARTH_DATE) {
    throw new Error("Date is before the Cosmic Epoch (Jan 1, 2000).");
  }

  const totalDaysSinceEpoch = getDaysBetween(COSMIC_EPOCH_EARTH_DATE, earthDate);

  const cosmicYear = Math.floor(totalDaysSinceEpoch / DAYS_IN_COSMIC_YEAR) + 1;
  let daysIntoCosmicYear = totalDaysSinceEpoch % DAYS_IN_COSMIC_YEAR;

  let currentDayCount = 0;
  let phaseName = "";
  let cycle = 0;

  for (const phase of COSMIC_PHASES) {
    if (daysIntoCosmicYear < currentDayCount + phase.days) {
      phaseName = phase.name;
      cycle = daysIntoCosmicYear - currentDayCount + 1;
      break;
    }
    currentDayCount += phase.days;
  }

  return { cosmicYear, phase: phaseName, cycle };
}

/**
 * Converts a Cosmic Date to an Earth Date.
 * @param cosmicYear The cosmic year.
 * @param phaseName The name of the cosmic phase.
 * @param cycle The cycle (day) within the phase.
 * @returns The corresponding Earth Date string (YYYY-MM-DD).
 * @throws Error if the cosmic date is invalid.
 */
export function cosmicToEarth(cosmicYear: number, phaseName: string, cycle: number): string {
  if (cosmicYear < 1) {
    throw new Error("Cosmic Year must be 1 or greater.");
  }

  const targetPhase = COSMIC_PHASES.find(p => p.name.toLowerCase() === phaseName.toLowerCase());
  if (!targetPhase) {
    throw new Error(`Invalid Cosmic Phase: ${phaseName}`);
  }
  if (cycle < 1 || cycle > targetPhase.days) {
    throw new Error(`Cycle ${cycle} is out of range for ${targetPhase.name} (1-${targetPhase.days}).`);
  }

  const daysBeforeTargetCosmicYear = (cosmicYear - 1) * DAYS_IN_COSMIC_YEAR;

  let daysIntoTargetCosmicYear = 0;
  for (const phase of COSMIC_PHASES) {
    if (phase.name.toLowerCase() === phaseName.toLowerCase()) {
      break; // Found the target phase, daysIntoTargetCosmicYear now holds days *before* this phase
    }
    daysIntoTargetCosmicYear += phase.days;
  }
  daysIntoTargetCosmicYear += (cycle - 1); // Add days within the target phase

  const totalDaysToAdd = daysBeforeTargetCosmicYear + daysIntoTargetCosmicYear;

  const earthDate = new Date(COSMIC_EPOCH_EARTH_DATE);
  earthDate.setUTCDate(COSMIC_EPOCH_EARTH_DATE.getUTCDate() + totalDaysToAdd);

  return earthDate.toISOString().split('T')[0];
}
