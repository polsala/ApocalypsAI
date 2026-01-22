#!/usr/bin/env ts-node

export function convert(dateStr: string): string {
  const date = new Date(dateStr);
  if (isNaN(date.getTime())) {
    throw new Error(`Invalid date: ${dateStr}`);
  }
  const year = date.getUTCFullYear();
  const wastelandYear = year - 2000;
  if (wastelandYear < 0) {
    return "Pre-Apocalypse";
  }

  // Compute day of year (1‑based)
  const startOfYear = Date.UTC(year, 0, 1);
  const dayMs = 24 * 60 * 60 * 1000;
  const dayOfYear = Math.floor((date.getTime() - startOfYear) / dayMs) + 1;

  // Wasteland calendar: 13 months × 28 days = 364 days
  const wastelandDay = ((dayOfYear - 1) % 364) + 1;
  const monthNames = [
    "Ash", "Dust", "Ruin", "Scorch", "Blight", "Cinder",
    "Gloom", "Ember", "Frost", "Shade", "Dusk", "Night", "Eclipse"
  ];
  const monthIndex = Math.floor((wastelandDay - 1) / 28);
  const dayInMonth = ((wastelandDay - 1) % 28) + 1;

  const month = monthNames[monthIndex];
  const paddedDay = dayInMonth.toString().padStart(2, "0");
  return `${wastelandYear}-${month}-${paddedDay}`;
}

// CLI support
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length !== 1) {
    console.error("Usage: npx ts-node src/index.ts <YYYY-MM-DD>");
    process.exit(1);
  }
  try {
    console.log(convert(args[0]));
  } catch (e) {
    console.error(e.message);
    process.exit(1);
  }
}
