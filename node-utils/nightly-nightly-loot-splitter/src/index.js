/*
 * nightly‑loot‑splitter
 * © 2026 ApocalypsAI – whimsical utility for dividing loot.
 *
 * No external dependencies – pure JavaScript (Node.js 14+).
 */

/**
 * Simple linear‑congruential generator for deterministic pseudo‑random numbers.
 * Returns a function that yields a float in [0, 1).
 */
function createRNG(seed) {
  let state = seed >>> 0; // ensure unsigned 32‑bit
  return function () {
    // Constants from Numerical Recipes
    state = (state * 1664525 + 1013904223) >>> 0;
    return state / 0x100000000;
  };
}

/**
 * Compute loot shares.
 * @param {number} total - Total loot value (integer >= 0).
 * @param {number} survivors - Number of survivors (integer > 0).
 * @returns {Object} Mapping survivor IDs to their share.
 */
function computeShares(total, survivors) {
  if (!Number.isInteger(total) || total < 0) {
    throw new Error('total must be a non‑negative integer');
  }
  if (!Number.isInteger(survivors) || survivors <= 0) {
    throw new Error('survivors must be a positive integer');
  }

  const baseShare = Math.floor(total / survivors);
  const remainder = total % survivors; // leftover caps after even split

  // Deterministic RNG seeded with total + survivors
  const rng = createRNG(total + survivors);

  // Generate adjustments in range [-2, 2]
  const adjustments = [];
  let sumAdj = 0;
  for (let i = 0; i < survivors - 1; i++) {
    const adj = Math.floor(rng() * 5) - 2; // 0‑4 -> -2‑2
    adjustments.push(adj);
    sumAdj += adj;
  }
  // Last adjustment makes total adjustment zero
  adjustments.push(-sumAdj);

  const shares = {};
  for (let i = 0; i < survivors; i++) {
    const survivorId = `survivor${i + 1}`;
    let share = baseShare + adjustments[i];
    // Ensure no negative shares; if negative, set to 0 and compensate later
    if (share < 0) share = 0;
    shares[survivorId] = share;
  }

  // Distribute remainder caps to the first survivors (after adjustments)
  let idx = 0;
  let remaining = remainder;
  while (remaining > 0) {
    const survivorId = `survivor${(idx % survivors) + 1}`;
    shares[survivorId] += 1;
    remaining -= 1;
    idx += 1;
  }

  // Final sanity check: total must match input
  const finalTotal = Object.values(shares).reduce((a, b) => a + b, 0);
  if (finalTotal !== total) {
    // Adjust the first survivor to fix any off‑by‑one caused by negative clipping
    const diff = total - finalTotal;
    shares['survivor1'] += diff;
  }

  return shares;
}

// CLI entry point
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length !== 2) {
    console.error('Usage: node src/index.js <total_loot> <survivor_count>');
    process.exit(1);
  }
  const total = Number(args[0]);
  const survivors = Number(args[1]);
  try {
    const result = computeShares(total, survivors);
    console.log(JSON.stringify(result, null, 2));
  } catch (e) {
    console.error('Error:', e.message);
    process.exit(1);
  }
}

module.exports = { computeShares };
