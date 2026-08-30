import { textToBlockPattern } from '../src/main';
import assert from 'assert';

/**
 * Normalise line endings for cross‑platform consistency.
 */
function normalize(str: string): string {
  return str.replace(/\r/g, '');
}

// Test pattern for character 'A' (ASCII 65 -> 01000001)
const resultA = normalize(textToBlockPattern('A'));
const expectedA = ' █      █';
assert.strictEqual(resultA, expectedA, 'Pattern for "A" should match expected block representation');

// Test pattern for characters 'A' followed by 'B'
// 'B' is ASCII 66 -> 01000010 -> " █    █ "
const resultAB = normalize(textToBlockPattern('AB'));
const expectedAB = ' █      █\n █    █ ';
assert.strictEqual(resultAB, expectedAB, 'Pattern for "AB" should match expected block representation');

console.log('All tests passed.');
