import { parseDiceNotation, rollDice, asciiDie } from "../src/main";

/**
 * Helper to create a deterministic random function.
 * Returns the values from `seq` in order, looping if necessary.
 */
function mockRandomSequence(seq: number[]): () => number {
  let i = 0;
  return () => {
    const val = seq[i % seq.length];
    i++;
    return val;
  };
}

// Test parsing of complex notation
const spec = parseDiceNotation("3d8-2");
if (spec.count !== 3 || spec.sides !== 8 || spec.modifier !== -2) {
  throw new Error("parseDiceNotation failed");
}

// Test deterministic rolling (always returns 1 because Math.random() => 0)
const deterministicRand = mockRandomSequence([0]); // 0 => roll of 1
const rolls = rollDice(2, 6, deterministicRand);
if (rolls[0] !== 1 || rolls[1] !== 1) {
  throw new Error("rollDice deterministic test failed");
}

// Test ASCII art for a standard die (value 5)
const art = asciiDie(5, 6);
const expected = [
  "+-------+",
  "| *   * |",
  "|   *   |",
  "| *   * |",
  "+-------+",
].join("\n");
if (art !== expected) {
  throw new Error("asciiDie test failed");
}

// Mock rationale: using a fixed random sequence ensures the tests run offline and are repeatable.
console.log("All tests passed");
