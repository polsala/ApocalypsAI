import { strict as assert } from "assert";
import { getHourInTimezone, getEmojiForHour } from "../src/index";

// Helper to create a fixed date (UTC) for reproducible tests.
function fixedDate(isoString: string): Date {
  return new Date(isoString);
}

// Test getHourInTimezone with known time zones.
const testDate = fixedDate("2023-01-01T12:00:00Z"); // UTC noon

// UTC should return 12.
assert.equal(getHourInTimezone("UTC", testDate), 12, "UTC hour should be 12");

// America/New_York is UTC‑5 in winter (no DST), so hour should be 7.
assert.equal(
  getHourInTimezone("America/New_York", testDate),
  7,
  "New York hour should be 7"
);

// Asia/Tokyo is UTC+9, so hour should be 21.
assert.equal(
  getHourInTimezone("Asia/Tokyo", testDate),
  21,
  "Tokyo hour should be 21"
);

// Test emoji mapping.
assert.equal(getEmojiForHour(5), "\uD83C\uDF19", "5 should be night 🌙");
assert.equal(getEmojiForHour(6), "\uD83C\uDF05", "6 should be sunrise 🌅");
assert.equal(getEmojiForHour(11), "\uD83C\uDF05", "11 should be sunrise 🌅");
assert.equal(getEmojiForHour(12), "\uD83C\uDF1E", "12 should be sun 🌞");
assert.equal(getEmojiForHour(17), "\uD83C\uDF1E", "17 should be sun 🌞");
assert.equal(getEmojiForHour(18), "\uD83C\uDF19", "18 should be night 🌙");
assert.equal(getEmojiForHour(23), "\uD83C\uDF19", "23 should be night 🌙");

console.log("All tests passed.");
