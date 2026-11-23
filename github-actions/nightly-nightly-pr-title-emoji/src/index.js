const core = require('@actions/core');
const github = require('@actions/github');

function getRandomEmoji() {
  const emojis = ['🚀','✨','🔥','💡','🎉','🛠️','🤖','🧩','🌟','🍀'];
  return emojis[Math.floor(Math.random() * emojis.length)];
}

async function run() {
  try {
    const token = core.getInput('github-token', { required: true });
    const octokit = github.getOctokit(token);
    const context = github.context;

    if (!context.payload.pull_request) {
      core.setFailed('No pull request found in the context.');
      return;
    }

    const pr = context.payload.pull_request;
    const owner = context.repo.owner;
    const repo = context.repo.repo;
    const prNumber = pr.number;
    const originalTitle = pr.title;

    const emoji = getRandomEmoji();
    const newTitle = `${originalTitle} ${emoji}`;

    await octokit.rest.pulls.update({
      owner,
      repo,
      pull_number: prNumber,
      title: newTitle
    });

    core.setOutput('emoji', emoji);
    console.log(`Appended emoji ${emoji} to PR #${prNumber}`);
  } catch (error) {
    core.setFailed(error.message);
  }
}

module.exports = { getRandomEmoji, run };

if (require.main === module) {
  run();
}
