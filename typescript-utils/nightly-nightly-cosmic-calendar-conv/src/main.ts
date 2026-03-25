interface CosmicDate {
  stellarCycle: number;
  phaseName: string;
  phaseNumber: number; // 1-13, or 0 for Temporal Flux
  dayInPhase: number; // 1-28, or 0 for Temporal Flux
  isTemporalFlux: boolean;
  temporalFluxDayNumber?: number; // 1 or 2 for Temporal Flux days
}

const COSMIC_EPOCH_YEAR = 2000;
const PHASE_DURATION_DAYS = 28;
const NUM_PHASES = 13;
const TOTAL_PHASED_DAYS = NUM_PHASES * PHASE_DURATION_DAYS; // 364

const PHASE_NAMES: string[] = [
  "Genesis Glow", "Astral Bloom", "Nebula Nurture", "Comet's Kiss",
  "Void Whisper", "Stardust Serenity", "Galactic Glimmer", "Quantum Quasar",
  "Echoing Emptiness", "Celestial Chill", "Rift Resonance", "Chronos Cascade",
  "Omega Orb"
];

/**
 * Calculates the day of the year (1-indexed) for a given UTC date.
 * @param date The UTC date.
 * @returns The day of the year (1 to 365 or 366).
 */
function getDayOfYearUTC(date: Date): number {
  const startOfYear = new Date(Date.UTC(date.getUTCFullYear(), 0, 1));
  const diff = date.getTime() - startOfYear.getTime();
  return Math.floor(diff / (1000 * 60 * 60 * 24)) + 1;
}

/**
 * Converts an Earth date to a Cosmic Date.
 * @param earthDate The Earth date to convert. Assumes UTC for internal calculations.
 * @returns A CosmicDate object.
 */
export function convertToCosmicDate(earthDate: Date): CosmicDate {
  // Ensure we work with UTC to avoid timezone issues. The input date is treated as UTC.
  const utcYear = earthDate.getUTCFullYear();
  const dayOfYear = getDayOfYearUTC(earthDate);

  const stellarCycle = utcYear - COSMIC_EPOCH_YEAR + 1;

  if (dayOfYear > TOTAL_PHASED_DAYS) {
    // It's a Temporal Flux day
    return {
      stellarCycle: stellarCycle,
      phaseName: "Temporal Flux",
      phaseNumber: 0,
      dayInPhase: 0,
      isTemporalFlux: true,
      temporalFluxDayNumber: dayOfYear - TOTAL_PHASED_DAYS
    };
  } else {
    // It's within a Cosmic Phase
    const phaseIndex = Math.floor((dayOfYear - 1) / PHASE_DURATION_DAYS);
    const dayInPhase = (dayOfYear - 1) % PHASE_DURATION_DAYS + 1;

    return {
      stellarCycle: stellarCycle,
      phaseName: PHASE_NAMES[phaseIndex],
      phaseNumber: phaseIndex + 1,
      dayInPhase: dayInPhase,
      isTemporalFlux: false
    };
  }
}

// CLI execution logic
if (require.main === module) {
  const args = process.argv.slice(2);
  let inputDate: Date;

  if (args.length > 0) {
    const dateString = args[0];
    // Attempt to parse as UTC to be consistent with internal logic
    inputDate = new Date(dateString + 'T12:00:00Z'); 
    if (isNaN(inputDate.getTime())) {
      console.error(`Error: Invalid date format provided. Please use YYYY-MM-DD. Got: ${dateString}`);
      process.exit(1);
    }
  } else {
    // Use current UTC date if no argument
    const now = new Date();
    inputDate = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate()));
  }

  const cosmicDate = convertToCosmicDate(inputDate);

  console.log(`Earth Date: ${inputDate.toISOString().split('T')[0]}`);
  if (cosmicDate.isTemporalFlux) {
    console.log(`Cosmic Date: Stellar Cycle ${cosmicDate.stellarCycle}, ${cosmicDate.phaseName} Day ${cosmicDate.temporalFluxDayNumber}`);
  } else {
    console.log(`Cosmic Date: Stellar Cycle ${cosmicDate.stellarCycle}, Phase ${cosmicDate.phaseNumber} (${cosmicDate.phaseName}), Day ${cosmicDate.dayInPhase}`);
  }
}
