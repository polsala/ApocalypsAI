#!/usr/bin/env node

function nextWaterDate(lastDateStr, intervalDays) {
  if (typeof lastDateStr !== 'string') {
    throw new Error('lastDateStr must be a string');
  }
  const lastDate = new Date(lastDateStr);
  if (isNaN(lastDate)) {
    throw new Error('Invalid date string');
  }
  if (!Number.isInteger(intervalDays) || intervalDays < 0) {
    throw new Error('intervalDays must be a non‑negative integer');
  }
  const next = new Date(lastDate);
  next.setDate(next.getDate() + intervalDays);
  // Return ISO date (YYYY-MM-DD)
  return next.toISOString().split('T')[0];
}

// CLI handling
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length !== 2) {
    console.error('Usage: node src/index.js <last-watered-ISO> <interval-days>');
    process.exit(1);
  }
  const [lastDateStr, intervalStr] = args;
  const interval = parseInt(intervalStr, 10);
  try {
    const result = nextWaterDate(lastDateStr, interval);
    console.log(result);
  } catch (e) {
    console.error('Error:', e.message);
    process.exit(1);
  }
}

module.exports = { nextWaterDate };
