#!/usr/bin/env node

/**
 * Calculates remaining amount after radioactive decay.
 * @param {number} initial - initial amount
 * @param {number} halfLife - half‑life period
 * @param {number} days - elapsed time
 * @returns {number} remaining amount
 */
function calculateRemaining(initial, halfLife, days) {
  if (halfLife <= 0) throw new Error('Half‑life must be positive');
  if (initial < 0) throw new Error('Initial amount cannot be negative');
  const exponent = days / halfLife;
  return initial * Math.pow(0.5, exponent);
}

// CLI handling
if (require.main === module) {
  const args = process.argv.slice(2).map(Number);
  if (args.length !== 3 || args.some(isNaN)) {
    console.error('Usage: node src/index.js <initial> <halfLife> <days>');
    process.exit(1);
  }
  const [initial, halfLife, days] = args;
  try {
    const remaining = calculateRemaining(initial, halfLife, days);
    console.log(`${remaining.toFixed(2)} grams remaining after ${days} days`);
  } catch (e) {
    console.error('Error:', e.message);
    process.exit(1);
  }
}

module.exports = { calculateRemaining };
