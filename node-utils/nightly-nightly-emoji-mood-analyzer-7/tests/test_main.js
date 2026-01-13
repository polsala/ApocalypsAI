// tests/test_main.js
// Tests for nightly-emoji-mood-analyzer

const assert = require('assert');
const { spawnSync } = require('child_process');

function runCLI(input) {
  // Execute the CLI synchronously, feeding input via stdin
  const result = spawnSync('node', ['src/main.js'], {
    input: input,
    encoding: 'utf-8'
  });
  // Mock rationale: Using spawnSync ensures deterministic, offline execution.
  if (result.status !== 0) {
    // If the process exited with error, capture stderr for debugging
    throw new Error(`CLI exited with code ${result.status}: ${result.stderr}`);
  }
  return result.stdout.trim();
}

// Test cases
const cases = [
  { input: 'I love sunny days', expected: 'ð' },
  { input: 'I hate rainy weather', expected: 'ð¢' },
  { input: 'It is a day', expected: 'ð' },
  { input: 'Good and bad things happen', expected: 'ð' },
  { input: 'Fantastic! Excellent! Wonderful!', expected: 'ð' },
  { input: 'Terrible, horrible, awful', expected: 'ð¢' }
];

for (const { input, expected } of cases) {
  const output = runCLI(input + '
'); // ensure newline termination
  assert.strictEqual(output, expected, `Input: "${input}" should yield ${expected}`);
}

console.log('All tests passed.');

