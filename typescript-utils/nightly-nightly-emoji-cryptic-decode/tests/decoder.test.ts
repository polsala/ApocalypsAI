import { decodeEmojis } from "../src/decoder";
import assert from "assert";

function arraysEqual(a: any[], b: any[]): boolean {
  return JSON.stringify(a) === JSON.stringify(b);
}

// Test known emojis
const input1 = "🐱 🚀 ❤️";
const expected1 = [["cat"], ["rocket"], ["love", "heart"]];
const result1 = decodeEmojis(input1);
assert(arraysEqual(result1, expected1), "decodeEmojis should return correct meanings");

// Test unknown emoji
const input2 = "🦄";
const expected2 = [[]];
const result2 = decodeEmojis(input2);
assert(arraysEqual(result2, expected2), "unknown emoji should yield empty array");

// Test empty input
const input3 = "";
const expected3: string[][] = [];
const result3 = decodeEmojis(input3);
assert(arraysEqual(result3, expected3), "empty input should return empty array");

console.log("All tests passed.");
