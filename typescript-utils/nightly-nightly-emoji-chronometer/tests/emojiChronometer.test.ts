import { generateChrono } from "../src/emojiChronometer";
import assert from "assert";

function arraysEqual(a: any[], b: any[]): boolean {
  return a.length === b.length && a.every((v, i) => v === b[i]);
}

// Test 1: 3 seconds, interval 1 → first three phases
const result1 = generateChrono(3, 1);
assert(arraysEqual(result1, ["🌑", "🌒", "🌓"]), "Test 1 failed");

// Test 2: 10 seconds, interval 2 → five ticks
const result2 = generateChrono(10, 2);
assert(arraysEqual(result2, ["🌑", "🌒", "🌓", "🌔", "🌕"]), "Test 2 failed");

// Test 3: zero seconds should yield empty array
const result3 = generateChrono(0, 1);
assert(arraysEqual(result3, []), "Test 3 failed");

console.log("All tests passed");

