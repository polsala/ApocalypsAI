// nightly-emoji-mood-analyzer tests
const { execSync } = require('child_process');
const assert = require('assert');

function run(input) {
  // Execute the CLI with given stdin and capture stdout
  return execSync('node src/main.js', { input, encoding: 'utf8' }).trim();
}

// Test strong positive sentiment
assert.strictEqual(run('I love this awesome project'), 'ð');

// Test mild negative sentiment
assert.strictEqual(run('I am sad and angry'), 'ð');

// Test neutral sentiment
assert.strictEqual(run('Just an ordinary day'), 'ð');

console.log('All tests passed');

