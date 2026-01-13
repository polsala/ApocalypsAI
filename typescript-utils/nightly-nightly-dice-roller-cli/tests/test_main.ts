import * as assert from "assert";
import { parseNotation, rollDice, diceUnicode } from "../src/main";

// Helper to mock Math.random with a predefined sequence
function mockRandom(sequence: number[]) {
  let i = 0;
  const original = Math.random;
  Math.random = () => {
    const value = sequence[i % sequence.length];
    i++;
    return value;
  };
  return () => { Math.random = original; }; // restore function
}

// Test parseNotation
assert.deepStrictEqual(parseNotation("d6"), { count: 1, sides: 6, modifier: 0 });
assert.deepStrictEqual(parseNotation("2d8+3"), { count: 2, sides: 8, modifier: 3 });
assert.deepStrictEqual(parseNotation("4d10-2"), { count: 4, sides: 10, modifier: -2 });

// Mock randomness to produce deterministic rolls: 0.0 => 1, 0.5 => floor(0.5*6)+1 = 4, etc.
const restore = mockRandom([0.0, 0.5, 0.99]); // will be used for three rolls
const result = rollDice("3d6+2");
restore(); // restore original Math.random

// Expected rolls: 1 (0.0*6+1), 4 (0.5*6+1), 7 (0.99*6+1 => floor(5.94)+1=6) -> actually 6
assert.deepStrictEqual(result.rolls, [1, 4, 6]);
assert.strictEqual(result.total, 1 + 4 + 6 + 2);

// Test diceUnicode mapping
assert.strictEqual(diceUnicode(1), "⚀");
assert.strictEqual(diceUnicode(6), "⚅");
assert.strictEqual(diceUnicode(7), "7");

console.log("All tests passed.");

