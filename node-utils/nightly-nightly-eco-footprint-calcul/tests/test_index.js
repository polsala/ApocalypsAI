const { execSync } = require('child_process');
const assert = require('assert');

function run(args) {
  // Execute the CLI with given arguments and capture stdout as UTF‑8 string
  return execSync(`node ${__dirname}/../src/index.js ${args}`, { encoding: 'utf8' });
}

// Test 1: calculation correctness with known inputs
const output = run('--miles 1000 --kwh 500 --flight-hours 2');
// Expected: 1000*0.411 + 500*0.475 + 2*90 = 828.5 kg
assert.ok(output.includes('828.50 kg'), `Unexpected calculation result: ${output.trim()}`);

// Test 2: help flag displays usage information
const helpOutput = run('-h');
assert.ok(helpOutput.includes('Usage:'), 'Help output missing expected Usage section');

console.log('All tests passed.');
process.exit(0);
