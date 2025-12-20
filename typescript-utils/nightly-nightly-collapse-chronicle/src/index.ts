#!/usr/bin/env node

import * as process from "process";

// The moment the world fell apart – the reference point for all calculations.
const COLLAPSE_DATE = new Date("2023-01-01T00:00:00Z");

/**
 * Compute the elapsed time between two dates.
 * Returns an object containing whole days, hours, minutes and seconds.
 */
export function getElapsed(from: Date, to: Date = new Date()): {
  days: number;
  hours: number;
  minutes: number;
  seconds: number;
} {
  const diffMs = Math.max(0, to.getTime() - from.getTime());
  const seconds = Math.floor(diffMs / 1000) % 60;
  const minutes = Math.floor(diffMs / (1000 * 60)) % 60;
  const hours = Math.floor(diffMs / (1000 * 60 * 60)) % 24;
  const days = Math.floor(diffMs / (1000 * 60 * 60 * 24));
  return { days, hours, minutes, seconds };
}

function main(): void {
  const args = process.argv.slice(2);
  let targetDate: Date;

  if (args.length > 0) {
    const parsed = new Date(args[0]);
    if (isNaN(parsed.getTime())) {
      console.error("Invalid date format. Use ISO‑8601 string.");
      process.exit(1);
    }
    targetDate = parsed;
  } else {
    targetDate = new Date();
  }

  const elapsed = getElapsed(COLLAPSE_DATE, targetDate);
  console.log(
    `Days since the Great Collapse: ${elapsed.days} days, ${elapsed.hours} hours, ${elapsed.minutes} minutes, ${elapsed.seconds} seconds`
  );
}

if (require.main === module) {
  main();
}
