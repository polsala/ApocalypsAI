import { parseNotation, rollDice, dieFace, formatResult } from '../src/main';
import assert from 'assert';

// Mock rationale: replace Math.random with a deterministic function so rolls are predictable.
const originalRandom = Math.random;
Math.random = () => 0; // always yields the lowest possible roll (1)

// Test parsing of a typical notation
const parsed = parseNotation('2d6+3');
assert.deepStrictEqual(parsed, { count: 2, sides: 6, modifier: 3 }, 'parseNotation failed');

// Test deterministic rolling (should produce two 1s)
const rolls = rollDice(parsed);
assert.deepStrictEqual(rolls, [1, 1], 'rollDice deterministic mock failed');

// Test Unicode face conversion
assert.strictEqual(dieFace(1), '⚀', 'dieFace 1');
assert.strictEqual(dieFace(5), '⚄', 'dieFace 5');
assert.strictEqual(dieFace(7), '7', 'dieFace fallback for >6');

// Test final formatting string
const output = formatResult(parsed, rolls);
assert.strictEqual(output, '🎲 2d6+3 → [⚀ ⚀] + 3 = 5', 'formatResult output mismatch');

// Restore original Math.random to avoid side effects for other tests
Math.random = originalRandom;

console.log('All tests passed');
