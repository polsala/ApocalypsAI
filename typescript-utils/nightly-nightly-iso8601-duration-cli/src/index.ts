//!/usr/bin/env node

/**
 * Parse an ISO‑8601 duration string (e.g. "P1Y2M3DT4H5M6S") and return a human‑readable description.
 * Supports years, months, weeks, days, hours, minutes, and seconds.
 * If no component is present, returns "0 seconds".
 */
function parseDuration(iso: string): string {
  const regex = /^P(?:(\d+)Y)?(?:(\d+)M)?(?:(\d+)W)?(?:(\d+)D)?(?:T(?:(\d+)H)?(?:(\d+)M)?(?:(\d+(?:\.\d+)?)S)?)?$/;
  const match = iso.toUpperCase().match(regex);
  if (!match) {
    throw new Error(`Invalid ISO‑8601 duration: "${iso}"`);
  }
  const [_, years, months, weeks, days, hours, minutes, seconds] = match;
  const parts: string[] = [];
  if (years) parts.push(`${years} year${Number(years) === 1 ? '' : 's'}`);
  if (months) parts.push(`${months} month${Number(months) === 1 ? '' : 's'}`);
  if (weeks) parts.push(`${weeks} week${Number(weeks) === 1 ? '' : 's'}`);
  if (days) parts.push(`${days} day${Number(days) === 1 ? '' : 's'}`);
  if (hours) parts.push(`${hours} hour${Number(hours) === 1 ? '' : 's'}`);
  if (minutes) parts.push(`${minutes} minute${Number(minutes) === 1 ? '' : 's'}`);
  if (seconds) {
    // Trim trailing zeros for whole numbers
    const secNum = Number(seconds);
    const secStr = Number.isInteger(secNum) ? secNum.toString() : seconds;
    parts.push(`${secStr} second${secNum === 1 ? '' : 's'}`);
  }
  if (parts.length === 0) {
    return '0 seconds';
  }
  return parts.join(', ');
}

// CLI handling
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length !== 1) {
    console.error('Usage: ts-node src/index.ts <ISO‑8601‑duration>');
    process.exit(1);
  }
  try {
    const result = parseDuration(args[0]);
    console.log(result);
  } catch (e) {
    console.error((e as Error).message);
    process.exit(1);
  }
}

export { parseDuration };
