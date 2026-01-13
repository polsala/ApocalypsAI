export const MOON_PHASES = ["🌑","🌒","🌓","🌔","🌕","🌖","🌗","🌘"];

/**
 * Generate an array of moon‑phase emojis representing the passage of time.
 * @param seconds Total duration in seconds.
 * @param interval Interval between ticks (seconds).
 * @returns Array of emojis, one per tick.
 */
export function generateChrono(seconds: number, interval: number = 1): string[] {
  if (seconds <= 0 || interval <= 0) {
    return [];
  }
  const steps = Math.floor(seconds / interval);
  const result: string[] = [];
  for (let i = 0; i < steps; i++) {
    result.push(MOON_PHASES[i % MOON_PHASES.length]);
  }
  return result;
}

