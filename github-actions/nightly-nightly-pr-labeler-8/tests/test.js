const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// Helper to run the action script with a mocked GITHUB_EVENT_PATH
function runActionWithTitle(prTitle) {
  // Create a temporary event JSON file
  const event = {
    pull_request: {
      title: prTitle
    }
  };
  const tmpDir = fs.mkdtempSync(path.join(require('os').tmpdir(), 'pr-labeler-'));
  const eventFile = path.join(tmpDir, 'event.json');
  fs.writeFileSync(eventFile, JSON.stringify(event), 'utf8');

  // Set env var and execute the script
  const env = Object.assign({}, process.env, { GITHUB_EVENT_PATH: eventFile });
  const output = execSync('node src/index.js', { env, encoding: 'utf8' }).trim();
  // Clean up
  fs.rmSync(tmpDir, { recursive: true, force: true });
  return output;
}

// Mock‑randomness for reproducibility – override Math.random
const originalRandom = Math.random;
Math.random = () => 0.42; // deterministic index into emojis array (will pick "📚")

// Test cases
const cases = [
  { title: 'Fix bug in authentication', expected: ['bug', '📚'] },
  { title: 'Add new feature for export', expected: ['enhancement', '📚'] },
  { title: 'Update documentation for API', expected: ['documentation', '📚'] },
  { title: 'Refactor codebase', expected: ['📚'] }
];

let allPassed = true;
for (const c of cases) {
  const out = runActionWithTitle(c.title);
  const match = out.match(/::set-output name=labels::(.+)/);
  const labels = match ? match[1].split(',').map(l => l.trim()) : [];
  const missing = c.expected.filter(e => !labels.includes(e));
  if (missing.length) {
    console.error(`FAIL: title "${c.title}" missing labels ${missing.join(', ')}`);
    allPassed = false;
  } else {
    console.log(`PASS: title "${c.title}" produced ${labels.join(', ')}`);
  }
}

// Restore original Math.random
Math.random = originalRandom;

if (!allPassed) {
  process.exit(1);
}
