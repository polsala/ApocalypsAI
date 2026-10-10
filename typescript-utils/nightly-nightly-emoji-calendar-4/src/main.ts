import { strict as assert } from 'assert';\n\n/**\n * Generate a calendar string for a given year and month. Each day is suffixed with an emoji:\n * - 📅  Weekday (Mon‑Fri)\n * - 🌞  Weekend (Sat‑Sun)\n * - 🎉  Today (overrides other emojis)\n *\n * @param year  Full year (e.g., 2023)\n * @param month 1‑based month (1 = January)\n * @param today Optional Date object representing "today" for deterministic testing.\n * @returns Multiline string representing the calendar.\n */
export function generateCalendar(year: number, month: number, today: Date = new Date()): string {
  // Validate inputs
  assert(Number.isInteger(year) && year > 0, 'year must be a positive integer');
  assert(Number.isInteger(month) && month >= 1 && month <= 12, 'month must be between 1 and 12');
\n  const firstDay = new Date(year, month - 1, 1).getDay(); // 0 = Sun
  const daysInMonth = new Date(year, month, 0).getDate();\n\n  const isSameDay = (d: number): boolean => {
    return (
      d === today.getDate() &&
      month === today.getMonth() + 1 &&
      year === today.getFullYear()
    );
  };\n\n  const rows: string[] = [];
  const header = 'Su Mo Tu We Th Fr Sa';
  rows.push(header);\n\n  let week: string[] = [];
  // Pad leading empty days
  for (let i = 0; i < firstDay; i++) {
    week.push('   ');
  }\n\n  for (let day = 1; day <= daysInMonth; day++) {
    const weekday = (firstDay + day - 1) % 7; // 0‑6\n    let emoji = '📅'; // default weekday\n    if (weekday === 0 || weekday === 6) {
      emoji = '🌞'; // weekend\n    }\n    if (isSameDay(day)) {
      emoji = '🎉'; // today overrides\n    }\n    const cell = `${day}${emoji}`.padEnd(3, ' ');
    week.push(cell);
    if (weekday === 6) {
      rows.push(week.join(' '));
      week = [];
    }
  }\n\n  // Flush remaining days of the last week\n  if (week.length > 0) {
    rows.push(week.join(' '));
  }\n\n  return rows.join('\n');\n}\n\n/** Simple CLI wrapper */\nfunction main() {\n  const args = process.argv.slice(2);\n  const argMap: Record<string, string> = {};
  for (let i = 0; i < args.length; i += 2) {\n    const key = args[i];\n    const value = args[i + 1];\n    if (key && value) {\n      argMap[key.replace(/^--/, '')] = value;\n    }\n  }\n  const now = new Date();\n  const year = argMap['year'] ? parseInt(argMap['year'], 10) : now.getFullYear();\n  const month = argMap['month'] ? parseInt(argMap['month'], 10) : now.getMonth() + 1;\n  try {\n    const output = generateCalendar(year, month, now);\n    console.log(output);\n  } catch (e) {\n    console.error('Error:', (e as Error).message);\n    process.exit(1);\n  }\n}\n\nif (require.main === module) {\n  main();\n}\n
