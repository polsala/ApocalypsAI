import { generateAsciiQr } from '../src/index';
import assert from 'assert';

// Mock rationale: we use a deterministic mapping of characters to binary patterns.

// Test single character 'A' (ASCII 65 -> 01000001)
const resultA = generateAsciiQr('A');
const expectedA = ' █    █';
assert.strictEqual(resultA, expectedA, 'ASCII QR for "A" should match expected pattern');

// Test two characters 'AB'
const resultAB = generateAsciiQr('AB');
// 'B' is ASCII 66 -> 01000010 -> ' █   █ '
const expectedAB = ' █    █\n █   █ ';
assert.strictEqual(resultAB, expectedAB, 'ASCII QR for "AB" should match expected multi‑line pattern');

console.log('All tests passed.');
