/**
 * Emoji Calendar Generator
 * Generates a month calendar where each day is prefixed with an emoji representing the weekday.
 */
export const WEEKDAY_EMOJIS = ['âï¸','ð','ð','ð','ð','ð','ð'] as const;

/**
 * Generate a printable calendar for a given month and year.
 * @param month 1â12
 * @param year full year (e.g., 2023)
 * @returns array of strings, each representing a week line
 */
export function generateCalendar(month: number, year: number): string[] {
  // Validate month
  if (month < 1 || month > 12) {
    throw new Error('Month must be between 1 and 12');
  }
  const weeks: string[][] = [];
  const first = new Date(year, month - 1, 1);
  const daysInMonth = new Date(year, month, 0).getDate();
  let day = 1;
  // First week â may have leading blanks
  const firstWeek: string[] = [];
  for (let wd = 0; wd < 7; wd++) {
    if (wd < first.getDay()) {
      firstWeek.push('   ');
    } else {
      const emoji = WEEKDAY_EMOJIS[wd];
      firstWeek.push(`${emoji}${day.toString().padStart(2, '0')}`);
      day++;
    }
  }
  weeks.push(firstWeek);
  // Subsequent weeks
  while (day <= daysInMonth) {
    const week: string[] = [];
    for (let wd = 0; wd < 7 && day <= daysInMonth; wd++) {
      const emoji = WEEKDAY_EMOJIS[wd];
      week.push(`${emoji}${day.toString().padStart(2, '0')}`);
      day++;
    }
    // Pad the rest of the week with blanks if month ended early
    while (week.length < 7) {
      week.push('   ');
    }
    weeks.push(week);
  }
  // Convert each week array to a single string line
  return weeks.map(w => w.join(' '));
}

// CLI entry point â executed when the file is run directly with Node
if (require.main === module) {
  const args = process.argv.slice(2).map(Number);
  const now = new Date();
  const month = args[0] && args[0] >= 1 && args[0] <= 12 ? args[0] : now.getMonth() + 1;
  const year = args[1] && args[1] >= 1970 ? args[1] : now.getFullYear();
  const lines = generateCalendar(month, year);
  console.log(`Emoji Calendar for ${month}/${year}`);
  lines.forEach(l => console.log(l));
}

