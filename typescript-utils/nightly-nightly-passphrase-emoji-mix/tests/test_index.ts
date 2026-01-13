import assert from 'assert';
import generatePassphrase from '../src/index';

/**
 * Mock Math.random to return a predefined sequence.
 * After the sequence is exhausted, it falls back to 0.5 (arbitrary).
 */
function mockRandom(sequence: number[]): void {
  let idx = 0;
  (global as any).Math.random = () => {
    if (idx < sequence.length) {
      return sequence[idx++];
    }
    return 0.5;
  };
}

// Test 1 â deterministic output with a known random sequence
mockRandom([0.1, 0.2, 0.9]); // word1, word2, emoji1
const phrase = generatePassphrase(2, 1);
assert.strictEqual(phrase, 'bravo charlie â¢ï¸', 'Passphrase should match the mocked selection');

// Test 2 â zero words / emojis should return empty string
mockRandom([]);
assert.strictEqual(generatePassphrase(0, 0), '', 'Zero counts should yield empty string');

console.log('All tests passed.');
