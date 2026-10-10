const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const token = core.getInput('github-token', { required: true });
    const labelToTrigger = core.getInput('label-to-trigger', { required: true });
    const messagesInput = core.getInput('messages', { required: true });
    const messages = JSON.parse(messagesInput);

    const { context } = github;
    const octokit = github.getOctokit(token);

    let issueNumber;
    let labels = [];

    if (context.eventName === 'pull_request' && context.payload.pull_request) {
      issueNumber = context.payload.pull_request.number;
      labels = context.payload.pull_request.labels.map(label => label.name);
      core.info(`Processing Pull Request #${issueNumber}`);
    } else if (context.eventName === 'issues' && context.payload.issue) {
      issueNumber = context.payload.issue.number;
      labels = context.payload.issue.labels.map(label => label.name);
      core.info(`Processing Issue #${issueNumber}`);
    } else {
      core.info('Not a pull_request or issues event, or payload is missing. Skipping.');
      return;
    }

    if (!issueNumber) {
      core.info('Could not determine issue or pull request number. Skipping.');
      return;
    }

    if (labels.includes(labelToTrigger)) {
      const randomIndex = Math.floor(Math.random() * messages.length);
      const message = messages[randomIndex];

      core.info(`Label '${labelToTrigger}' found. Posting whimsical encouragement.`);
      const { data: comment } = await octokit.rest.issues.createComment({
        owner: context.repo.owner,
        repo: context.repo.repo,
        issue_number: issueNumber,
        body: message
      });
      core.setOutput('comment-id', comment.id);
      core.info(`Comment posted: ${comment.html_url}`);
    } else {
      core.info(`Label '${labelToTrigger}' not found on #${issueNumber}. Skipping.`);
    }
  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
