const core = require('@actions/core');
const github = require('@actions/github');
const { comments } = require('./comments');

async function run() {
  try {
    const token = core.getInput('github-token', { required: true });
    const daysBack = parseInt(core.getInput('days-back') || '7', 10);

    const octokit = github.getOctokit(token);
    const { owner, repo } = github.context.repo;

    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - daysBack);

    core.info(`Looking for merged PRs in ${owner}/${repo} merged after ${cutoffDate.toISOString()}...`);

    // Fetch merged PRs
    const { data: pullRequests } = await octokit.rest.pulls.list({
      owner,
      repo,
      state: 'closed',
      sort: 'updated',
      direction: 'desc',
      per_page: 100 // Fetch up to 100 recent PRs
    });

    const eligiblePRs = pullRequests.filter(pr => {
      if (!pr.merged_at) return false;
      const mergedAt = new Date(pr.merged_at);
      return mergedAt >= cutoffDate;
    });

    if (eligiblePRs.length === 0) {
      core.info('No eligible merged Pull Requests found in the specified period.');
      return;
    }

    // Randomly select one PR
    const randomIndex = Math.floor(Math.random() * eligiblePRs.length);
    const selectedPR = eligiblePRs[randomIndex];

    const comment = comments[Math.floor(Math.random() * comments.length)];

    core.info(`Selected PR #${selectedPR.number}: ${selectedPR.title}`);
    core.info(`Posting commendation: \"${comment}\"`)

    // Post the comment
    await octokit.rest.issues.createComment({
      owner,
      repo,
      issue_number: selectedPR.number,
      body: comment
    });

    core.info(`Successfully commended PR #${selectedPR.number}.`);

  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
