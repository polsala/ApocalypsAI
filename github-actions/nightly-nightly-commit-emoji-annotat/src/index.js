const core = require('@actions/core');
const github = require('@actions/github');

function getSentiment(message) {
  const positive = ['feat', 'add', 'improve', 'fix', 'refactor', 'enhance'];
  const negative = ['bug', 'remove', 'fail', 'break', 'error', 'deprecate'];
  const lower = message.toLowerCase();
  if (positive.some(word => lower.includes(word))) return 'positive';
  if (negative.some(word => lower.includes(word))) return 'negative';
  return 'neutral';
}

function emojiForSentiment(sentiment) {
  if (sentiment === 'positive') return '+1';
  if (sentiment === 'negative') return '-1';
  return 'confused';
}

async function run() {
  try {
    const token = core.getInput('github-token', { required: true });
    const pullNumber = parseInt(core.getInput('pull-number', { required: true }), 10);
    const octokit = github.getOctokit(token);
    const { owner, repo } = github.context.repo;

    const { data: commits } = await octokit.rest.pulls.listCommits({
      owner,
      repo,
      pull_number: pullNumber,
    });

    for (const commit of commits) {
      const sentiment = getSentiment(commit.commit.message);
      const reaction = emojiForSentiment(sentiment);
      await octokit.rest.reactions.createForCommit({
        owner,
        repo,
        commit_sha: commit.sha,
        content: reaction,
      });
      core.info(`Added ${reaction} reaction to commit ${commit.sha}`);
    }
  } catch (error) {
    core.setFailed(error.message);
  }
}

if (require.main === module) {
  run();
}

module.exports = { getSentiment, emojiForSentiment, run };
