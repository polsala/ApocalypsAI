const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const token = core.getInput('github_token', { required: true });
    const octokit = github.getOctokit(token);
    const context = github.context;

    if (!context.payload.pull_request) {
      core.setFailed('No pull request payload found.');
      return;
    }

    const prNumber = context.payload.pull_request.number;
    const title = context.payload.pull_request.title.toLowerCase();

    const labels = [];

    if (/(bug|fix|error)/.test(title)) {
      labels.push('bug');
    }
    if (/(feat|feature|add)/.test(title)) {
      labels.push('feature');
    }
    if (/(doc|readme|docs)/.test(title)) {
      labels.push('docs');
    }
    if (labels.length === 0) {
      labels.push('chore');
    }

    await octokit.rest.issues.addLabels({
      owner: context.repo.owner,
      repo: context.repo.repo,
      issue_number: prNumber,
      labels: labels
    });

    core.setOutput('added_labels', labels.join(','));
  } catch (error) {
    core.setFailed(error.message);
  }
}

module.exports = { run };

if (require.main === module) {
  run();
}
