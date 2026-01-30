const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const token = core.getInput('github-token', { required: true });
    const octokit = github.getOctokit(token);
    const eventPath = process.env.GITHUB_EVENT_PATH;
    if (!eventPath) {
      core.setFailed('GITHUB_EVENT_PATH not set');
      return;
    }
    const event = require(eventPath);
    const commitMessage = (event.head_commit && event.head_commit.message) || '';
    const sha = event.after || (event.head_commit && event.head_commit.id);
    if (!sha) {
      core.setFailed('Commit SHA not found in event payload');
      return;
    }
    const emoji = selectEmoji(commitMessage);
    await octokit.reactions.createForCommit({
      ...github.context.repo,
      commit_sha: sha,
      content: emoji
    });
    core.setOutput('emoji', emoji);
  } catch (error) {
    core.setFailed(error.message);
  }
}

function selectEmoji(message) {
  const lower = message.toLowerCase();
  if (lower.includes('fix')) return '+1';
  if (lower.includes('feat')) return 'rocket';
  if (lower.includes('docs')) return 'book';
  return 'eyes';
}

module.exports = { run, selectEmoji };

if (require.main === module) {
  run();
}
