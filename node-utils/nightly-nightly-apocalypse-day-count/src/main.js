#!/usr/bin/env node

/**
 * Nightly Apocalypse Day Counter
 * Calculates days elapsed since 2023‑01‑01.
 */

const { exit } = require('process');

/**
 * Parse a YYYY‑MM‑DD string into a Date object (UTC midnight).
 * @param {string} isoStr
 * @returns {Date}
 */
function parseISODate(isoStr) {
  const parts = isoStr.split('-');
  if (parts.length !== 3) {
    throw new Error('Invalid date format. Expected YYYY-MM-DD');
  }
  const [year, month, day] = parts.map(Number);
  // month is 0‑based for Date constructor
  return new Date(Date.UTC(year, month - 1, day));
}

/**
 * Compute whole days between the apocalypse start (2023‑01‑01) and the given date.
 * If no date string is supplied, the current date (local) is used.
 * @param {string|null} dateStr ISO date string or null
 * @returns {number} Number of days (can be negative for dates before the start)
 */
function daysSinceApocalypse(dateStr) {
  const start = new Date(Date.UTC(2023, 0, 1)); // 2023‑01‑01 UTC
  const target = dateStr ? parseISODate(dateStr) : new Date();
  const diffMs = target - start;
  const msPerDay = 24 * 60 * 60 * 1000;
  return Math.floor(diffMs / msPerDay);
}

/**
 * Simple help message printed when --help is supplied or when arguments are invalid.
 */
function printHelp() {
  console.log('Usage: node src/main.js [--date YYYY-MM-DD]');
  console.log('If --date is omitted, today\'s date is used.');
}

// CLI entry point
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.includes('--help')) {
    printHelp();
    exit(0);
  }

  let dateArg = null;
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--date' && i + 1 < args.length) {
      dateArg = args[i + 1];
      break;
    }
  }

  try {
    const days = daysSinceApocalypse(dateArg);
    console.log(`${days} days since the Great Apocalypse (2023-01-01)`);
  } catch (e) {
    console.error('Error:', e.message);
    printHelp();
    exit(1);
  }
}

module.exports = { daysSinceApocalypse };
