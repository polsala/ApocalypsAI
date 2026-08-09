const assert = require('assert');
const { generateQR } = require('../src/index.js');

// Mock rationale: we use a fixed input and compare against the exact expected pattern.
// This ensures the algorithm is deterministic and does not rely on external services.

// Test single character 'A' (ASCII 65 => binary 01000001)
const expectedA = ' █    █';
assert.strictEqual(generateQR('A'), expectedA, "QR for 'A' should match expected pattern");

// Test two‑character string 'AB'
// 'B' is ASCII 66 => binary 01000010 => ' █   █ '
const expectedAB = expectedA + '\n' + ' █   █ ';
assert.strictEqual(generateQR('AB'), expectedAB, "QR for 'AB' should match expected multi‑line pattern");

console.log('All tests passed.');
