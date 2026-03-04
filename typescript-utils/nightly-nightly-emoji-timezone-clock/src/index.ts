export function getHourInTimezone(timeZone: string, date: Date = new Date()): number {
  // Intl.DateTimeFormat can format the hour for a specific time zone.
  const formatter = new Intl.DateTimeFormat("en-US", {
    timeZone,
    hour: "numeric",
    hour12: false,
  });
  const parts = formatter.formatToParts(date);
  const hourPart = parts.find((p) => p.type === "hour");
  if (hourPart) {
    return parseInt(hourPart.value, 10);
  }
  // Fallback to UTC hour if formatting fails (should never happen with valid zones).
  return date.getUTCHours();
}

export function getEmojiForHour(hour: number): string {
  // Normalize hour to 0‑23 range.
  const h = ((hour % 24) + 24) % 24;
  if (h >= 6 && h <= 11) {
    return "\uD83C\uDF05"; // 🌅 sunrise
  }
  if (h >= 12 && h <= 17) {
    return "\uD83C\uDF1E"; // 🌞 daytime sun
  }
  // Night covers 18‑23 and 0‑5.
  return "\uD83C\uDF19"; // 🌙 night moon
}

// CLI entry point.
if (require.main === module) {
  const args = process.argv.slice(2);
  const timeZone = args[0] || "UTC";
  try {
    const hour = getHourInTimezone(timeZone);
    const emoji = getEmojiForHour(hour);
    console.log(`${timeZone} ${hour}:00 ${emoji}`);
  } catch (err) {
    console.error(`Error: Invalid time zone "${timeZone}"`);
    process.exit(1);
  }
}
