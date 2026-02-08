const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const token = core.getInput('github-token', { required: true });
    const mappingInput = core.getInput('label-mapping');
    let labelMapping = {};
    try {
      labelMapping = JSON.parse(mappingInput);
    } catch (e) {
      core.setFailed('label-mapping must be valid JSON');
      return;
    }

    const context = github.context;
    if (!context.payload.pull_request) {
      core.setFailed('This action only runs on pull_request events');
      return;
    }

    const prNumber = context.payload.pull_request.number;
    const prTitle = context.payload.pull_request.title;
    const repo = context.repo;

    const octokit = github.getOctokit(token);

    // Determine which labels to add based on keywords (case‑insensitive)
    const labelsToAdd = [];
    for (const [keyword, label] of Object.entries(labelMapping)) {
      const regex = new RegExp(`\\b${keyword}\\b`, 'i');
      if (regex.test(prTitle)) {
        labelsToAdd.push(label);
      }
    }

    if (labelsToAdd.length === 0) {
      core.info('No matching keywords found; no labels will be added.');
      return;
    }

    // Add labels (GitHub API ignores duplicates)
    await octokit.rest.issues.addLabels({
      owner: repo.owner,
      repo: repo.repo,
      issue_number: prNumber,
      labels: labelsToAdd
    });
    core.info(`Added labels: ${labelsToAdd.join(', ')}`);
  } catch (error) {
    core.setFailed(error.message);
  }
}

module.exports = { run };

if (require.main === module) {
  run();
}
