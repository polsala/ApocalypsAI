const { execSync } = require('child_process');
const path = require('path');
const assert = require('assert');
const fs = require('fs');

// Create a temporary mock event file
const mockEvent = {
  changed_files: [
    'src/app.py',
    'lib/util.js',
    'README.md',
    'scripts/deploy.sh',
    'src/main.rs'
  ]
};

const mockEventPath = path.join(__dirname, 'mock_event.json');
fs.writeFileSync(mockEventPath, JSON.stringify(mockEvent), 'utf8');

// Run the action script with the mock event
const env = Object.assign({}, process.env, {
  GITHUB_EVENT_PATH: mockEventPath,
  INPUT_LABEL_PREFIX: 'lang-'
});

const output = execSync('node ../../src/index.js', { env, encoding: 'utf8' });

// Expected labels: lang-python,lang-javascript,lang-shell,lang-rust,lang-markdown
const expected = '::set-output name=labels::lang-python,lang-javascript,lang-shell,lang-rust,lang-markdown';
assert.strictEqual(output.trim(), expected);
console.log('All tests passed');
