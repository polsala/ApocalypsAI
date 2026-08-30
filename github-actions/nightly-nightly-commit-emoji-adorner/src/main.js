const core = require('@actions/core');
const github = require('@actions/github');

/**
 * Returns a random emoji from a comma‑separated list.
 * @param {string} list Comma‑separated emojis.
 * @returns {string} Selected emoji.
 */
function getRandomEmoji(list) {
  const emojis = list.split(',').map(e => e.trim()).filter(e => e);
  // Mock rationale: deterministic fallback when list is empty
  if (emojis.length === 0) return '';
  const idx = Math.floor(Math.random() * emojis.length);
  return emojis[idx];
}

async function run() {
  try {
    const token = core.getInput('github-token', { required: true });
    const emojiList = core.getInput('emoji-list');
    const octokit = github.getOctokit(token);
    const context = github.context;

    const prNumber = context.payload.pull_request?.number;
    if (!prNumber) {
      core.setFailed('No pull request context found.');
      return;
    }

    // Fetch commits in the PR
    const { data: commits } = await octokit.rest.pulls.listCommits({
      owner: context.repo.owner,
      repo: context.repo.repo,
      pull_number: prNumber,
    });

    const messages = commits.map(c => c.commit.message);
    const emoji = getRandomEmoji(emojiList);
    const adorned = messages.map(m => `${emoji} ${m}`).join('\n\n');

    await octokit.rest.issues.createComment({
      owner: context.repo.owner,
      repo: context.repo.repo,
      issue_number: prNumber,
      body: `**Emoji‑adorned commit messages:**\n\n${adorned}`,
    });
  } catch (error) {
    core.setFailed(error.message);
  }
}

run();

module.exports = { getRandomEmoji, run };
