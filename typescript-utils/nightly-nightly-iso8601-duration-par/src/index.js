function parseISO8601Duration(input) {
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

function formatDuration(d) {
  const parts = [];
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

module.exports = { parseISO8601Duration, formatDuration };
