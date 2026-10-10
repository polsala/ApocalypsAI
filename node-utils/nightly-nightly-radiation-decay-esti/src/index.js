#!/usr/bin/env node
const fs = require('fs');

const halfLives = {
  'I-131': 8 / 365, // days to years
  'Cs-137': 30.17,
  'U-235': 7.04e8,
};

function computeDecay(isotope, initialActivity, years) {
  const hl = halfLives[isotope];
  if (hl === undefined) {
    throw new Error(`Unknown isotope: ${isotope}`);
  }
  const remaining = initialActivity * Math.pow(0.5, years / hl);
  return remaining;
}

// CLI handling
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length !== 3) {
    console.error('Usage: node src/index.js <isotope> <initial_Bq> <years>');
    process.exit(1);
  }
  const [iso, initStr, yearsStr] = args;
  const init = parseFloat(initStr);
  const years = parseFloat(yearsStr);
  if (isNaN(init) || isNaN(years)) {
    console.error('Initial activity and years must be numbers.');
    process.exit(1);
  }
  try {
    const remaining = computeDecay(iso, init, years);
    console.log(`Remaining activity: ${remaining.toFixed(2)} Bq`);
  } catch (e) {
    console.error(e.message);
    process.exit(1);
  }
}

module.exports = { computeDecay, halfLives };
