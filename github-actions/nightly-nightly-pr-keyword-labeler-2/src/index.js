const fs = require('fs');

function getInput(name) {
  const envName = `INPUT_${name.toUpperCase()}`;
  return process.env[envName] || '';
}

function setOutput(name, value) {
  // GitHub Actions command to set output
  console.log(`::set-output name=${name}::${value}`);
}

function main() {
  const keyword = getInput('keyword').toLowerCase();
  const label = getInput('label');
  const eventPath = process.env['GITHUB_EVENT_PATH'];
  if (!eventPath) {
    setOutput('label', '');
    return;
  }
  const eventData = JSON.parse(fs.readFileSync(eventPath, 'utf8'));
  const title = (eventData.pull_request && eventData.pull_request.title) || '';
  if (title.toLowerCase().includes(keyword)) {
    setOutput('label', label);
  } else {
    setOutput('label', '');
  }
}

main();
