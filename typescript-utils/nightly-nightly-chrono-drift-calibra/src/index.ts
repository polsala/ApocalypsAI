import { TimeInput, DriftResult } from './types';

/**
 * Calculates the temporal drift between an actual time and a perceived time.
 * @param actual The actual, objective Date object.
 * @param perceived The perceived Date object.
 * @returns The drift in milliseconds (perceived - actual).
 */
export function calculateDrift(actual: Date, perceived: Date): number {
  return perceived.getTime() - actual.getTime();
}

/**
 * Determines a whimsical recalibration mantra based on the temporal drift.
 * @param driftMs The temporal drift in milliseconds.
 * @returns A string representing the recalibration mantra.
 */
export function getRecalibrationMantra(driftMs: number): string {
  const absDrift = Math.abs(driftMs);

  // Time thresholds in milliseconds
  const ONE_MINUTE = 60 * 1000;
  const ONE_HOUR = 60 * ONE_MINUTE;
  const ONE_DAY = 24 * ONE_HOUR;

  if (absDrift === 0) {
    return "Your internal chronometer is perfectly aligned with the cosmic flow. Serenity.";
  } else if (absDrift <= ONE_MINUTE) {
    return "A gentle nudge for your temporal compass. Breathe and realign.";
  } else if (absDrift <= ONE_HOUR) {
    return "The fabric of time ripples slightly. Re-anchor your awareness.";
  } else if (absDrift <= ONE_DAY) {
    return "Significant temporal resonance detected. Seek a stable temporal anchor.";
  } else {
    return "Reality itself seems to waver. Embrace the present, for it is all you truly have.";
  }
}

/**
 * Main function to parse arguments, calculate drift, and print results.
 * @param args Command line arguments (e.g., process.argv.slice(2)).
 * @returns A DriftResult object or null if input is invalid.
 */
export function run(args: string[]): DriftResult | null {
  if (args.length !== 2) {
    console.error("Usage: node dist/index.js <actual_time_iso> <perceived_time_iso>");
    return null;
  }

  const [actualTimeStr, perceivedTimeStr] = args;

  const actualTime = new Date(actualTimeStr);
  const perceivedTime = new Date(perceivedTimeStr);

  if (isNaN(actualTime.getTime()) || isNaN(perceivedTime.getTime())) {
    console.error("Error: Invalid date format. Please use ISO 8601 strings.");
    return null;
  }

  const driftMs = calculateDrift(actualTime, perceivedTime);
  const mantra = getRecalibrationMantra(driftMs);

  console.log(`Temporal Drift: ${driftMs}ms`);
  console.log(`Recalibration Mantra: ${mantra}`);

  return { driftMs, mantra };
}

// Only run if executed directly as a script
if (require.main === module) {
  run(process.argv.slice(2));
}
