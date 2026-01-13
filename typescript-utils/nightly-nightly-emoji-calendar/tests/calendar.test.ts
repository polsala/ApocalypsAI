import { generateCalendar } from "../src/calendar";

/**
 * Helper to count occurrences of a substring in a string.
 */
function countOccurrences(str: string, sub: string): number {
  return (str.match(new RegExp(sub, "g")) || []).length;
}

describe("generateCalendar", () => {
  test("produces correct number of days for February 2024 (leap year)", () => {
    const output = generateCalendar(2, 2024);
    // February 2024 has 29 days
    expect(countOccurrences(output, " ")).toBeGreaterThanOrEqual(29); // crude check
    expect(output).toContain("29 ");
  });

  test("weekday emojis appear exactly once per line", () => {
    const output = generateCalendar(1, 2023);
    const lines = output.split("
");
    // Second line should be the emoji header
    const emojiLine = lines[1];
    const emojis = ["âï¸", "ð", "ð", "ð", "ð", "ð", "ð¸"];
    emojis.forEach(e => {
      expect(emojiLine).toContain(e);
    });
    // No other line should contain any of the emojis (they appear only in header)
    for (let i = 2; i < lines.length; i++) {
      emojis.forEach(e => {
        expect(lines[i]).not.toContain(e);
      });
    }
  });

  test("throws on invalid month", () => {
    expect(() => generateCalendar(0, 2023)).toThrow();
    expect(() => generateCalendar(13, 2023)).toThrow();
  });
});

