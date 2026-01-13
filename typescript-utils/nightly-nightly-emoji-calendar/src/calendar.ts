const WEEKDAY_EMOJIS = ["âï¸", "ð", "ð", "ð", "ð", "ð", "ð¸"]; // Sun to Sat

/**
 * Returns a string representing the calendar for the given month/year.
 * The first line is a centered month header, the second line lists the weekday emojis,
 * followed by rows of day numbers aligned under their emojis.
 */
export function generateCalendar(month: number, year: number): string {
  // Validate inputs (basic)
  if (month < 1 || month > 12) {
    throw new Error("Month must be between 1 and 12");
  }
  if (year < 1) {
    throw new Error("Year must be a positive integer");
  }

  const firstDay = new Date(year, month - 1, 1);
  const daysInMonth = new Date(year, month, 0).getDate();
  const startWeekday = firstDay.getDay(); // 0 = Sun

  // Header centered to width of 20 characters (approx)
  const monthNames = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
  ];
  const header = `${monthNames[month - 1]} ${year}`;
  const headerLine = header.padStart(Math.floor((20 + header.length) / 2)).padEnd(20);

  const emojiLine = WEEKDAY_EMOJIS.join(" ");

  const weeks: string[] = [];
  let week = new Array(7).fill("");
  // Fill initial empty slots before the first day
  for (let i = 0; i < startWeekday; i++) {
    week[i] = "   ";
  }
  let day = 1;
  for (let i = startWeekday; i < 7; i++) {
    week[i] = day.toString().padStart(2, " ") + " ";
    day++;
  }
  weeks.push(week.join(""));

  while (day <= daysInMonth) {
    week = new Array(7).fill("");
    for (let i = 0; i < 7 && day <= daysInMonth; i++) {
      week[i] = day.toString().padStart(2, " ") + " ";
      day++;
    }
    // Fill trailing empty slots
    for (let i = 0; i < 7; i++) {
      if (week[i] === "") {
        week[i] = "   ";
      }
    }
    weeks.push(week.join(""));
  }

  const calendarLines = [headerLine, emojiLine, ...weeks];
  return calendarLines.join("
");
}

