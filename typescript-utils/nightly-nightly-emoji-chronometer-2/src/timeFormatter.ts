/**
 * Map of decimal digits to their corresponding emoji representations.
 */
const digitEmoji: Record<string, string> = {
  "0": "0️⃣",
  "1": "1️⃣",
  "2": "2️⃣",
  "3": "3️⃣",
  "4": "4️⃣",
  "5": "5️⃣",
  "6": "6️⃣",
  "7": "7️⃣",
  "8": "8️⃣",
  "9": "9️⃣",
};

/**
 * Convert a numeric string (e.g., "12") into its emoji representation.
 */
function digitsToEmoji(numStr: string): string {
  return numStr.split("").map((ch) => digitEmoji[ch] ?? ch).join("");
}

/**
 * Format a Date object as an emoji clock string: HH:MM:SS → emoji digits.
 *
 * @param date Date instance to format.
 * @returns Emoji representation of the time.
 */
export function formatTime(date: Date): string {
  const pad = (n: number) => n.toString().padStart(2, "0");
  const hours = pad(date.getHours());
  const minutes = pad(date.getMinutes());
  const seconds = pad(date.getSeconds());

  // Combine with colon separators, then replace each digit.
  const timeStr = `${hours}:${minutes}:${seconds}`;
  return digitsToEmoji(timeStr.replace(/:/g, ""));
}
