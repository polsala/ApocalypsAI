const core = require('@actions/core');

function determineLabel(title, mapping) {
  const priorities = ['critical', 'high', 'medium', 'low'];
  const lowerTitle = title.toLowerCase();
  for (const p of priorities) {
    const keywords = mapping[p] || [];
    for (const kw of keywords) {
      if (lowerTitle.includes(kw.toLowerCase())) {
        return p;
      }
    }
  }
  return 'untriaged';
}

function run() {
  try {
    const title = core.getInput('title', { required: true });
    const mappingInput = core.getInput('priority_keywords');
    let mapping = {};
    try {
      mapping = JSON.parse(mappingInput);
    } catch (e) {
      core.setFailed('priority_keywords must be valid JSON');
      return;
    }
    const label = determineLabel(title, mapping);
    core.setOutput('label', label);
  } catch (error) {
    core.setFailed(error.message);
  }
}

if (require.main === module) {
  run();
}

module.exports = { run, determineLabel };
