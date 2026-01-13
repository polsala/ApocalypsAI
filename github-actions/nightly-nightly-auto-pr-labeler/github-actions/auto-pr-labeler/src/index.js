const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const token = core.getInput('repo-token', { required: true });
    const octokit = github.getOctokit(token);
    const { context } = github;
    const pr = context.payload.pull_request;
    if (!pr) {
      core.setFailed('No pull request found.');
      return;
    }
    const title = pr.title.toLowerCase();
    const labels = [];

    const mapping = {
      'fix': 'ð§ zombie-fix',
      'feature': 'âï¸ sunrise-feature',
      'doc': 'ð documentation',
      'refactor': 'ð§ refactor',
      'test': 'â test-addition'
    };

    for (const [keyword, label] of Object.entries(mapping)) {
      if (title.includes(keyword)) {
        labels.push(label);
      }
    }

    if (labels.length > 0) {
      await octokit.rest.issues.addLabels({
        owner: context.repo.owner,
        repo: context.repo.repo,
        issue_number: pr.number,
        labels
      });
      core.info(`Added labels: ${labels.join(', ')}`);
    } else {
      core.info('No matching keywords, no labels added.');
    }
  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
