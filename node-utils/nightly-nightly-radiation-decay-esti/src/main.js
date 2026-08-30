#!/usr/bin/env node
// Nightly Radiation Decay Estimator (Node.js)
// Provides a simple CLI and a programmatic function to compute remaining activity.

// Half‑life data (years). Values are approximate where necessary.
const HALF_LIVES = {
  "C-14": 5730,
  "U-238": 4.468e9,
  // I‑131 half‑life is 8.02 days → convert to years (8.02 / 365)
  "I-131": 8.02 / 365
};

/**
 * Compute the remaining fraction of activity after a given time.
 * @param {string} isotope - Key matching an entry in HALF_LIVES (e.g., "C-14").
 * @param {number} years - Elapsed time in years.
 * @returns {number} Remaining fraction (0‑1).
 * @throws {Error} If the isotope is unknown or years is negative.
 */
function computeDecay(isotope, years) {
  const halfLife = HALF_LIVES[isotope];
  if (halfLife === undefined) {
    throw new Error(`Unknown isotope: ${isotope}`);
  }
  if (years < 0) {
    throw new Error('Years cannot be negative');
  }
  // Remaining fraction = 0.5^(years / halfLife)
  return Math.pow(0.5, years / halfLife);
}

// Simple argument parser for the CLI (no external deps).
function parseArgs(argv) {
  const result = {};
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2);
      const value = argv[i + 1];
      result[key] = value;
      i++; // skip next token (its value)
    }
  }
  return result;
}

// CLI entry point
if (require.main === module) {
  const args = parseArgs(process.argv.slice(2));
  const isotope = args.isotope || args.i;
  const yearsStr = args.years || args.y;
  const years = yearsStr !== undefined ? parseFloat(yearsStr) : NaN;

  if (!isotope || isNaN(years)) {
    console.error('Usage: node src/main.js --isotope <NAME> --years <NUMBER>');
    process.exit(1);
  }

  try {
    const fraction = computeDecay(isotope, years);
    console.log(`Remaining activity of ${isotope} after ${years} years: ${fraction}`);
  } catch (e) {
    console.error(e.message);
    process.exit(1);
  }
}

module.exports = { computeDecay };
