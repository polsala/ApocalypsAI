const core = require('@actions/core');
const github = require('@actions/github');

const WISDOMS = [
  "Always know where your towel is. It's not just for hitchhikers anymore.",
  "Remember, duct tape fixes everything, even existential dread.",
  "A well-maintained zombie apocalypse plan is a happy apocalypse plan.",
  "Hydration is key, especially when fleeing mutant squirrels.",
  "Never trust a robot offering free hugs.",
  "The best defense against a rogue AI is a good offense... or a really bad Wi-Fi signal.",
  "Keep your emergency snacks close, and your emergency memes closer.",
  "When in doubt, blame the temporal anomaly.",
  "If you hear banjo music, run. If you don't hear banjo music, still run, just in case.",
  "Always carry a spare pair of socks. You never know when you'll need to cross a radioactive puddle.",
  "A good pair of boots will outlast any apocalypse.",
  "Learn to identify edible fungi. Or, more importantly, inedible fungi.",
  "Solar power is your friend. Unless it's a cloudy apocalypse.",
  "Barter skills are more valuable than gold. Unless you're bartering for gold.",
  "Don't forget to laugh. Even if it's a maniacal, end-of-the-world laugh."
];

async function run() {
  try {
    const githubToken = core.getInput('github-token', { required: true });
    const wisdomKeyword = core.getInput('wisdom-keyword'); // Defaults to 'survival tip' from action.yml

    const octokit = github.getOctokit(githubToken);
    const { owner, repo } = github.context.repo;
    const pullRequest = github.context.payload.pull_request;

    if (!pullRequest) {
      core.warning('This action only runs on pull_request events. Skipping.');
      return;
    }

    const prNumber = pullRequest.number;
    const prBody = pullRequest.body || '';

    // Check if the PR description already contains the wisdom keyword (case-insensitive)
    if (prBody.toLowerCase().includes(wisdomKeyword.toLowerCase())) {
      core.info(`PR #${prNumber} already contains the keyword "${wisdomKeyword}". No advice needed.`);
      return;
    }

    // Pick a random wisdom
    const randomWisdom = WISDOMS[Math.floor(Math.random() * WISDOMS.length)];
    const commentBody = `### 🔮 Apocalyptic Wisdom Advisory 🔮\n\nIt seems this Pull Request could benefit from a touch of foresight! Here's a survival tip for the ages:\n\n> "${randomWisdom}"\n\nConsider adding your own **${wisdomKeyword}** to the PR description next time!`;

    // Post the comment to the PR
    const { data: comment } = await octokit.rest.issues.createComment({
      owner,
      repo,
      issue_number: prNumber,
      body: commentBody
    });

    core.setOutput('comment-id', comment.id);
    core.info(`Posted apocalyptic wisdom to PR #${prNumber}. Comment ID: ${comment.id}`);

  } catch (error) {
    core.setFailed(error.message);
  }
}

// Export run for testing, and call it if not in a test environment
if (require.main === module) {
  run();
} else {
  module.exports = run;
}
