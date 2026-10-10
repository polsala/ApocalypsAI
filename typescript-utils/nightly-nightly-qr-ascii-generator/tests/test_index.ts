// Mock rationale: No external dependencies; we use Node's built‑in assert.
import assert from "assert";
import { generateAsciiArt } from "../src/index";

// Helper to visualize expected output (spaces are significant)
function visualize(str: string): string {
  return str.replace(/ /g, "·"); // replace spaces with middle dot for readability in comments
}

// Test 1: Single odd character (code 65 – 'A') → empty block
const resultA = generateAsciiArt("A");
const expectedA = "  \n  ";
assert.strictEqual(resultA, expectedA, `Failed on 'A': expected ${visualize(expectedA)} got ${visualize(resultA)}`);

// Test 2: Single even character (code 66 – 'B') → filled block
const resultB = generateAsciiArt("B");
const expectedB = "██\n██";
assert.strictEqual(resultB, expectedB, `Failed on 'B': expected ${visualize(expectedB)} got ${visualize(resultB)}`);

// Test 3: Mixed characters 'AB' → empty block + filled block
const resultAB = generateAsciiArt("AB");
const expectedAB = "  ██\n  ██";
assert.strictEqual(resultAB, expectedAB, `Failed on 'AB': expected ${visualize(expectedAB)} got ${visualize(resultAB)}`);

console.log("All tests passed.");
