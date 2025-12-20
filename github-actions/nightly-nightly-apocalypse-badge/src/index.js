const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const token = core.getInput('github-token', { required: true });
    const octokit = github.getOctokit(token);
    const context = github.context;

    // Ensure we are dealing with a pull request event
    if (!context.payload.pull_request) {
      core.info('No pull request payload – exiting.');
      return;
    }

    const pr = context.payload.pull_request;
    const labels = pr.labels.map(l => l.name);
    const hasApocalypse = labels.includes('apocalypse');

    if (!hasApocalypse) {
      core.info('Apocalypse label not present – nothing to do.');
      return;
    }

    const badgeUrl = 'https://img.shields.io/badge/Apocalypse-⚔️-red';
    const commentBody = `![Apocalypse](${badgeUrl})`;

    // Post the comment
    await octokit.rest.issues.createComment({
      owner: context.repo.owner,
      repo: context.repo.repo,
      issue_number: pr.number,
      body: commentBody
    });

    core.info('Apocalypse badge comment posted.');
  } catch (error) {
    core.setFailed(`Action failed with error: ${error}`);
  }
}

run();
