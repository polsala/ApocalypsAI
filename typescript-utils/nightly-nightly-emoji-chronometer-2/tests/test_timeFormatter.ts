import { formatTime } from "../src/timeFormatter";
import { strict as assert } from "assert";

/**
 * Helper to create a Date with a fixed timestamp.
 * The mock rationale: we avoid any external time source to keep tests deterministic.
 */
function makeFixedDate(hours: number, minutes: number, seconds: number): Date {
  const date = new Date();
  date.setHours(hours, minutes, seconds, 0);
  return date;
}

// Test cases: each entry maps a fixed time to the expected emoji string.
const cases: Array<{ time: Date; expected: string }> = [
  {
    time: makeFixedDate(0, 0, 0),
    expected: "0️⃣0️⃣0️⃣0️⃣0️⃣0️⃣",
  },
  {
    time: makeFixedDate(9, 5, 3),
    expected: "0️⃣9️⃣0️⃣5️⃣0️⃣3️⃣",
  },
  {
    time: makeFixedDate(12, 34, 56),
    expected: "1️⃣2️⃣3️⃣4️⃣5️⃣6️⃣",
  },
  {
    time: makeFixedDate(23, 59, 59),
    expected: "2️⃣3️⃣5️⃣9️⃣5️⃣9️⃣",
  },
];

for (const { time, expected } of cases) {
  const result = formatTime(time);
  assert.equal(result, expected, `Failed for time ${time.toTimeString()}`);
}

console.log("All emoji‑chronometer tests passed.");
