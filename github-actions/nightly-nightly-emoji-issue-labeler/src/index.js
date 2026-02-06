const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const emoji = core.getInput('emoji', { required: true });
    const baseLabel = core.getInput('label', { required: true });
    const fullLabel = `${baseLabel} ${emoji}`;

    const token = process.env.GITHUB_TOKEN;
    if (!token) {
      core.setFailed('GITHUB_TOKEN is required');
      return;
    }

    const octokit = github.getOctokit(token);
    const { context } = github;
    const issueNumber = context.issue.number;
    const owner = context.repo.owner;
    const repo = context.repo.repo;

    // Ensure label exists
    await octokit.rest.issues.createLabel({
      owner,
      repo,
      name: fullLabel,
      color: 'FF5733',
      description: `Label with emoji ${emoji}`
    }).catch(err => {
      // If label already exists, ignore error
      if (err.status !== 422) {
        throw err;
      }
    });

    // Add label to issue/PR
    await octokit.rest.issues.addLabels({
      owner,
      repo,
      issue_number: issueNumber,
      labels: [fullLabel]
    });
  } catch (error) {
    core.setFailed(error.message);
  }
}

if (require.main === module) {
  run();
} else {
  module.exports = { run };
}
