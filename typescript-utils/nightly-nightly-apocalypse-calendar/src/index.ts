#!/usr/bin/env node

export const APOCALYPSE_EPOCH = new Date('2023-01-01T00:00:00Z');

/**
 * Compute the number of whole days that have elapsed since the apocalypse epoch.
 * @param target Date to compute against â defaults to now.
 * @returns Number of days (integer).
 */
export function computeDays(target: Date = new Date()): number {
  const diff = target.getTime() - APOCALYPSE_EPOCH.getTime();
  return Math.floor(diff / (1000 * 60 * 60 * 24));
}

if (require.main === module) {
  const arg = process.argv[2];
  const date = arg ? new Date(arg) : new Date();
  if (isNaN(date.getTime())) {
    console.error('Invalid date format. Use YYYY-MM-DD.');
    process.exit(1);
  }
  const days = computeDays(date);
  console.log(`It has been ${days} days since the Great Fallout.`);
}

