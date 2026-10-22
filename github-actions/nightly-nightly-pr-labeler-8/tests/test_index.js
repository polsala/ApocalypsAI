const assert = require('assert');
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

// Mock event payload with a variety of changed files
const mockEvent = {
  files: [
    'docs/README.md',
    'src/main.py',
    'tests/test_main.py',
    '.github/workflows/build.yml'
  ]
};

// Write mock payload to a temporary file
const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'pr-labeler-'));
const eventFile = path.join(tmpDir, 'event.json');
fs.writeFileSync(eventFile, JSON.stringify(mockEvent));

// Execute the action script with GITHUB_EVENT_PATH pointing to the mock file
const env = { ...process.env, GITHUB_EVENT_PATH: eventFile };
const output = execSync('node src/index.js', { env, encoding: 'utf8' }).trim();

// Expected labels based on the heuristics defined in src/index.js
const expected = JSON.stringify(['documentation', 'python', 'tests', 'ci']);
assert.strictEqual(output, expected, `Expected ${expected} but got ${output}`);

console.log('All tests passed');
