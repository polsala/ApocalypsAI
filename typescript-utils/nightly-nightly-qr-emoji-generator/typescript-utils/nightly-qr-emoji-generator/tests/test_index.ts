import { generatePseudoQR } from '../src/index';
import * as assert from 'assert';

// Test single character 'A' (U+0041 => 01000001)
const resultA = generatePseudoQR('A');
const expectedA = ' █\n  \n  \n █';
assert.strictEqual(resultA, expectedA, 'QR for "A" should match expected pattern');

// Test two characters to ensure grid layout works
const resultAB = generatePseudoQR('AB');
const lines = resultAB.split('\n');
assert.strictEqual(lines.length, 4, 'AB should produce 4 rows (grid size 2×2 blocks)');
assert.ok(lines[0].includes(' █'), 'First line should contain block for "A"');
assert.ok(lines[0].includes('██'), 'First line should contain block for "B"');

console.log('All tests passed');
