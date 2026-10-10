export function toWasteland(gregorianDate: string): string {
  // Expect YYYY-MM-DD
  const [yearStr, monthStr, dayStr] = gregorianDate.split("-");
  const year = parseInt(yearStr, 10);
  const month = parseInt(monthStr, 10);
  const day = parseInt(dayStr, 10);
  if (isNaN(year) || isNaN(month) || isNaN(day)) {
    throw new Error("Invalid date format. Expected YYYY-MM-DD");
  }
  const wastelandYear = year - 2023; // apocalypse year 2023
  return `Year ${wastelandYear}, Month ${month}, Day ${day}`;
}

// CLI entry point
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length !== 1) {
    console.error("Usage: nightly-wasteland-calendar <YYYY-MM-DD>");
    process.exit(1);
  }
  try {
    const result = toWasteland(args[0]);
    console.log(`Wasteland ${result}`);
  } catch (e: any) {
    console.error(e.message);
    process.exit(1);
  }
}
