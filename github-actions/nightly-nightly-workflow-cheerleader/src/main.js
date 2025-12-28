const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const token = core.getInput('token', { required: true });
    const customMessage = core.getInput('message');
    const issueNumberInput = core.getInput('issue-number');

    const octokit = github.getOctokit(token);
    const { owner, repo } = github.context.repo;

    let issue_number = parseInt(issueNumberInput);

    if (isNaN(issue_number) || issue_number <= 0) {
      // Try to get issue/PR number from context if not provided
      if (github.context.payload.pull_request) {
        issue_number = github.context.payload.pull_request.number;
      } else if (github.context.payload.issue) {
        issue_number = github.context.payload.issue.number;
      } else if (github.context.payload.workflow_run) {
        // For workflow_run events, try to find associated PRs/issues
        // This is more complex and might require additional API calls.
        // For simplicity, we'll stick to direct PR/Issue context for now.
        core.warning('No direct pull request or issue found in workflow_run context. Skipping comment.');
        return;
      }
    }

    if (!issue_number) {
      core.warning('Could not determine an issue or pull request number to comment on. Skipping comment.');
      return;
    }

    const messages = [
      "Huzzah! This workflow has triumphed over the digital dragons!",
      "Behold, a symphony of success! Your code sings!",
      "The gears of progress turn smoothly, thanks to this magnificent run!",
      "Victory is ours! The bits and bytes align perfectly!",
      "Workflow complete! Now go forth and conquer more code!",
      "The cosmic alignment of your code is truly spectacular! Well done!",
      "Success! The digital spirits rejoice in your accomplishment!",
      "A masterpiece of automation! This workflow is a shining beacon!",
      "Your efforts have borne fruit! A glorious success!",
      "The prophecy has been fulfilled: this workflow is a triumph!"
    ];

    const messageToPost = customMessage || messages[Math.floor(Math.random() * messages.length)];

    core.info(`Attempting to post comment on ${owner}/${repo}#${issue_number}`);
    core.info(`Message: "${messageToPost}"`);

    const { data: comment } = await octokit.rest.issues.createComment({
      owner,
      repo,
      issue_number,
      body: `✨ **Workflow Cheerleader says:** ✨\n\n${messageToPost}`
    });

    core.setOutput('comment-url', comment.html_url);
    core.info(`Comment posted: ${comment.html_url}`);

  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
