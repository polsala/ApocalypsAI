const core = require('@actions/core');
const github = require('@actions/github');

async function run() { // Export this function for testing
  try {
    const token = core.getInput('repo-token', { required: true });
    const staleDays = parseInt(core.getInput('stale-days') || '30', 10);
    const overgrownCommentThreshold = parseInt(core.getInput('overgrown-comment-threshold') || '50', 10);

    const octokit = github.getOctokit(token);
    const { owner, repo } = github.context.repo;

    const now = new Date();
    let nurturedCount = 0;

    // Fetch all open issues and pull requests
    // Using pagination for robustness
    let issuesAndPrs = [];
    let page = 1;
    let hasMore = true;
    while (hasMore) {
      const { data } = await octokit.rest.issues.listForRepo({
        owner,
        repo,
        state: 'open',
        per_page: 100,
        page: page,
      });
      issuesAndPrs = issuesAndPrs.concat(data);
      if (data.length < 100) {
        hasMore = false;
      }
      page++;
    }

    for (const item of issuesAndPrs) {
      const updatedAt = new Date(item.updated_at);
      const daysSinceUpdate = Math.floor((now - updatedAt) / (1000 * 60 * 60 * 24));

      let commentBody = '';

      // Prioritize "parched" over "overgrown" if both conditions are met,
      // as "parched" implies a need for general attention, while "overgrown"
      // is more about structure.
      if (daysSinceUpdate >= staleDays) {
        // Item is "parched"
        const parchedComments = [
          "This discussion looks a bit parched! Anyone care to sprinkle some fresh ideas?",
          "A gentle breeze whispers... this issue seems to be waiting for a little nurturing. What's next?",
          "The digital garden needs tending! This one's looking a bit dry. Any thoughts to water it?",
          "Is this issue taking a long nap? Time for a wake-up call with some new insights!",
          "Our community garden thrives on interaction! Let's revive this conversation."
        ];
        commentBody = parchedComments[Math.floor(Math.random() * parchedComments.length)];
      } else if (item.comments >= overgrownCommentThreshold) {
        // Item is "overgrown"
        const overgrownComments = [
          "This discussion is blooming wildly! Perhaps a summary is in order to help us find the path?",
          "So many vibrant ideas here! Could someone help prune the discussion into actionable steps?",
          "The conversation has grown into a magnificent forest! Let's find the clearing and define our next move.",
          "A bountiful harvest of comments! Time to gather the fruits and distill the essence.",
          "This thread is a thriving ecosystem! Who can help us navigate its rich biodiversity?"
        ];
        commentBody = overgrownComments[Math.floor(Math.random() * overgrownComments.length)];
      }

      if (commentBody) {
        await octokit.rest.issues.createComment({
          owner,
          repo,
          issue_number: item.number,
          body: commentBody,
        });
        core.info(`Nurtured #${item.number}: ${commentBody}`);
        nurturedCount++;
      }
    }

    core.setOutput('nurtured-items-count', nurturedCount);
  } catch (error) {
    core.setFailed(error.message);
  }
}

module.exports = run; // Export the run function

if (require.main === module) {
  run(); // Call run() only when executed directly
}
