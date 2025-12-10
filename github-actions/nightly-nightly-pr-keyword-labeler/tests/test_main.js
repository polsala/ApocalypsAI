const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const assert = require('assert');

// Create a temporary mock event JSON
const mockEvent = {
  pull_request: {
    number: 42,
    title: 'Add zombie feature to the apocalypse engine',
    body: 'This PR introduces a new zombie mechanic and fixes a bug.'
  }
};
const eventPath = path.join(__dirname, 'mock_event.json');
fs.writeFileSync(eventPath, JSON.stringify(mockEvent), { encoding: 'utf8' });

// Set required environment variables for the action
process.env.GITHUB_EVENT_PATH = eventPath;
process.env.INPUT_TOKEN = 'ghp_dummyToken';
process.env.INPUT_MAPPING = `bug:🐞 Bug\nfeature:✨ Feature\nzombie:🧟‍♂️ Zombie`;

// Execute the action script
const output = execSync('node ../../src/main.js', { encoding: 'utf8' });

// Expected labels (order follows mapping definition)
const expected = '::set-output name=added_labels::🐞 Bug,✨ Feature,🧟‍♂️ Zombie';
assert.ok(output.includes(expected), `Output should contain expected label string.\nGot: ${output}`);
console.log('Test passed: correct labels detected and output.');
