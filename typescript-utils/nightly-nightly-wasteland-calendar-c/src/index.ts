#!/usr/bin/env node
import { readFileSync } from "fs";

export function convertToWasteland(gregorian: string): string {
  // Expect YYYY-MM-DD
  const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(gregorian);
  if (!match) {
    throw new Error("Invalid date format. Expected YYYY-MM-DD");
  }
  const [, yearStr, monthStr, dayStr] = match;
  const year = parseInt(yearStr, 10);
  const month = parseInt(monthStr, 10);
  const day = parseInt(dayStr, 10);

  const wastelandYear = year - 2077;
  const monthNames = [
    "Dust",
    "Ash",
    "Scorch",
    "Ember",
    "Ruin",
    "Fallout",
    "Barren",
    "Mirage",
    "Cinder",
    "Blight",
    "Dusk",
    "Nightfall",
  ];
  if (month < 1 || month > 12) {
    throw new Error("Month out of range");
  }
  const monthName = monthNames[month - 1];
  return `${wastelandYear} ${monthName} ${day}`;
}

// CLI handling
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length !== 1) {
    console.error("Usage: npx ts-node src/index.ts <YYYY-MM-DD>");
    process.exit(1);
  }
  try {
    const result = convertToWasteland(args[0]);
    console.log(result);
  } catch (e) {
    console.error((e as Error).message);
    process.exit(1);
  }
}
