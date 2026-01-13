import { strict as assert } from "assert";
import { timeToClockEmoji } from "../src/emojiClock";

function test(time: string, expected: string) {
  const result = timeToClockEmoji(time);
  assert.equal(result, expected, `time ${time} => ${expected}`);
}

// Full hour cases
test("00:00", "🕛");
test("03:00", "🕒");
test("12:00", "🕛");
test("15:00", "🕒");

// Half hour cases
test("02:30", "🕝");
test("14:30", "🕝");

// Edge rounding
test("02:44", "🕝");
test("02:45", "🕒");

// Invalid format should throw
let threw = false;
try {
  timeToClockEmoji("invalid");
} catch {
  threw = true;
}
assert.ok(threw, "should throw on invalid format");

console.log("All tests passed");
