const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

// Mock PR event JSON
const event = {
  pull_request: {
    title: "Add zombie apocalypse feature"
  }
};

// Write temporary event file
const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'pr-event-'));
const eventPath = path.join(tmpDir, 'event.json');
fs.writeFileSync(eventPath, JSON.stringify(event), 'utf8');

// Set environment variables for the action
process.env['INPUT_KEYWORD'] = 'zombie';
process.env['INPUT_LABEL'] = '🧟‍♂️-zombie';
process.env['GITHUB_EVENT_PATH'] = eventPath;

// Execute the action script
const output = execSync('node src/index.js', { encoding: 'utf8' });

// Verify that the output contains the expected label
if (!output.includes('::set-output name=label::🧟‍♂️-zombie')) {
  console.error('Test failed: expected label not set');
  process.exit(1);
} else {
  console.log('Test passed');
}

// Clean up
fs.unlinkSync(eventPath);
fs.rmdirSync(tmpDir);
