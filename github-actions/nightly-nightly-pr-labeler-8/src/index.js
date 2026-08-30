// Nightly PR Labeler Action
// Reads INPUT_LABELS env var (set by GitHub Actions) and outputs the processed list.

function getInput(name) {
  const envName = `INPUT_${name.toUpperCase()}`;
  return process.env[envName] || '';
}

function setOutput(name, value) {
  // GitHub Actions expects to write to a file defined in GITHUB_OUTPUT
  const outputFile = process.env['GITHUB_OUTPUT'];
  if (outputFile) {
    const fs = require('fs');
    fs.appendFileSync(outputFile, `${name}=${value}\n`);
  } else {
    // Fallback: print to console (for local testing)
    console.log(`::set-output name=${name}::${value}`);
  }
}

function run() {
  const raw = getInput('labels');
  const labels = raw.split(',').map(l => l.trim()).filter(l => l);
  const result = labels.join(', ');
  console.log(`Applying labels: ${result}`);
  setOutput('applied-labels', result);
}

run();
