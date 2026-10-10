import { shiftDate, ShiftUnit } from './chronoShifter';

function main() {
  const args = process.argv.slice(2); // Remove 'node' and 'index.js'

  if (args.length !== 2) {
    console.error("Usage: chrono-shifter <date-string> <shift-unit>");
    console.error("Example: chrono-shifter '2023-10-27T10:00:00Z' 'lunar-cycle'");
    console.error("Available units: " + Object.values(ShiftUnit).join(', '));
    process.exit(1);
  }

  const dateString = args[0];
  const unitString = args[1];

  const originalDate = new Date(dateString);

  if (isNaN(originalDate.getTime())) {
    console.error(`Error: Invalid date string provided: \"${dateString}\"`);
    process.exit(1);
  }

  const shiftUnit = unitString as ShiftUnit;
  if (!Object.values(ShiftUnit).includes(shiftUnit)) {
    console.error(`Error: Invalid shift unit provided: \"${unitString}\"`);
    console.error("Available units: " + Object.values(ShiftUnit).join(', '));
    process.exit(1);
  }

  try {
    const result = shiftDate(originalDate, shiftUnit);
    console.log(`Original Date: ${result.originalDate.toISOString()}`);
    console.log(`Shift Unit: ${result.unit}`);
    console.log(`Shifted Date: ${result.shiftedDate.toISOString()}`);
    console.log(`Description: Your date has been ${result.description}`);
  } catch (error: any) {
    console.error(`An unexpected error occurred: ${error.message}`);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}
