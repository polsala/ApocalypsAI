const { execSync } = require('child_process');
const assert = require('assert');

function runAction(title) {
  const env = Object.assign({}, process.env, { INPUT_TITLE: title });
  const output = execSync('node src/index.js', { env, encoding: 'utf8' });
  const match = output.match(/::set-output name=emoji::(.+)/);
  return match ? match[1].trim() : null;
}

// Positive case
let emoji = runAction('Add new feature to dashboard');
assert.strictEqual(emoji, '👍', 'Positive title should yield 👍');

// Negative case
emoji = runAction('Remove deprecated API');
assert.strictEqual(emoji, '👎', 'Negative title should yield 👎');

// Neutral case
emoji = runAction('Refactor codebase');
assert.strictEqual(emoji, '🤝', 'Neutral title should yield 🤝');

console.log('All tests passed');
