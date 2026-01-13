import { visualizeHash } from '../src/hashVisualizer';
import assert from 'assert';

// Mock rationale: we use a fixed input and compare against a preâcomputed expected string.
const input = 'test';
// Expected visual hash for the string "test" (computed with the same algorithm).
const expected = 'ââââââââââââââââ
ââââââââââââââââ
ââââââââââââââââ
ââââââââââââââââ';

const actual = visualizeHash(input);
assert.strictEqual(actual, expected, 'Visual hash does not match expected output');
console.log('All tests passed.');

