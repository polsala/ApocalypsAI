// Nightly Radiation Decay Estimator
// SPDX-License-Identifier: MIT

/**
 * Half‑life data (in years) for a few common isotopes.
 * Values are approximate but sufficient for demonstration purposes.
 */
const HALF_LIVES = {
  'U-235': 703800000, // Uranium‑235
  'U-238': 4478000000, // Uranium‑238
  'C-14': 5730, // Carbon‑14
  'I-131': 8.02 / 365, // Iodine‑131 (8.02 days converted to years)
};

/**
 * Calculates the remaining fraction of activity after a given number of years.
 *
 * @param {string} isotope - Isotope identifier (e.g., "U-235").
 * @param {number} years - Elapsed time in years (must be >= 0).
 * @returns {number} Remaining activity as a fraction of the original (0‑1).
 * @throws {Error} If the isotope is unknown or years is negative.
 */
function estimateDecay(isotope, years) {
  if (typeof isotope !== 'string') {
    throw new Error('Isotope must be a string');
  }
  const halfLife = HALF_LIVES[isotope];
  if (halfLife === undefined) {
    throw new Error(`Unknown isotope: ${isotope}`);
  }
  if (typeof years !== 'number' || years < 0) {
    throw new Error('Years must be a non‑negative number');
  }
  // Decay formula: remaining = 0.5 ^ (t / halfLife)
  const exponent = years / halfLife;
  return Math.pow(0.5, exponent);
}

/** Simple CLI argument parser (no external deps). */
function parseArgs(argv) {
  const args = {};
  argv.forEach(arg => {
    if (arg.startsWith('--')) {
      const [key, value] = arg.slice(2).split('=');
      args[key] = value;
    }
  });
  return args;
}

if (require.main === module) {
  const args = parseArgs(process.argv.slice(2));
  const isotope = args.isotope;
  const years = parseFloat(args.years);
  if (!isotope || isNaN(years)) {
    console.error('Usage: node src/main.js --isotope=<ISOTOPE> --years=<YEARS>');
    process.exit(1);
  }
  try {
    const fraction = estimateDecay(isotope, years);
    console.log(`Isotope: ${isotope}`);
    console.log(`Years elapsed: ${years}`);
    console.log(`Remaining activity: ${fraction.toFixed(4)} (${(fraction * 100).toFixed(2)}% of original)`);
  } catch (e) {
    console.error('Error:', e.message);
    process.exit(1);
  }
}

module.exports = { estimateDecay };
