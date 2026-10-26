#!/usr/bin/env node

/**
 * Map of hour numbers (1‑12) to their clock face emojis.
 */
const hourEmojiMap = {
  1: "🕐",
  2: "🕑",
  3: "🕒",
  4: "🕓",
  5: "🕔",
  6: "🕕",
  7: "🕖",
  8: "🕗",
  9: "🕘",
  10: "🕙",
  11: "🕚",
  12: "🕛"
};

/**
 * Convert a time string (HH:MM) or the current time to a sequence of clock emojis.
 * @param {string|undefined} timeStr Optional time in "HH:MM" 24‑hour format.
 * @returns {string} Emoji representation, e.g. "🕑🕖".
 */
function timeToEmoji(timeStr) {
  // Use UTC to avoid local timezone surprises.
  const now = timeStr ? new Date(`1970-01-01T${timeStr}:00Z`) : new Date();
  let hours = now.getUTCHours();
  let minutes = now.getUTCMinutes();

  // Round minutes to the nearest 5.
  minutes = Math.round(minutes / 5) * 5;
  if (minutes === 60) {
    minutes = 0;
    hours = (hours + 1) % 24;
  }

  // Convert to 12‑hour clock for emoji mapping.
  const hour12 = hours % 12 === 0 ? 12 : hours % 12;
  const hourEmoji = hourEmojiMap[hour12];

  // Minute index: 0 (no minute emoji) or 1‑11.
  const minuteIdx = (minutes / 5) % 12;
  const minuteEmoji = minuteIdx === 0 ? "" : hourEmojiMap[minuteIdx];

  return hourEmoji + minuteEmoji;
}

if (require.main === module) {
  const arg = process.argv[2];
  console.log(timeToEmoji(arg));
}

module.exports = { timeToEmoji };
