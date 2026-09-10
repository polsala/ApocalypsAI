const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const token = core.getInput('github-token', { required: true });
    const octokit = github.getOctokit(token);
    const context = github.context;

    // Load the event payload (pull_request_target event)
    const eventPath = process.env.GITHUB_EVENT_PATH;
    if (!eventPath) {
      core.setFailed('GITHUB_EVENT_PATH is not defined');
      return;
    }
    const event = require(eventPath);
    const pr = event.pull_request;
    if (!pr) {
      core.setFailed('No pull_request data found in event payload');
      return;
    }

    const additions = pr.additions || 0;
    const deletions = pr.deletions || 0;
    const totalChanges = additions + deletions;

    let category = '';
    let emoji = '';
    if (totalChanges < 10) {
      category = 'tiny';
      emoji = '🪶';
    } else if (totalChanges < 51) {
      category = 'small';
      emoji = '🐦';
    } else if (totalChanges < 201) {
      category = 'medium';
      emoji = '🦅';
    } else {
      category = 'large';
      emoji = '🦖';
    }

    const commentBody = `${emoji} This PR is **${category.toUpperCase()}** (${totalChanges} line changes).`;

    await octokit.rest.issues.createComment({
      owner: context.repo.owner,
      repo: context.repo.repo,
      issue_number: pr.number,
      body: commentBody,
    });

    core.setOutput('size-category', category);
  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
