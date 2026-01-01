export function generateCalendar(year: number, month: number): string {
  const daysInMonth = new Date(year, month, 0).getDate();
  const firstDay = new Date(year, month - 1, 1).getDay(); // 0=Sunday
  const emojis = ['⚫', '🟢', '🟡', '🔵', '🟠', '🟣', '🟤']; // Sunday to Saturday
  let calendar = `Calendar for ${year}-${String(month).padStart(2, '0')}\n`;
  calendar += 'Sun Mon Tue Wed Thu Fri Sat\\n';
  let week = '';
  for (let i = 0; i < firstDay; i++) {
    week += '    ';
  }
  for (let day = 1; day <= daysInMonth; day++) {
    const dayOfWeek = new Date(year, month - 1, day).getDay();
    const emoji = emojis[dayOfWeek];
    week += `${day.toString().padStart(2, ' ')}${emoji} `;
    if (dayOfWeek === 6) {
      calendar += week.trimEnd() + '\\n';
      week = '';
    }
  }
  if (week) {
    calendar += week.trimEnd() + '\\n';
  }
  return calendar;
}

if (require.main === module) {
  const args = process.argv.slice(2);
  const now = new Date();
  const year = args[0] ? parseInt(args[0], 10) : now.getFullYear();
  const month = args[1] ? parseInt(args[1], 10) : now.getMonth() + 1;
  console.log(generateCalendar(year, month));
}
