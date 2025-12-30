const core = require('@actions/core');
const github = require('@actions/github');

function extractEmojis(text) {
  // Simple regex for emoji characters (Unicode range)
  const emojiRegex = /[\u{1F300}-\u{1F6FF}\u{1F900}-\u{1F9FF}\u{2600}-\u{26FF}]/gu;
  return text.match(emojiRegex) || [];
}

async function run() {
  try {
    const token = core.getInput('github-token', { required: true });
    const octokit = github.getOctokit(token);
    const { context } = github;
    const pr = context.payload.pull_request;
    if (!pr) {
      core.setFailed('No pull request found in context.');
      return;
    }
    const title = pr.title;
    const emojis = extractEmojis(title);
    const emojiLabelMap = {
      '🚀': 'enhancement',
      '🐛': 'bug',
      '📚': 'documentation'
    };
    const labelsToAdd = [...new Set(emojis.map(e => emojiLabelMap[e]).filter(Boolean))];
    if (labelsToAdd.length === 0) {
      core.info('No matching emojis found; nothing to label.');
      return;
    }
    await octokit.rest.issues.addLabels({
      owner: context.repo.owner,
      repo: context.repo.repo,
      issue_number: pr.number,
      labels: labelsToAdd
    });
    core.info(`Added labels: ${labelsToAdd.join(', ')}`);
  } catch (error) {
    core.setFailed(error.message);
  }
}

run();

module.exports = { run, extractEmojis };
