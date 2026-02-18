const core = require('@actions/core');
const github = require('@actions/github');

function getRandomQuote() {
  const quotes = [
    "The sky is falling, but the code still compiles.",
    "When the servers go down, the coffee rises.",
    "In the end, all bugs are just features of the apocalypse.",
    "May your merge conflicts be as fleeting as the world’s last sunrise.",
    "Deploy early, survive later."
  ];
  return quotes[Math.floor(Math.random() * quotes.length)];
}

async function run() {
  try {
    const token = core.getInput('github-token', { required: true });
    const octokit = github.getOctokit(token);
    const { context } = github;
    const { owner, repo } = context.repo;
    const issue_number = context.payload.pull_request?.number;
    if (!issue_number) {
      core.setFailed('No pull request found in context.');
      return;
    }
    const commentBody = getRandomQuote();
    await octokit.rest.issues.createComment({
      owner,
      repo,
      issue_number,
      body: commentBody
    });
    core.setOutput('comment', commentBody);
  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
