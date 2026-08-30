const core = require('@actions/core');
const github = require('@actions/github');

function getRandomTip() {
  const tips = [
    "Always keep a spare can of beans in your bunker.",
    "Never trust a squirrel with your map.",
    "Water is life—filter it before you drink.",
    "A flashlight is only useful if you have batteries.",
    "Remember: the best camouflage is invisibility."
  ];
  return tips[Math.floor(Math.random() * tips.length)];
}

async function run() {
  try {
    const token = core.getInput('github-token', { required: true });
    const octokit = github.getOctokit(token);
    const { context } = github;
    const issueNumber = context.payload.pull_request?.number;
    if (!issueNumber) {
      core.setFailed('No pull request found in context.');
      return;
    }
    const tip = getRandomTip();
    await octokit.rest.issues.createComment({
      ...context.repo,
      issue_number: issueNumber,
      body: `🛡️ **Apocalypse Survival Tip:** ${tip}`
    });
    core.setOutput('tip', tip);
  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
