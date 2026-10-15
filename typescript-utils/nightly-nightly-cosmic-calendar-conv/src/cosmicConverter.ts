export type StellarCycle = {
  name: string;
  symbol: string;
};

export type LunarPhase = {
  name: string;
  emoji: string;
};

export type GalacticEra = {
  name: string;
  description: string;
};

export type CosmicDate = {
  earthDate: Date;
  stellarCycle: StellarCycle;
  lunarPhase: LunarPhase;
  galacticEra: GalacticEra;
  cosmicDay: number; // Day of the year in cosmic terms (1-indexed)
  cosmicDayName: string; // Whimsical name for the day
  fullCosmicString: string;
};

// Mappings for cosmic elements
const STELLAR_CYCLES: StellarCycle[] = [
  { name: "Nebula's Embrace", symbol: "✨" },
  { name: "Comet's Trail", symbol: "☄️" },
  { name: "Pulsar's Hum", symbol: "🎶" },
  { name: "Void's Whisper", symbol: "🌌" },
  { name: "Solar Flare", symbol: "☀️" },
  { name: "Dark Matter Drift", symbol: "⚫" },
  { name: "Stardust Bloom", symbol: "🌸" },
  { name: "Cosmic Ray Dance", symbol: "⚡" },
  { name: "Singularity's Gaze", symbol: "👁️" },
  { name: "Quantum Foam Ripple", symbol: "🌊" },
  { name: "Event Horizon Spin", symbol: "🌀" },
  { name: "Celestial Alignment", symbol: "🔭" }
];

const LUNAR_PHASES: LunarPhase[] = [
  { name: "New Moon's Promise", emoji: "🌑" },
  { name: "Waxing Crescent's Hope", emoji: "🌒" },
  { name: "First Quarter's Resolve", emoji: "🌓" },
  { name: "Waxing Gibbous's Growth", emoji: "🌔" },
  { name: "Full Moon's Radiance", emoji: "🌕" },
  { name: "Waning Gibbous's Reflection", emoji: "🌖" },
  { name: "Last Quarter's Release", emoji: "🌗" },
  { name: "Waning Crescent's Retreat", emoji: "🌘" }
];

const GALACTIC_ERAS: GalacticEra[] = [
  { name: "Era of the Great Silence", description: "Before the echoes began." },
  { name: "Era of the Shifting Stars", description: "When the constellations danced anew." },
  { name: "Era of the Void's Awakening", description: "The current epoch of cosmic integration." },
  { name: "Era of the Whispering Galaxies", description: "The future, yet to unfold." }
];

/**
 * Calculates the 1-indexed day of the year for a given Date object.
 * @param date The Date object.
 * @returns The day of the year (1-365 or 1-366 for leap years).
 */
function getDayOfYear(date: Date): number {
  const start = new Date(date.getFullYear(), 0, 1); // January 1st of the current year
  const diff = date.getTime() - start.getTime();
  const oneDay = 1000 * 60 * 60 * 24;
  return Math.floor(diff / oneDay) + 1; // Add 1 because it's 1-indexed
}

/**
 * Converts a standard Earth date string (YYYY-MM-DD) into a CosmicDate object.
 * @param dateString The Earth date in YYYY-MM-DD format.
 * @returns A CosmicDate object or null if the input date is invalid.
 */
export function convertToCosmicDate(dateString: string): CosmicDate | null {
  const date = new Date(dateString);
  if (isNaN(date.getTime())) {
    return null; // Invalid date
  }

  const year = date.getFullYear();

  // Stellar Cycle: Based on year modulo length of cycles
  // (year - 2000) ensures a consistent starting point for the cycle.
  const stellarCycleIndex = (year - 2000) % STELLAR_CYCLES.length;
  const stellarCycle = STELLAR_CYCLES[stellarCycleIndex < 0 ? stellarCycleIndex + STELLAR_CYCLES.length : stellarCycleIndex];

  // Lunar Phase: Simplified, distributed across the days of the year.
  // This provides a consistent 'phase' for any given day of the year.
  const dayOfYear = getDayOfYear(date);
  const lunarPhaseIndex = Math.floor((dayOfYear / (date.getFullYear() % 4 === 0 ? 366 : 365)) * LUNAR_PHASES.length) % LUNAR_PHASES.length;
  const lunarPhase = LUNAR_PHASES[lunarPhaseIndex];

  // Galactic Era: Based on centuries, starting from 2000.
  // Capped at the last defined era to avoid out-of-bounds access for very future dates.
  const eraOffset = year - 2000;
  const eraIndex = Math.floor(eraOffset / 100);
  const galacticEra = GALACTIC_ERAS[Math.min(eraIndex, GALACTIC_ERAS.length - 1)];

  // Cosmic Day: Simply the day of the year, with a whimsical name.
  const cosmicDay = dayOfYear;
  const cosmicDayName = `Day ${cosmicDay} of the ${stellarCycle.name}`;

  const fullCosmicString =
    `${stellarCycle.symbol} ${stellarCycle.name}, ` +
    `${lunarPhase.emoji} ${lunarPhase.name}, ` +
    `Cosmic Day ${cosmicDay} (${cosmicDayName}), ` +
    `within the ${galacticEra.name}.`;

  return {
    earthDate: date,
    stellarCycle,
    lunarPhase,
    galacticEra,
    cosmicDay,
    cosmicDayName,
    fullCosmicString
  };
}
