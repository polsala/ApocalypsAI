const core = require('@actions/core');
const github = require('@actions/github');

function getLabelsFromTitle(title) {
  const lower = title.toLowerCase();
  const labels = new Set();
  if (lower.includes('fix') || lower.includes('bug')) labels.add('bug');
  if (lower.includes('feat') || lower.includes('feature')) labels.add('enhancement');
  if (lower.includes('doc') || lower.includes('docs')) labels.add('documentation');
  return Array.from(labels);
}

async function run() {
  try {
    const token = core.getInput('token', { required: true });
    const octokit = github.getOctokit(token);
    const context = github.context;
    if (!context.payload.pull_request) {
      core.setFailed('No pull request payload');
      return;
    }
    const title = context.payload.pull_request.title;
    const owner = context.repo.owner;
    const repo = context.repo.repo;
    const number = context.payload.pull_request.number;
    const labels = getLabelsFromTitle(title);
    if (labels.length === 0) {
      core.info('No matching labels found');
      return;
    }
    await octokit.rest.issues.addLabels({
      owner,
      repo,
      issue_number: number,
      labels,
    });
    core.info(`Added labels: ${labels.join(', ')}`);
  } catch (error) {
    core.setFailed(error.message);
  }
}

module.exports = { getLabelsFromTitle, run };
if (require.main === module) {
  run();
}
