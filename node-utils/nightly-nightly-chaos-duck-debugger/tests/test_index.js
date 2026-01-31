const { spawn } = require('child_process');
const path = require('path');

// Mock rationale: We mock by capturing stdout and ensuring output contains expected strings.

test('CLI outputs a debugging scenario and rubber duck hint', (done) => {
  const cliPath = path.join(__dirname, '../src/index.js');
  const child = spawn('node', [cliPath]);

  let stdout = '';
  child.stdout.on('data', (data) => {
    stdout += data.toString();
  });

  child.on('close', () => {
    expect(stdout).toContain('🚨 DEBUGGING CHALLENGE 🚨');
    expect(stdout).toContain('🦆 Rubber Duck says:');
    done();
  });
});
