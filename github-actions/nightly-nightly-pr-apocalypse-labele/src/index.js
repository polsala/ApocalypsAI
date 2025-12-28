const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const token = core.getInput('github-token', { required: true });
    const rawKeywords = core.getInput('keywords');
    const keywords = rawKeywords.split(',').map(k => k.trim().toLowerCase()).filter(k => k.length > 0);

    const context = github.context;
    if (context.eventName !== 'pull_request') {
      core.info('Event is not a pull_request, skipping.');
      return;
    }

    const pr = context.payload.pull_request;
    const title = pr.title.toLowerCase();
    const matches = keywords.some(kw => title.includes(kw));

    if (!matches) {
      core.info('No apocalypse keywords found in PR title.');
      return;
    }

    const octokit = github.getOctokit(token);
    const owner = context.repo.owner;
    const repo = context.repo.repo;
    const issue_number = pr.number;

    await octokit.rest.issues.addLabels({
      owner,
      repo,
      issue_number,
      labels: ['apocalypse']
    });
    core.info(`Added 'apocalypse' label to PR #${issue_number}`);
  } catch (error) {
    core.setFailed(`Action failed with error: ${error}`);
  }
}

run();
