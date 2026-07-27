// nightly-radiation-calculator
// Calculates a whimsical "safe distance" from a radiation source.
// Author: ApocalypsAI Nightly Integrator
// License: MIT

/**
 * Calculate a safe distance (in meters) from a radiation source.
 * Uses a simplified inverse‑square law: distance = sqrt(1 / (sieverts * 0.5)).
 * The result is rounded to two decimal places.
 *
 * @param {number} sieverts - Measured radiation level (must be > 0).
 * @returns {number} Safe distance in meters, rounded to 2 decimals.
 * @throws {Error} If sieverts is not a positive number.
 */
function calculateSafeDistance(sieverts) {
  if (typeof sieverts !== 'number' || isNaN(sieverts) || sieverts <= 0) {
    throw new Error('Sieverts must be a positive number');
  }
  const factor = 0.5; // fictional attenuation factor
  const distance = Math.sqrt(1 / (sieverts * factor));
  return Math.round(distance * 100) / 100; // two decimal places
}

// CLI handling when the file is executed directly
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length !== 1) {
    console.error('Usage: node src/main.js <sieverts>');
    process.exit(1);
  }
  const input = parseFloat(args[0]);
  try {
    const safeDist = calculateSafeDistance(input);
    console.log(`Safe distance: ${safeDist.toFixed(2)} meters. Stay safe, wanderer!`);
  } catch (err) {
    console.error('Error:', err.message);
    process.exit(1);
  }
}

module.exports = { calculateSafeDistance };
