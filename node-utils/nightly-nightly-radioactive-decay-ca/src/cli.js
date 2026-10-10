#!/usr/bin/env node
const { calculateRemaining } = require('./decay');

function printUsageAndExit() {
  console.error('Usage: node src/cli.js <initial-amount> <half-life> <elapsed-time>');
  process.exit(1);
}

const args = process.argv.slice(2);
if (args.length !== 3) {
  printUsageAndExit();
}
const [initialStr, halfLifeStr, elapsedStr] = args;
const initial = parseFloat(initialStr);
const halfLife = parseFloat(halfLifeStr);
const elapsed = parseFloat(elapsedStr);
if (isNaN(initial) || isNaN(halfLife) || isNaN(elapsed)) {
  printUsageAndExit();
}
try {
  const remaining = calculateRemaining(initial, halfLife, elapsed);
  console.log(`Remaining amount: ${remaining}`);
} catch (err) {
  console.error('Error:', err.message);
  process.exit(1);
}
