const core = require('@actions/core');
const github = require('@actions/github');

function getRandomQuote() {
  const quotes = [
    "The journey of a thousand miles begins with a single step.",
    "When the mind is still, the universe surrenders.",
    "Silence is a source of great strength.",
    "The obstacle is the path.",
    "Let go or be dragged."
  ];
  return quotes[Math.floor(Math.random() * quotes.length)];
}

async function run() {
  try {
    const token = core.getInput('github-token', { required: true });
    const octokit = github.getOctokit(token);
    const { context } = github;
    const issueNumber = context.payload.issue?.number;
    if (!issueNumber) {
      core.setFailed('No issue number found in context.');
      return;
    }
    const quote = getRandomQuote();
    await octokit.rest.issues.createComment({
      ...context.repo,
      issue_number: issueNumber,
      body: quote
    });
    core.setOutput('quote', quote);
  } catch (error) {
    core.setFailed(error.message);
  }
}

run();

module.exports = { getRandomQuote, run };
