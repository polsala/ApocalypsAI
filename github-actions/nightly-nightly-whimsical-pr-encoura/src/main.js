const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const githubToken = core.getInput('github-token', { required: true });
    const customMessagesInput = core.getInput('messages');

    const defaultMessages = [
      "Behold, a new PR sprouts! May your code be as robust as a mutant cactus in the wasteland.",
      "A wild PR appeared! It's super effective! Go forth and conquer, brave coder!",
      "The stars align, the void whispers... and a Pull Request is born! May its path be bug-free and its merges swift.",
      "Greetings, traveler! Your PR has arrived, bearing gifts of code. May the ancient algorithms bless its journey.",
      "The ApocalypsAI Integrator smiles upon this Pull Request. May your merge be legendary!",
      "A beacon of code in the digital night! This PR shines brightly. Keep up the excellent work!",
      "From the depths of the repository, a new contribution emerges! We salute your efforts!",
      "Your code is like a rare artifact found in the ruins – precious and full of potential. Well done!",
      "May your commits be many and your conflicts few. This PR is a step towards a brighter future!",
      "The digital winds carry whispers of your genius. This Pull Request is a testament to it!"
    ];

    let customMessages = [];
    if (customMessagesInput) {
      try {
        customMessages = JSON.parse(customMessagesInput);
        if (!Array.isArray(customMessages)) {
          throw new Error('Custom messages must be a JSON array.');
        }
      } catch (error) {
        core.warning(`Could not parse custom messages: ${error.message}. Using default messages only.`);
        customMessages = [];
      }
    }

    const allMessages = customMessages.length > 0 ? customMessages : defaultMessages;
    const chosenMessage = allMessages[Math.floor(Math.random() * allMessages.length)];

    const octokit = github.getOctokit(githubToken);
    const { owner, repo } = github.context.repo;
    const pullRequestNumber = github.context.payload.pull_request.number;

    if (!pullRequestNumber) {
      core.setFailed('Could not get Pull Request number from context. This action should run on pull_request_target.');
      return;
    }

    const { data: comment } = await octokit.rest.issues.createComment({
      owner,
      repo,
      issue_number: pullRequestNumber,
      body: chosenMessage
    });

    core.setOutput('comment-id', comment.id);
    core.info(`Posted whimsical encouragement to PR #${pullRequestNumber}: "${chosenMessage}"`);

  } catch (error) {
    core.setFailed(error.message);
  }
}

if (require.main === module) {
  run();
}

module.exports = { run }; // Export for testing
