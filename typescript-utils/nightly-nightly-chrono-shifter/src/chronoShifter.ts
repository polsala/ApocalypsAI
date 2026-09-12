export enum ShiftUnit {
  LunarCycle = "lunar-cycle",
  VoidWhisper = "void-whisper",
  TemporalRipple = "temporal-ripple",
  StardustBlink = "stardust-blink",
  CosmicTide = "cosmic-tide"
}

export interface ShiftResult {
  originalDate: Date;
  shiftedDate: Date;
  unit: ShiftUnit;
  description: string;
}

/**
 * Shifts a given date by a whimsical, non-standard temporal unit.
 * @param originalDate The date to shift.
 * @param unit The whimsical unit to shift by.
 * @returns A ShiftResult object containing the original, shifted date, unit, and a description.
 */
export function shiftDate(originalDate: Date, unit: ShiftUnit): ShiftResult {
  const shiftedDate = new Date(originalDate.getTime()); // Create a mutable copy

  let description: string;

  switch (unit) {
    case ShiftUnit.LunarCycle:
      // Approximately 29.5 days
      shiftedDate.setDate(shiftedDate.getDate() + 29); // Add 29 days
      shiftedDate.setHours(shiftedDate.getHours() + 12); // Add 12 hours (0.5 days)
      description = "shifted forward by one ethereal lunar cycle.";
      break;
    case ShiftUnit.VoidWhisper:
      // 7 hours, 7 minutes, 7 seconds
      shiftedDate.setHours(shiftedDate.getHours() + 7);
      shiftedDate.setMinutes(shiftedDate.getMinutes() + 7);
      shiftedDate.setSeconds(shiftedDate.getSeconds() + 7);
      description = "gently nudged by a fleeting void whisper.";
      break;
    case ShiftUnit.TemporalRipple:
      // 13 days, 13 hours
      shiftedDate.setDate(shiftedDate.getDate() + 13);
      shiftedDate.setHours(shiftedDate.getHours() + 13);
      description = "rippled through time by a curious temporal anomaly.";
      break;
    case ShiftUnit.StardustBlink:
      // 1 minute, 1 second
      shiftedDate.setMinutes(shiftedDate.getMinutes() + 1);
      shiftedDate.setSeconds(shiftedDate.getSeconds() + 1);
      description = "fast-forwarded by a mere stardust blink.";
      break;
    case ShiftUnit.CosmicTide:
      // Approximately 182 days (half a year)
      shiftedDate.setDate(shiftedDate.getDate() + 182);
      description = "swept along by a grand cosmic tide.";
      break;
    default:
      throw new Error(`Unknown shift unit: ${unit}`);
  }

  return {
    originalDate,
    shiftedDate,
    unit,
    description
  };
}
