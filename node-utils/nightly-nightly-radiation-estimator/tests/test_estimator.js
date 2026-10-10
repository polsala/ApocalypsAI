const { execSync } = require('child_process');
const path = require('path');
const assert = require('assert');

// Mock rationale: deterministic inputs, no external dependencies
function run(args) {
  const cmd = `node ${path.join(__dirname, '..', 'src', 'index.js')} ${args}`;
  return execSync(cmd, { encoding: 'utf8' }).trim();
}

// Test safe dose
let output = run('--distance 5 --time 2 --rate 10');
assert(output.includes('Total dose: 20'), 'Dose calculation failed');
assert(output.includes('Safe'), 'Safety status incorrect');

// Test unsafe dose
output = run('--distance 0 --time 5 --rate 30');
assert(output.includes('Total dose: 150'), 'Dose calculation failed');
assert(output.includes('Unsafe'), 'Safety status incorrect');

console.log('All tests passed');
