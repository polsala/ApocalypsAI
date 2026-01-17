const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const token = core.getInput('github-token', { required: true });
    const octokit = github.getOctokit(token);

    const pullRequest = github.context.payload.pull_request;
    if (!pullRequest || !pullRequest.merged) {
      core.info('PR is not merged. Skipping celebration.');
      core.setOutput('is-first-contribution', 'false');
      return;
    }

    const owner = github.context.repo.owner;
    const repo = github.context.repo.repo;
    const author = pullRequest.user.login;
    const currentPrNumber = pullRequest.number;

    core.info(`Checking if ${author}'s PR #${currentPrNumber} is their first contribution to ${owner}/${repo}...`);

    // Search for other *merged* PRs by the same author in this repository
    // We need to exclude the current PR from the count.
    const query = `is:pr author:${author} is:merged repo:${owner}/${repo}`;
    const searchResult = await octokit.rest.search.issuesAndPullRequests({
      q: query,
      per_page: 100 // Fetch enough to be reasonably sure, or paginate if needed for very active repos
    });

    const mergedPrsByAuthor = searchResult.data.items.filter(item => item.pull_request && item.number !== currentPrNumber);

    if (mergedPrsByAuthor.length === 0) {
      core.info(`🎉 This is ${author}'s first merged contribution! Celebrating!`);
      const commentBody = `
✨ **A new blossom has bloomed!** ✨

Welcome, @${author}! We're absolutely thrilled to celebrate your very first merged contribution to our garden of code. Your effort on PR #${currentPrNumber} is a wonderful addition, and we're excited to see what else you'll cultivate with us!

Thank you for making our community a little brighter!
`;

      await octokit.rest.issues.createComment({
        owner,
        repo,
        issue_number: currentPrNumber,
        body: commentBody,
      });
      core.setOutput('is-first-contribution', 'true');
    } else {
      core.info(`${author} has ${mergedPrsByAuthor.length} other merged PRs. Not their first contribution.`);
      core.setOutput('is-first-contribution', 'false');
    }

  } catch (error) {
    core.setFailed(error.message);
  }
}

// This allows the script to be run directly or imported for testing
if (require.main === module) {
  run();
}
module.exports = { run };
