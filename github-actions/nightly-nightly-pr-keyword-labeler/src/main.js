const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// Helper to read action inputs (GitHub sets them as env vars INPUT_<NAME>)
function getInput(name) {
  const envName = `INPUT_${name.toUpperCase()}`;
  return process.env[envName] || '';
}

function parseMapping(mappingStr) {
  const map = {};
  const lines = mappingStr.split(/\r?\n/).filter(l => l.trim() !== '');
  for (const line of lines) {
    const idx = line.indexOf(':');
    if (idx === -1) continue; // skip malformed lines
    const key = line.slice(0, idx).trim().toLowerCase();
    const label = line.slice(idx + 1).trim();
    if (key && label) map[key] = label;
  }
  return map;
}

function loadEvent() {
  const eventPath = process.env.GITHUB_EVENT_PATH;
  if (!eventPath) {
    console.error('GITHUB_EVENT_PATH not set');
    process.exit(1);
  }
  const raw = fs.readFileSync(eventPath, { encoding: 'utf8' });
  return JSON.parse(raw);
}

function findMatchingLabels(event, mapping) {
  const title = (event.pull_request?.title || '').toLowerCase();
  const body = (event.pull_request?.body || '').toLowerCase();
  const matches = [];
  for (const [keyword, label] of Object.entries(mapping)) {
    if (title.includes(keyword) || body.includes(keyword)) {
      matches.push(label);
    }
  }
  return matches;
}

function main() {
  const token = getInput('token');
  const mappingStr = getInput('mapping');
  if (!token) {
    console.error('Input token is required');
    process.exit(1);
  }
  const mapping = parseMapping(mappingStr);
  const event = loadEvent();
  const labels = findMatchingLabels(event, mapping);

  if (labels.length === 0) {
    console.log('No matching labels found.');
    return;
  }

  // Output for downstream steps
  console.log(`::set-output name=added_labels::${labels.join(',')}`);
  // In a real action we would call the GitHub API here. For safety we just log.
  console.log(`Would add labels [${JSON.stringify(labels)}] to PR #${event.pull_request?.number}`);
}

if (require.main === module) {
  main();
}
