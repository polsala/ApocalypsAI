#!/usr/bin/env node
const args = process.argv.slice(2);
function parseArg(flag) {
  const idx = args.indexOf(flag);
  if (idx !== -1 && idx + 1 < args.length) {
    return parseFloat(args[idx + 1]);
  }
  return null;
}
const distance = parseArg('--distance');
const time = parseArg('--time');
const rate = parseArg('--rate');
if (time === null || rate === null) {
  console.error('Usage: node src/index.js --distance <km> --time <hours> --rate <µSv/h>');
  process.exit(1);
}
// distance is currently unused but kept for future expansion
const dose = rate * time;
const safeLimit = 100; // µSv per day
const status = dose <= safeLimit ? 'Safe (below 100 µSv)' : 'Unsafe (exceeds 100 µSv)';
console.log(`Total dose: ${dose} µSv`);
console.log(`Status: ${status}`);
