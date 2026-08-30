const assert = require('assert');
const { spawnSync } = require('child_process');
const path = require('path');
const { generateStoryboard } = require('../src/index');

// ---- Core function tests ---------------------------------------------------

// Basic mapping of known words and unknown fallback
assert.strictEqual(
  generateStoryboard('love fire unknown'),
  '❤️ 🔥 ❓',
  'Basic mapping failed'
);

// Plural handling, punctuation stripping, and mixed known/unknown words
assert.strictEqual(
  generateStoryboard('Cats, dogs! and coffee.'),
  '🐱 🐶 ❓ ☕',
  'Plural and punctuation handling failed'
);

// Empty or non‑string input should yield an empty string
assert.strictEqual(
  generateStoryboard(''),
  '',
  'Empty string handling failed'
);
assert.strictEqual(
  generateStoryboard(null),
  '',
  'Null input handling failed'
);

// ---- CLI tests ------------------------------------------------------------

const cliPath = path.resolve(__dirname, '..', 'src', 'index.js');
const result = spawnSync('node', [cliPath, 'happy sad moon'], { encoding: 'utf8' });
assert.strictEqual(result.stdout.trim(), '😊 😢 🌙', 'CLI output mismatch');
assert.strictEqual(result.status, 0, 'CLI exited with non‑zero status');

console.log('All tests passed');
