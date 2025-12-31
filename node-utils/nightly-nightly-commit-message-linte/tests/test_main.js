const { execSync } = require('child_process');
const path = require('path');

function run(args, input) {
  const script = path.join(__dirname, '..', 'src', 'main.js');
  const cmd = `node ${script} ${args}`;
  try {
    const stdout = execSync(cmd, { input, encoding: 'utf8' });
    return { code: 0, stdout, stderr: '' };
  } catch (e) {
    return { code: e.status || 1, stdout: e.stdout || '', stderr: e.stderr || '' };
  }
}

function assert(condition, message) {
  if (!condition) {
    console.error('Test failed:', message);
    process.exit(1);
  }
}

// 1. Valid commit passes
let res = run('', 'feat(parser): add new parsing logic');
assert(res.code === 0, 'Valid commit should exit with code 0');
assert(/looks good/.test(res.stdout), 'Valid commit should contain success message');

// 2. Invalid type fails
res = run('', 'unknown: something');
assert(res.code !== 0, 'Invalid type should exit with non‑zero code');
assert(/Invalid commit type/.test(res.stderr), 'Error should mention invalid commit type');

// 3. Suggest emoji works deterministically
res = run('--suggest-emoji', 'fix: correct typo');
assert(res.code === 0, '--suggest-emoji should still succeed');
assert(/🚀/.test(res.stdout), 'Suggested emoji should be the deterministic 🚀');

console.log('All tests passed.');
process.exit(0);
