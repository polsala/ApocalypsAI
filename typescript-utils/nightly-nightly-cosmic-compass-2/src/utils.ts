/**
 * Simple Linear Congruential Generator (LCG) for deterministic pseudo-random numbers.
 * @param seed The initial seed for the generator.
 * @returns A function that generates the next pseudo-random number.
 */
export function createSeededRandom(seed: number) {
  // LCG parameters (standard values)
  const m = 0x80000000; // 2^31
  const a = 1103515245;
  const c = 12345;

  let state = seed % m;

  return function() {
    state = (a * state + c) % m;
    return state / m; // Return a number between 0 (inclusive) and 1 (exclusive)
  };
}

/**
 * Formats a Date object into YYYY-MM-DD string.
 * @param date The Date object to format.
 * @returns A string in YYYY-MM-DD format.
 */
export function formatDate(date: Date): string {
  const year = date.getFullYear();
  const month = (date.getMonth() + 1).toString().padStart(2, '0');
  const day = date.getDate().toString().padStart(2, '0');
  return `${year}-${month}-${day}`;
}

/**
 * Generates a numeric seed from a date string (YYYY-MM-DD).
 * @param dateString The date string.
 * @returns A numeric seed.
 */
export function generateSeedFromDate(dateString: string): number {
  const parts = dateString.split('-').map(Number);
  // A simple way to combine year, month, day into a seed.
  // Ensure it's within a reasonable integer range.
  return (parts[0] * 10000 + parts[1] * 100 + parts[2]) % 2147483647; // Max 31-bit signed int
}
