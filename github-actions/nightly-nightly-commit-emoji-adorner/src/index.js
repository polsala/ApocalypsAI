const core = require('@actions/core');
const github = require('@actions/github');

// A small collection of fun emojis
const EMOJIS = ['🚀','✨','🔥','🌟','💥','🛸','🤖','🧩','🎉','🦄'];

async function run() {
  try {
    const token = core.getInput('token', { required: true });
    const octokit = github.getOctokit(token);
    const context = github.context;

    // Only act on pull request events
    if (!context.payload.pull_request) {
      core.info('No pull request context – skipping.');
      return;
    }

    const prNumber = context.payload.pull_request.number;
    const randomEmoji = EMOJIS[Math.floor(Math.random() * EMOJIS.length)];
    const commentBody = `${randomEmoji} Thanks for the PR!`;

    await octokit.rest.issues.createComment({
      owner: context.repo.owner,
      repo: context.repo.repo,
      issue_number: prNumber,
      body: commentBody,
    });

    core.setOutput('comment', commentBody);
    core.info(`Posted comment: ${commentBody}`);
  } catch (error) {
    core.setFailed(error.message);
  }
}

module.exports = { run };

// If the file is executed directly (e.g., via `node src/index.js`), run the action.
if (require.main === module) {
  run();
}
