import { encodeWithEmoji, rot13 } from "../src/main";

// Mock rationale: No external dependencies; tests are pure functions.

function expectEqual(actual: string, expected: string): void {
  if (actual !== expected) {
    throw new Error(`Assertion failed. Expected: ${expected}, Got: ${actual}`);
  }
}

// Test ROT13 correctness
const rot13Tests: Array<[string, string]> = [
  ["Hello", "Uryyb"],
  ["abcdefghijklmnopqrstuvwxyz", "nopqrstuvwxyzabcdefghijklm"],
  ["ABCDEFGHIJKLMNOPQRSTUVWXYZ", "NOPQRSTUVWXYZABCDEFGHIJKLM"],
  ["123!", "123!"],
];
for (const [input, expected] of rot13Tests) {
  expectEqual(rot13(input), expected);
}

// Test emojiâdecorated output
// Emoji list used in implementation: ["ð","ð","ð","ð¥","ð§","ð","ð²","ð§©","â¡","ðª"]
// For input "Hello" -> ROT13 "Uryyb"
// U (85) %10 =5 -> "ð§"
// r (114)%10 =4 -> "ð¥"
// y (121)%10 =1 -> "ð"
// y (121)%10 =1 -> "ð"
// b (98) %10 =8 -> "â¡"
const expectedHello = "ð§Uð¥rðyðyâ¡b";
expectEqual(encodeWithEmoji("Hello"), expectedHello);

// Empty string should return empty
expectEqual(encodeWithEmoji(""), "");

console.log("All tests passed.");

