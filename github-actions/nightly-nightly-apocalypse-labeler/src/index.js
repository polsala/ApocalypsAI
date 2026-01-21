const fs = require('fs');

function getInput(name) {
  const envName = `INPUT_${name.replace(/ /g, '_').toUpperCase()}`;
  return process.env[envName] || '';
}

function setOutput(name, value) {
  console.log(`::set-output name=${name}::${value}`);
}

function main() {
  const keywordsStr = getInput('keywords');
  const label = getInput('label') || 'apocalypse-ready';
  const keywords = keywordsStr
    .split(',')
    .map(k => k.trim().toLowerCase())
    .filter(Boolean);

  const eventPath = process.env['GITHUB_EVENT_PATH'];
  if (!eventPath) {
    console.error('GITHUB_EVENT_PATH not set');
    process.exit(1);
  }

  const raw = fs.readFileSync(eventPath, 'utf8');
  let event;
  try {
    event = JSON.parse(raw);
  } catch (e) {
    console.error('Failed to parse GITHUB_EVENT_PATH JSON');
    process.exit(1);
  }

  const title = (event.pull_request && event.pull_request.title || '').toLowerCase();
  const matched = keywords.some(k => title.includes(k));

  if (matched) {
    setOutput('apocalypse_label', label);
  } else {
    setOutput('apocalypse_label', '');
  }
}

main();
