#!/usr/bin/env node

function parseDuration(str) {
  const regex = /(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?/i;
  const match = regex.exec(str);
  if (!match) return null;
  const hours = parseInt(match[1] || '0', 10);
  const minutes = parseInt(match[2] || '0', 10);
  const seconds = parseInt(match[3] || '0', 10);
  return hours * 3600 + minutes * 60 + seconds;
}

function formatDuration(totalSeconds) {
  totalSeconds = Math.floor(totalSeconds);
  const h = Math.floor(totalSeconds / 3600);
  const m = Math.floor((totalSeconds % 3600) / 60);
  const s = totalSeconds % 60;
  const parts = [];
  if (h) parts.push(`${h}h`);
  if (m) parts.push(`${m}m`);
  if (s || parts.length === 0) parts.push(`${s}s`);
  return parts.join(' ');
}

function printHelp() {
  console.log('Usage: node src/index.js <parse|format> <value>');
  console.log('  parse   Convert duration string (e.g., 2h30m) to seconds');
  console.log('  format  Convert seconds to human readable string');
}

if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length !== 2) {
    printHelp();
    process.exit(1);
  }
  const [cmd, val] = args;
  if (cmd === 'parse') {
    const secs = parseDuration(val);
    if (secs === null) {
      console.error('Invalid duration format');
      process.exit(1);
    }
    console.log(secs);
  } else if (cmd === 'format') {
    const num = Number(val);
    if (isNaN(num)) {
      console.error('Invalid number of seconds');
      process.exit(1);
    }
    console.log(formatDuration(num));
  } else {
    printHelp();
    process.exit(1);
  }
}

module.exports = { parseDuration, formatDuration };
