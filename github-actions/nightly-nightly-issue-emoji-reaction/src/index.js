const core = require('@actions/core');
const github = require('@actions/github');

function getRandomEmoji(emojis) {
  const list = emojis.split(',').map(e => e.trim()).filter(e => e);
  const idx = Math.floor(Math.random() * list.length);
  return list[idx];
}

async function run() {
  try {
    const token = core.getInput('token', { required: true });
    const emojis = core.getInput('emojis');
    const octokit = github.getOctokit(token);
    const context = github.context;

    if (!context.payload.issue) {
      core.setFailed('No issue payload found.');
      return;
    }

    const issueNumber = context.payload.issue.number;
    const owner = context.repo.owner;
    const repo = context.repo.repo;

    const emoji = getRandomEmoji(emojis);
    await octokit.rest.reactions.createForIssue({
      owner,
      repo,
      issue_number: issueNumber,
      content: emoji,
    });

    core.setOutput('emoji', emoji);
  } catch (error) {
    core.setFailed(error.message);
  }
}

if (require.main === module) {
  run();
} else {
  module.exports = { run, getRandomEmoji };
}
