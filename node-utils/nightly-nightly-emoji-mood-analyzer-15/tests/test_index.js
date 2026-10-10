const {execSync} = require('child_process');
const assert = require('assert');
const path = require('path');

function run(input) {
  const cmd = `node ${path.join(__dirname, '..', 'src', 'index.js')} "${input}"`;
  return execSync(cmd, {encoding: 'utf8'}).trim();
}

// Test happy mood
assert.strictEqual(run('I love sunny days and feel great'), '😊', 'Happy mood should return 😊');

// Test sad mood
assert.strictEqual(run('I am sad and feeling terrible'), '😢', 'Sad mood should return 😢');

// Test angry mood
assert.strictEqual(run('I am angry and furious about this'), '😠', 'Angry mood should return 😠');

// Test surprised mood
assert.strictEqual(run('Wow! That was unexpected'), '😲', 'Surprised mood should return 😲');

// Test neutral mood (no keywords)
assert.strictEqual(run('Just an ordinary statement'), '😐', 'Neutral mood should return 😐');

console.log('All tests passed');
