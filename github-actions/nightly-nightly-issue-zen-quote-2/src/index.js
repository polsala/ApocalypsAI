const core = require('@actions/core');
const github = require('@actions/github');

const quotes = [
  "The journey of a thousand miles begins with a single step.",
  "When the wind blows, adjust your sails.",
  "Silence is a source of great strength.",
  "Even the darkest night will end and the sun will rise.",
  "Patience is the companion of wisdom."
];

async function run() {
  try {
    const token = core.getInput('github-token', { required: true });
    const octokit = github.getOctokit(token);
    const { context } = github;
    const issue = context.payload.issue;
    if (!issue) {
      core.setFailed('No issue payload found.');
      return;
    }
    // Allow deterministic selection in tests via env var
    const rand = process.env.FIXED_RANDOM ? parseFloat(process.env.FIXED_RANDOM) : Math.random();
    const quote = quotes[Math.floor(rand * quotes.length)];
    const commentBody = `> ${quote}\n\n*— ApocalypsAI*`;
    await octokit.rest.issues.createComment({
      ...context.repo,
      issue_number: issue.number,
      body: commentBody
    });
  } catch (error) {
    core.setFailed(error.message);
  }
}

if (require.main === module) {
  run();
}

module.exports = { run };
