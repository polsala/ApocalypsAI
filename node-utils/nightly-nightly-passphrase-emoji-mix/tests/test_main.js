const assert = require('assert');
const { execSync } = require('child_process');
const path = require('path');

// Force deterministic randomness: pick first four words and first two emojis
process.env.FAKE_RANDOM = '0,1,2,3,0,1';

const output = execSync('node src/main.js', {
  cwd: path.resolve(__dirname, '..'),
  encoding: 'utf8'
}).trim();

const expected = 'sunny river mountain coffee 🌟🚀';
assert.strictEqual(output, expected);
console.log('All tests passed.');
