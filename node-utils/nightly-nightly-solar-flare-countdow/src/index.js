#!/usr/bin/env node
const FLARE_DATES = [
  "2024-09-15",
  "2025-02-10",
  "2025-07-23",
  "2026-01-05",
  "2026-06-30"
].map(d => new Date(d));

function getDaysUntilNextFlare(current) {
  const now = current instanceof Date ? current : new Date();
  for (const flare of FLARE_DATES) {
    if (flare > now) {
      const diffMs = flare - now;
      return Math.ceil(diffMs / (1000 * 60 * 60 * 24));
    }
  }
  return null; // no upcoming flare
}

if (require.main === module) {
  const arg = process.argv[2];
  const inputDate = arg ? new Date(arg) : new Date();
  if (isNaN(inputDate)) {
    console.error("Invalid date provided.");
    process.exit(1);
  }
  const days = getDaysUntilNextFlare(inputDate);
  if (days === null) {
    console.log("No upcoming solar flares are scheduled.");
  } else {
    console.log(`Days until next solar flare: ${days}`);
  }
}

module.exports = { getDaysUntilNextFlare };
