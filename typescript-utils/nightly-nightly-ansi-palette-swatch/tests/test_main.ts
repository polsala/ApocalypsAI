import { spawnSync } from 'child_process';
import { generatePalette } from '../src/main';
import * as assert from 'assert';

// Test the generatePalette function directly
const palette = generatePalette();
const rows = palette.split('\n');
assert.strictEqual(rows.length, 16, 'Palette should consist of 16 rows (256 colors / 16 per row)');
assert.ok(palette.includes('\\x1b[38;5;0m  0\\x1b[0m'), 'Palette must contain the escaped sequence for color 0');
assert.ok(palette.includes('\\x1b[38;5;255m255\\x1b[0m'), 'Palette must contain the escaped sequence for color 255');

// Test the CLI output matches the function output
const cliResult = spawnSync('node', ['-e', "console.log(require('../src/main').generatePalette())"], {
  cwd: __dirname + '/..',
  encoding: 'utf8'
});
assert.strictEqual(cliResult.status, 0, 'CLI should exit with status 0');
assert.ok(cliResult.stdout.includes('  0'), 'CLI output should contain the code for color 0');
assert.ok(cliResult.stdout.includes('255'), 'CLI output should contain the code for color 255');

console.log('All tests passed');
