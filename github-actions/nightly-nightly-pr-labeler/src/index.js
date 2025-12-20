const core = require('@actions/core');
const github = require('@actions/github');

function getLabelForTitle(title) {
  const lower = title.toLowerCase();
  if (lower.includes('urgent')) return 'high priority';
  if (lower.includes('wip')) return 'work in progress';
  if (lower.includes('fix')) return 'bug fix';
  if (lower.includes('feature')) return 'new feature';
  if (lower.includes('zombie')) return 'zombie PR';
  return null;
}

async function run() {
  try {
    const token = core.getInput('github-token', { required: true });
    const octokit = github.getOctokit(token);
    const { context } = github;
    const pr = context.payload.pull_request;
    if (!pr) {
      core.setFailed('No pull request found in context');
      return;
    }
    const label = getLabelForTitle(pr.title);
    if (!label) {
      core.info('No matching keyword, skipping labeling');
      return;
    }
    await octokit.rest.issues.addLabels({
      owner: context.repo.owner,
      repo: context.repo.repo,
      issue_number: pr.number,
      labels: [label],
    });
    core.info(`Added label "${label}" to PR #${pr.number}`);
  } catch (error) {
    core.setFailed(error.message);
  }
}

if (require.main === module) {
  run();
}
module.exports = run;
