const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const token = core.getInput('github_token', { required: true });
    const emojiList = core.getInput('emoji_labels') || '';
    const emojis = emojiList.split(',').map(e => e.trim()).filter(Boolean);
    const octokit = github.getOctokit(token);
    const { context } = github;

    if (!context.payload.pull_request) {
      core.setFailed('No pull request found in context');
      return;
    }

    const title = context.payload.pull_request.title;
    const labels = [];

    // Map common prefixes to labels
    const prefixMap = {
      'feat': 'feature',
      'fix': 'bug',
      'docs': 'documentation',
      'chore': 'chore',
      'refactor': 'refactor',
      'test': 'tests',
    };
    const lower = title.toLowerCase();
    for (const [prefix, label] of Object.entries(prefixMap)) {
      if (lower.startsWith(`${prefix}:`) || lower.startsWith(`${prefix}(`)) {
        labels.push(label);
        break;
      }
    }

    // Add a random emoji label if emojis are provided
    if (emojis.length > 0) {
      const random = emojis[Math.floor(Math.random() * emojis.length)];
      labels.push(random);
    }

    if (labels.length > 0) {
      await octokit.rest.issues.addLabels({
        owner: context.repo.owner,
        repo: context.repo.repo,
        issue_number: context.payload.pull_request.number,
        labels,
      });
      core.info(`Added labels: ${labels.join(', ')}`);
    } else {
      core.info('No labels to add');
    }
  } catch (error) {
    core.setFailed(error.message);
  }
}

run();

module.exports = { run };
