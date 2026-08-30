const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const githubToken = core.getInput('github-token', { required: true });
    const messageType = core.getInput('message-type'); // Currently only 'whimsical'

    const octokit = github.getOctokit(githubToken);

    const messages = [
      "Behold, a new beacon of hope in the digital wasteland! May your code compile swiftly and your bugs be few. ✨",
      "Another day, another step towards rebuilding! Your contribution shines brighter than a supernova in a void. Keep up the magnificent work! 🚀",
      "Even in the echoes of the old world, your creativity sparks new life. This contribution is a masterpiece in the making! 🎨",
      "The algorithms whisper tales of your brilliance! May your commits be atomic and your merges conflict-free. 🌟",
      "Fear not the digital dust storms! Your efforts are forging a path to a brighter tomorrow. Onward, brave coder! 🛡️",
      "In the grand symphony of the apocalypse, your code is a harmonious note. Keep composing wonders! 🎶",
      "The digital spirits cheer for your progress! May your debugging sessions be short and your deployments smooth. 👻",
      "A glimmer of genius in the gloom! Your work is a testament to resilience and innovation. Bravo! 💡",
      "From the ashes of the old world, your ideas bloom like radiant data flowers. Keep cultivating brilliance! 🌸",
      "The cosmic dust settles, revealing the path you forge with each line of code. You're a star-navigator of the digital realm! 🌌"
    ];

    const randomMessage = messages[Math.floor(Math.random() * messages.length)];

    let issueNumber;
    let repoOwner;
    let repoName;

    if (github.context.payload.pull_request) {
      issueNumber = github.context.payload.pull_request.number;
      repoOwner = github.context.repo.owner;
      repoName = github.context.repo.repo;
      core.info(`Detected Pull Request #${issueNumber}. Posting morale boost.`);
    } else if (github.context.payload.issue) {
      issueNumber = github.context.payload.issue.number;
      repoOwner = github.context.repo.owner;
      repoName = github.context.repo.repo;
      core.info(`Detected Issue #${issueNumber}. Posting morale boost.`);
    } else {
      core.warning('This action is intended to run on pull_request or issues events. No comment will be posted.');
      return;
    }

    if (!issueNumber) {
      core.setFailed('Could not determine issue or pull request number from the context.');
      return;
    }

    const { data: comment } = await octokit.rest.issues.createComment({
      owner: repoOwner,
      repo: repoName,
      issue_number: issueNumber,
      body: randomMessage
    });

    core.setOutput('comment-id', comment.id);
    core.info(`Morale boost posted successfully! Comment ID: ${comment.id}`);

  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
