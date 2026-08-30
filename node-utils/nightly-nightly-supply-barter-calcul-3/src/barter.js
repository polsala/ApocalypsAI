#!/usr/bin/env node
const fs = require('fs');

/**
 * Calculate adjusted barter values for a list of supply items.
 * @param {Array<{name:string, baseValue:number, scarcity:number}>} items
 * @returns {Array<{name:string, adjustedValue:number}>}
 */
function calculateBarterValues(items) {
  return items.map(item => {
    const {name, baseValue, scarcity} = item;
    // Ensure inputs are numbers; fallback to 0 if malformed.
    const base = Number(baseValue) || 0;
    const scar = Math.min(Math.max(Number(scarcity) || 0, 0), 1);
    const adjusted = Math.round(base * (1 + (1 - scar) * 0.5) * 100) / 100;
    return {name, adjustedValue: adjusted};
  });
}

// CLI execution block
if (require.main === module) {
  const [,, filePath] = process.argv;
  if (!filePath) {
    console.error('Usage: node src/barter.js <path-to-json>');
    process.exit(1);
  }
  try {
    const raw = fs.readFileSync(filePath, 'utf8');
    const data = JSON.parse(raw);
    const result = calculateBarterValues(data);
    console.log(JSON.stringify(result, null, 2));
  } catch (e) {
    console.error('Error reading or parsing file:', e.message);
    process.exit(1);
  }
}

module.exports = {calculateBarterValues};
