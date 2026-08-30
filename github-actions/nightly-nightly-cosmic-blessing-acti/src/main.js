const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const token = core.getInput('token', { required: true });
    const customBlessingsInput = core.getInput('blessings');

    const defaultBlessings = [
      "The cosmic dust motes align! Your changes have been blessed by the Elder Stars. ✨",
      "A ripple in the spacetime continuum confirms: this merge is *chef's kiss*. 🌌",
      "The Interdimensional Bureau of Code Quality has stamped this 'Approved by Squishy Tentacles'. 🐙",
      "May your next commit be as glorious as a supernova, and your bugs as rare as a unicorn's sneeze. 🦄",
      "By the power of the Andromeda Galaxy, this workflow is complete! Well done! 🌠",
      "The ancient prophecies foretold this success. You are truly a cosmic developer! 🔮",
      "A celestial choir sings praises for your impeccable work. Hallelujah! 🎶",
      "Your code has achieved peak enlightenment. The universe applauds! 👏",
      "The fabric of reality shimmers with your triumph. Keep up the stellar work! 💫",
      "Even the black holes are impressed. This is truly magnificent! ⚫"
    ];

    const blessings = customBlessingsInput ? customBlessingsInput.split(',').map(b => b.trim()) : defaultBlessings;
    const chosenBlessing = blessings[Math.floor(Math.random() * blessings.length)];

    const octokit = github.getOctokit(token);
    const context = github.context;

    let issueNumber;
    if (context.payload.pull_request) {
      issueNumber = context.payload.pull_request.number;
    } else if (context.payload.issue) {
      issueNumber = context.payload.issue.number;
    } else if (context.eventName === 'push' && context.payload.head_commit) {
      // For push events, we might want to comment on the commit itself or find associated PRs.
      // For simplicity, let's skip if not a PR or issue for now, or find a recent PR.
      // A more robust solution might involve searching for PRs associated with the commit SHA.
      // For this utility, let's focus on PRs and issues where a clear 'issue_number' exists.
      core.info('Not a pull request or issue event. Skipping comment.');
      core.setOutput('blessing-message', 'No comment posted (not PR/issue event).');
      return;
    } else {
      core.info('Could not determine issue or pull request number from context. Skipping comment.');
      core.setOutput('blessing-message', 'No comment posted (context unclear).');
      return;
    }

    if (issueNumber) {
      await octokit.rest.issues.createComment({
        owner: context.repo.owner,
        repo: context.repo.repo,
        issue_number: issueNumber,
        body: chosenBlessing
      });
      core.info(`Posted cosmic blessing to #${issueNumber}: ${chosenBlessing}`);
      core.setOutput('blessing-message', chosenBlessing);
    } else {
      core.info('No issue or pull request number found to post a comment.');
      core.setOutput('blessing-message', 'No comment posted (no issue/PR number).');
    }

  } catch (error) {
    core.setFailed(error.message);
  }
}

// Export for testing, run directly when executed as main script
if (require.main === module) {
  run();
} else {
  module.exports = { run };
}
