#!/usr/bin/env ts-node

export interface WastelandDate {
  year: number;
  month: number;
  day: number;
}

/**
 * Convert a Gregorian date to the Wasteland Calendar.
 * @param date Gregorian date to convert.
 * @param apocalypseDate The date of the Great Cataclysm. Defaults to 2023-01-01.
 * @returns WastelandDate object containing year, month (1â12) and day (1â30).
 */
export function toWasteland(date: Date, apocalypseDate: Date = new Date('2023-01-01')): WastelandDate {
  const msPerDay = 24 * 60 * 60 * 1000;
  const diffDays = Math.floor((date.getTime() - apocalypseDate.getTime()) / msPerDay);
  if (diffDays < 0) {
    throw new Error('Date is before the apocalypse');
  }
  const year = Math.floor(diffDays / 360);
  const dayOfYear = diffDays % 360;
  const month = Math.floor(dayOfYear / 30) + 1; // 1â12
  const day = (dayOfYear % 30) + 1; // 1â30
  return { year, month, day };
}

// CLI handling â only runs when the file is executed directly
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length < 1) {
    console.error('Usage: wasteland-calendar <YYYY-MM-DD> [apocalypse-YYYY-MM-DD]');
    process.exit(1);
  }
  const date = new Date(args[0]);
  const apocalypse = args[1] ? new Date(args[1]) : undefined;
  try {
    const wc = toWasteland(date, apocalypse);
    console.log(`Wasteland Date: Year ${wc.year}, Month ${wc.month}, Day ${wc.day}`);
  } catch (e: any) {
    console.error(e.message);
    process.exit(1);
  }
}

