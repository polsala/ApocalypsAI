const assert = require('assert');
const { execSync } = require('child_process');

function run(password) {
  // Escape double quotes for the shell command
  const escaped = password.replace(/"/g, '\\"');
  const cmd = `node src/index.js "${escaped}"`;
  return execSync(cmd, { encoding: 'utf8' }).trim();
}

// Test cases: [password, expectedOutput]
const cases = [
  ['', 'Very Weak 😱'],
  ['abc', 'Very Weak 😱'],
  ['abcdef', 'Weak 🙈'],
  ['123456', 'Weak 🙈'],
  ['abc12345', 'Moderate 😐'],
  ['Abc12345!', 'Strong 💪'],
  ['Abcdef12345!@', 'Very Strong 🚀']
];

cases.forEach(([pwd, expected]) => {
  const result = run(pwd);
  assert.strictEqual(result, expected, `Password: "${pwd}" expected "${expected}" but got "${result}"`);
});

console.log('All tests passed.');
