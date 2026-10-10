#!/usr/bin/env ts-node\n\n/**\n * nightly-emoji-timezone-converter\n *\n * Convert a timestamp from a source timezone to a target timezone and append an emoji\n * that reflects the time of day in the target zone.\n */\n\nimport { exit } from "process";\n\n/** Map hour (0‑23) to a whimsical emoji */
function hourToEmoji(hour: number): string {
  if (hour >= 5 && hour < 11) return "🌅"; // sunrise
  if (hour >= 11 && hour < 17) return "🌞"; // day
  if (hour >= 17 && hour < 22) return "🌇"; // sunset
  return "🌙"; // night
}\n\n/** Format a Date object in the target timezone as YYYY‑MM‑DD HH:MM */
function formatInTimezone(date: Date, tz: string): string {
  const parts = new Intl.DateTimeFormat("en-CA", { // en-CA gives YYYY‑MM‑DD
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
    timeZone: tz,
  }).formatToParts(date);

  const map: Record<string, string> = {};
  for (const part of parts) {
    map[part.type] = part.value;
  }
  return `${map.year}-${map.month}-${map.day} ${map.hour}:${map.minute}`;
}\n\n/** Parse a time string. If it looks like HH:MM we treat it as today in the source tz. */
function parseInput(timeStr: string, sourceTz: string): Date {
  // Try ISO format first
  const isoDate = new Date(timeStr);
  if (!isNaN(isoDate.getTime())) {
    return isoDate;
  }
  // Fallback to HH:MM (local to source timezone)
  const hhmm = /^([01]?\d|2[0-3]):([0-5]\d)$/.exec(timeStr);
  if (!hhmm) {
    throw new Error(`Invalid time format: ${timeStr}`);
  }
  const now = new Date();
  // Build a string like YYYY‑MM‑DDTHH:MM:00 in source tz using Intl to get the date parts
  const datePart = formatInTimezone(now, sourceTz).split(" ")[0]; // YYYY‑MM‑DD
  const iso = `${datePart}T${hhmm[1].padStart(2, "0")}:${hhmm[2].padStart(2, "0")}:00`;
  // Create date assuming the string is in source tz by using the Intl API to get the epoch ms
  const utcMs = Date.parse(iso + "Z"); // treat as UTC then offset later
  const offset = new Date().toLocaleString("en-US", { timeZone: sourceTz, hour12: false, timeZoneName: "short" }).split(" ").pop();
  // Simpler: use Date constructor with ISO and then adjust via Intl (acceptable for our limited use)
  return new Date(iso);
}\n\nfunction main() {
  const args = process.argv.slice(2);
  if (args.length !== 3) {
    console.error("Usage: ts-node src/index.ts <time> <source_tz> <target_tz>");
    console.error("Example: ts-node src/index.ts \"2023-08-13T15:30:00\" America/New_York Asia/Tokyo");
    exit(1);
  }
  const [timeStr, sourceTz, targetTz] = args;
  let sourceDate: Date;
  try {
    sourceDate = parseInput(timeStr, sourceTz);
  } catch (e) {
    console.error(e.message);
    exit(1);
  }
  // Convert to target timezone by getting the epoch ms and re‑formatting with Intl
  const formatted = formatInTimezone(sourceDate, targetTz);
  // Determine hour in target tz for emoji
  const hourPart = new Intl.DateTimeFormat("en-US", { hour: "numeric", hour12: false, timeZone: targetTz }).format(sourceDate);
  const hour = parseInt(hourPart, 10);
  const emoji = hourToEmoji(hour);
  console.log(`${formatted} ${emoji}`);
}\n\nif (require.main === module) {
  main();
}\n
