#!/usr/bin/env node

/**
 * Compute remaining radioactive activity using the exponential decay formula.
 * @param {number} initial - Initial activity in becquerels (Bq).
 * @param {number} halfLife - Half‑life of the isotope in years (must be > 0).
 * @param {number} elapsed - Elapsed time in years.
 * @returns {number} Remaining activity in becquerels.
 */
function computeDecay(initial, halfLife, elapsed) {
  return initial * Math.pow(0.5, elapsed / halfLife);
}

if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length !== 3) {
    console.error("Usage: decay <initial_activity> <half_life> <elapsed_time>");
    process.exit(1);
  }
  const [initialStr, halfLifeStr, elapsedStr] = args;
  const initial = parseFloat(initialStr);
  const halfLife = parseFloat(halfLifeStr);
  const elapsed = parseFloat(elapsedStr);

  if (isNaN(initial) || isNaN(halfLife) || isNaN(elapsed) || halfLife <= 0) {
    console.error("All arguments must be valid numbers, half-life > 0.");
    process.exit(1);
  }

  const remaining = computeDecay(initial, halfLife, elapsed);
  console.log(
    `After ${elapsed} years, activity drops from ${initial} Bq to ${remaining.toFixed(2)} Bq.`
  );

  const ratio = remaining / initial;
  let msg = "";
  if (ratio > 0.5) {
    msg = "The glow is still strong.";
  } else if (ratio > 0.1) {
    msg = "The wasteland is still mildly glowing.";
  } else {
    msg = "Barely a whisper of radiation.";
  }
  console.log(msg);
}

module.exports = { computeDecay };
