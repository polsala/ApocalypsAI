#!/usr/bin/env node
const crypto = require('crypto');

function parseNotation(notation) {
  const match = notation.trim().match(/^(\d*)d(\d+)([+-]\d+)?$/i);
  if (!match) {
    throw new Error('Invalid dice notation. Expected format NdM±K, e.g., 2d6+3');
  }
  const count = match[1] ? parseInt(match[1], 10) : 1;
  const sides = parseInt(match[2], 10);
  const modifier = match[3] ? parseInt(match[3], 10) : 0;
  return { count, sides, modifier };
}

function rollDice({ count, sides }) {
  let total = 0;
  for (let i = 0; i < count; i++) {
    // crypto.randomInt is inclusive of min, exclusive of max
    total += crypto.randomInt(1, sides + 1);
  }
  return total;
}

function main() {
  const arg = process.argv[2] || '1d6';
  try {
    const spec = parseNotation(arg);
    const roll = rollDice(spec);
    const result = roll + spec.modifier;
    console.log(`Rolling ${arg}: ${result}`);
  } catch (e) {
    console.error(e.message);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { parseNotation, rollDice };
