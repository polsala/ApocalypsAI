const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const token = core.getInput('repo-token', { required: true });
    const staleLabel = core.getInput('stale-issue-label');
    const daysBeforeStale = parseInt(core.getInput('days-before-stale'), 10);
    const daysBeforeClose = parseInt(core.getInput('days-before-close'), 10);
    const staleMessage = core.getInput('stale-issue-message');
    const closeMessage = core.getInput('close-issue-message');
    const exemptLabels = core.getInput('exempt-labels').split(',').map(l => l.trim()).filter(l => l.length > 0);
    const onlyLabels = core.getInput('only-labels').split(',').map(l => l.trim()).filter(l => l.length > 0);

    const octokit = github.getOctokit(token);
    const { owner, repo } = github.context.repo;

    const issues = await octokit.rest.issues.listForRepo({
      owner,
      repo,
      state: 'open',
      per_page: 100, // Max 100 issues per page
    });

    const now = new Date();

    for (const issue of issues.data) {
      // Skip pull requests
      if (issue.pull_request) {
        core.info(`Issue #${issue.number} is a pull request. Skipping.`);
        continue;
      }

      const issueLabels = issue.labels.map(label => label.name);

      // Check for exempt labels
      if (exemptLabels.some(label => issueLabels.includes(label))) {
        core.info(`Issue #${issue.number} has an exempt label. Skipping.`);
        continue;
      }

      // Check for only-labels if specified
      if (onlyLabels.length > 0 && !onlyLabels.some(label => issueLabels.includes(label))) {
        core.info(`Issue #${issue.number} does not have any of the specified 'only-labels'. Skipping.`);
        continue;
      }

      const updatedAt = new Date(issue.updated_at);
      const daysInactive = Math.floor((now - updatedAt) / (1000 * 60 * 60 * 24));
      const isStale = issueLabels.includes(staleLabel);

      if (isStale) {
        // Issue is already stale, check if it should be closed
        if (daysInactive >= (daysBeforeStale + daysBeforeClose)) {
          core.info(`Closing issue #${issue.number} due to extended inactivity.`);
          await octokit.rest.issues.createComment({
            owner,
            repo,
            issue_number: issue.number,
            body: closeMessage,
          });
          await octokit.rest.issues.update({
            owner,
            repo,
            issue_number: issue.number,
            state: 'closed',
          });
        } else {
          core.info(`Issue #${issue.number} is stale but not yet ready to be closed.`);
        }
      } else {
        // Issue is not stale, check if it should be marked stale
        if (daysInactive >= daysBeforeStale) {
          core.info(`Marking issue #${issue.number} as stale.`);
          await octokit.rest.issues.addLabels({
            owner,
            repo,
            issue_number: issue.number,
            labels: [staleLabel],
          });
          await octokit.rest.issues.createComment({
            owner,
            repo,
            issue_number: issue.number,
            body: staleMessage,
          });
        } else {
          core.info(`Issue #${issue.number} is active enough. Skipping.`);
        }
      }
    }
  } catch (error) {
    core.setFailed(error.message);
  }
}

run();

// Export for testing purposes
module.exports = { run };
