const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const token = core.getInput('github-token', { required: true });
    const customWhispersInput = core.getInput('whispers');

    const defaultWhispers = [
      "The void acknowledges your effort, and it is pleased.",
      "Even in the temporal flux, your code stands firm. Mostly.",
      "A glitch in the matrix? No, just pure brilliance!",
      "The cosmic dust settles, revealing your magnificent contribution.",
      "May your commits be many, and your merge conflicts few.",
      "The ancient ones whisper: 'Well done, mortal coder!'",
      "Your code shines brighter than a supernova in a forgotten galaxy.",
      "A ripple in the spacetime continuum, caused by your awesome commit!",
      "The algorithms sing praises to your elegant solution."
    ];

    const whispers = customWhispersInput
      ? customWhispersInput.split(',').map(w => w.trim()).filter(w => w.length > 0)
      : defaultWhispers;

    if (whispers.length === 0) {
      core.warning('No whispers provided, and default list is empty. Skipping comment.');
      core.setOutput('whisper-chosen', 'No whisper posted (empty list).');
      return;
    }

    const chosenWhisper = whispers[Math.floor(Math.random() * whispers.length)];
    core.setOutput('whisper-chosen', chosenWhisper);

    const octokit = github.getOctokit(token);
    const { owner, repo } = github.context.repo;

    let issueNumber;
    if (github.context.payload.pull_request) {
      issueNumber = github.context.payload.pull_request.number;
    } else if (github.context.payload.issue) {
      issueNumber = github.context.payload.issue.number;
    } else if (github.context.payload.comment && github.context.payload.issue) {
      // For issue_comment trigger, the issue object is directly in payload
      issueNumber = github.context.payload.issue.number;
    } else {
      core.warning('Could not determine a pull request or issue number from the context. Skipping comment.');
      return;
    }

    if (issueNumber) {
      await octokit.rest.issues.createComment({
        owner,
        repo,
        issue_number: issueNumber,
        body: `**A Whisper from the ApocalypsAI:**\n\n> _"${chosenWhisper}"_`
      });
      core.info(`Posted whisper to #${issueNumber}: "${chosenWhisper}"`);
    } else {
      core.warning('No valid issue or pull request number found to post a comment.');
    }

  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
