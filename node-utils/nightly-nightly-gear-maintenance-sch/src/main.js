#!/usr/bin/env node
const fs = require('fs');

/**
 * Compute a maintenance schedule for a list of gear items.
 * @param {Array<{name:string, durability:number}>} items
 * @returns {Array<{name:string, durability:number, action:string}>}
 */
function computeSchedule(items) {
  if (!Array.isArray(items)) {
    throw new Error('Items must be an array');
  }
  return items
    .map(item => {
      const durability = Number(item.durability);
      let action = 'Good';
      if (durability < 30) action = 'Repair ASAP';
      else if (durability < 60) action = 'Inspect soon';
      return { name: item.name, durability, action };
    })
    .sort((a, b) => a.durability - b.durability);
}

// CLI handling – only runs when executed directly
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length !== 1) {
    console.error('Usage: node src/main.js <path-to-gear-json>');
    process.exit(1);
  }
  const filePath = args[0];
  try {
    const raw = fs.readFileSync(filePath, 'utf8');
    const items = JSON.parse(raw);
    const schedule = computeSchedule(items);
    console.log(JSON.stringify(schedule, null, 2));
  } catch (err) {
    console.error('Error:', err.message);
    process.exit(1);
  }
}

module.exports = { computeSchedule };
