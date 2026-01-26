export interface Duration {
  hours: number;
  minutes: number;
  seconds: number;
}

/**
 * Parses a subset of ISO 8601 duration strings.
 * Supports hours, minutes, seconds (e.g., PT1H30M45S).
 * Returns an object with numeric values (defaults to 0).
 */
export function parseISO8601Duration(input: string): Duration {
  const regex = /^P(?:T)?(?:(\\d+)H)?(?:(\\d+)M)?(?:(\\d+(?:\\.\\d+)?)S)?$/i;
  const match = input.match(regex);
  if (!match) {
    throw new Error("Invalid ISO 8601 duration format");
  }
  const hours = match[1] ? parseInt(match[1], 10) : 0;
  const minutes = match[2] ? parseInt(match[2], 10) : 0;
  const seconds = match[3] ? parseFloat(match[3]) : 0;
  return { hours, minutes, seconds };
}

/**
 * Formats a Duration object into a human‑readable string.
 * Example: {hours:1, minutes:30, seconds:0} => "1 hour, 30 minutes"
 */
export function formatDuration(d: Duration): string {
  const parts: string[] = [];
  if (d.hours) {
    parts.push(d.hours + " hour" + (d.hours !== 1 ? "s" : ""));
  }
  if (d.minutes) {
    parts.push(d.minutes + " minute" + (d.minutes !== 1 ? "s" : ""));
  }
  if (d.seconds) {
    const secStr = Number.isInteger(d.seconds) ? d.seconds.toString() : d.seconds.toFixed(2);
    parts.push(secStr + " second" + (d.seconds !== 1 ? "s" : ""));
  }
  return parts.length ? parts.join(", ") : "0 seconds";
}

// CLI entry point
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length !== 1) {
    console.error("Usage: node src/index.js <ISO8601-duration>");
    process.exit(1);
  }
  try {
    const dur = parseISO8601Duration(args[0]);
    console.log(formatDuration(dur));
  } catch (e) {
    console.error("Error:", e.message);
    process.exit(1);
  }
}
