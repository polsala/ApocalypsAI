const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const assert = require('assert');

function runTest({ title, keywords, label, expected }) {
  // Create a temporary event JSON file
  const event = { pull_request: { title } };
  const eventPath = path.join(__dirname, 'event.json');
  fs.writeFileSync(eventPath, JSON.stringify(event), 'utf8');

  const env = {
    ...process.env,
    GITHUB_EVENT_PATH: eventPath,
    INPUT_KEYWORDS: keywords,
    INPUT_LABEL: label,
  };

  // Execute the action script
  const output = execSync('node ../../src/index.js', { env, encoding: 'utf8' });
  const match = output.trim().match(/::set-output name=apocalypse_label::(.*)/);
  const actual = match ? match[1] : null;

  // Clean up
  fs.unlinkSync(eventPath);

  // Assertion
  assert.strictEqual(actual, expected, `Expected output '${expected}' but got '${actual}'`);
}

// Positive case: title contains a keyword
runTest({
  title: 'The world ends soon',
  keywords: 'world, end',
  label: 'doomsday',
  expected: 'doomsday',
});

// Negative case: no keyword match
runTest({
  title: 'A calm day in the office',
  keywords: 'world, end',
  label: 'doomsday',
  expected: '',
});

console.log('All tests passed.');
