const core = require('@actions/core');
const github = require('@actions/github');

/**
 * Compute which labels should be added based on the PR title.
 * @param {string} title - Pull request title.
 * @param {Object} mapping - Keyword → label map.
 * @returns {string[]} Array of labels to add.
 */
function computeLabels(title, mapping) {
  const lower = title.toLowerCase();
  const labels = [];
  for (const [keyword, label] of Object.entries(mapping)) {
    if (lower.includes(keyword.toLowerCase())) {
      labels.push(label);
    }
  }
  return labels;
}

async function run() {
  try {
    const token = core.getInput('token', { required: true });
    const mappingInput = core.getInput('mapping');
    const mapping = JSON.parse(mappingInput);
    const context = github.context;

    if (!context.payload.pull_request) {
      core.setFailed('No pull request payload found.');
      return;
    }

    const pr = context.payload.pull_request;
    const labelsToAdd = computeLabels(pr.title, mapping);

    if (labelsToAdd.length === 0) {
      core.info('No matching labels found for this PR title.');
      return;
    }

    const octokit = github.getOctokit(token);
    await octokit.rest.issues.addLabels({
      owner: context.repo.owner,
      repo: context.repo.repo,
      issue_number: pr.number,
      labels: labelsToAdd,
    });
    core.info(`Added labels: ${labelsToAdd.join(', ')}`);
  } catch (error) {
    core.setFailed(error.message);
  }
}

// Export for unit testing
module.exports = { computeLabels, run };

if (require.main === module) {
  run();
}
