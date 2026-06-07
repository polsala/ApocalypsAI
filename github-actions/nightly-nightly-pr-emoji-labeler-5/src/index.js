// Minimal GitHub Action implementation without external packages
const core = {
  getInput: (name) => {
    const envName = `INPUT_${name.toUpperCase()}`;
    return process.env[envName] || '';
  },
  setOutput: (name, value) => {
    console.log(`::set-output name=${name}::${value}`);
  }
};

function determineEmoji(title) {
  const lower = title.toLowerCase();
  const positive = ['add', 'fix', 'improve', 'update', 'enhance'];
  const negative = ['remove', 'deprecate', 'break', 'fail', 'bug'];
  if (positive.some(word => lower.includes(word))) return '👍';
  if (negative.some(word => lower.includes(word))) return '👎';
  return '🤝';
}

function run() {
  const title = core.getInput('title');
  if (!title) {
    console.error('Error: title input is required');
    process.exit(1);
  }
  const emoji = determineEmoji(title);
  core.setOutput('emoji', emoji);
}

run();
