import { convert, getEmoji } from "../src/index";

/**
 * Mock rationale: The tests use fixed ISO timestamps and known IANA timezones.
 * Node's Intl implementation is deterministic for these inputs, so no external
 * services or randomness are required.
 */

describe("getEmoji", () => {
  test("returns sunrise emoji for hour 6", () => {
    expect(getEmoji(6)).toBe("\uD83C\uDF05");
  });
  test("returns sun emoji for hour 13", () => {
    expect(getEmoji(13)).toBe("\u2600\uFE0F");
  });
  test("returns sunset emoji for hour 19", () => {
    expect(getEmoji(19)).toBe("\uD83C\uDF07");
  });
  test("returns moon emoji for hour 23", () => {
    expect(getEmoji(23)).toBe("\uD83C\uDF19");
  });
});

describe("convert", () => {
  test("converts UTC to America/New_York and attaches correct emoji", () => {
    const iso = "2023-01-01T00:00:00Z"; // midnight UTC
    const result = convert(iso, "America/New_York");
    // New York is UTC‑5 on 2022‑12‑31 (standard time)
    expect(result.time).toBe("2022-12-31 19:00");
    expect(result.emoji).toBe("\uD83C\uDF07"); // sunset (19h)
  });

  test("converts UTC to Asia/Tokyo and attaches correct emoji", () => {
    const iso = "2023-08-01T14:30:00Z";
    const result = convert(iso, "Asia/Tokyo");
    // Tokyo is UTC+9, so time becomes 23:30 same day
    expect(result.time).toBe("2023-08-02 23:30");
    expect(result.emoji).toBe("\uD83C\uDF19"); // moon (23h)
  });
});
