import { generatePalette } from '../src/index';
import assert from 'assert';

const output = generatePalette();
assert.ok(output.length > 0, 'Palette output should not be empty');
// Verify that at least one ANSI escape sequence is present
assert.ok(output.includes('\x1b[48;5;0m'), 'Output should contain ANSI color codes');
console.log('All tests passed.');
