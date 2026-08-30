const assert = require('assert');
const childProcess = require('child_process');

// Save originals to restore later
const originalExecSync = childProcess.execSync;
const originalConsoleLog = console.log;
const originalEnv = { ...process.env };

// Mock data
const mockHash = 'deadbeef1234567890abcdef';
const mockMessage = 'Initial commit';
const mockEmoji = '🚀'; // First emoji in the list

// Override execSync to return deterministic values
childProcess.execSync = (cmd) => {
  if (cmd.startsWith('git rev-parse')) {
    return Buffer.from(mockHash);
  }
  if (cmd.startsWith('git log')) {
    return Buffer.from(mockMessage);
  }
  // For any other git command (e.g., commit --amend), just return empty buffer
  return Buffer.from('');
};

// Mock Math.random to always pick the first emoji (index 0)
const originalMathRandom = Math.random;
Math.random = () => 0;

let capturedOutput = '';
console.log = (msg) => {
  capturedOutput += msg + '\n';
};

// Set input env variable to false (no commit)
process.env.INPUT_COMMIT = 'false';

// Require the action script (it runs immediately)
require('../src/main.js');

// Verify that the output contains the expected set-output line
const expectedOutput = `::set-output name=new_message::${mockMessage} ${mockEmoji}`;
assert.ok(capturedOutput.includes(expectedOutput), 'Output does not contain expected new_message');

// Clean up / restore originals
childProcess.execSync = originalExecSync;
console.log = originalConsoleLog;
process.env = originalEnv;
Math.random = originalMathRandom;

console.log('All tests passed for nightly-commit-emoji-enhancer');
