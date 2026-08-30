#!/usr/bin/env node

/**
 * Nightly Emoji Clock
 *
 * Given a time (HH:MM) or the current system time, returns the nearest
 * clock‑face emoji (🕐‑🕛). Minutes >= 30 round up to the next hour.
 */

/** Parse a HH:MM string into hour and minute numbers. */
function parseTime(str) {
  const match = /^(\d{1,2}):(\d{2})$/.exec(str);
  if (!match) throw new Error('Invalid time format, expected HH:MM');
  const hour = parseInt(match[1], 10);
  const minute = parseInt(match[2], 10);
  if (hour < 0 || hour > 23) throw new Error('Invalid hour value');
  if (minute < 0 || minute > 59) throw new Error('Invalid minute value');
  return { hour, minute };
}

/** Return the clock emoji nearest to the supplied time. */
function nearestClockEmoji(timeStr) {
  let hour, minute;
  if (timeStr) {
    ({ hour, minute } = parseTime(timeStr));
  } else {
    const now = new Date();
    hour = now.getHours();
    minute = now.getMinutes();
  }

  // Convert to 12‑hour clock (1‑12)
  const hour12 = hour % 12 === 0 ? 12 : hour % 12;
  // Round based on minutes
  const nearestHour = minute >= 30 ? (hour12 % 12) + 1 : hour12;

  const emojiMap = {
    1: '🕐',
    2: '🕑',
    3: '🕒',
    4: '🕓',
    5: '🕔',
    6: '🕕',
    7: '🕖',
    8: '🕗',
    9: '🕘',
    10: '🕙',
    11: '🕚',
    12: '🕛'
  };
  return emojiMap[nearestHour];
}

// CLI entry point
if (require.main === module) {
  const arg = process.argv[2];
  try {
    const emoji = nearestClockEmoji(arg);
    console.log(emoji);
  } catch (e) {
    console.error('Error:', e.message);
    process.exit(1);
  }
}

module.exports = { nearestClockEmoji, parseTime };
