const core = require('@actions/core');
const github = require('@actions/github');

// List of whimsical fortunes
const FORTUNES = [
  "You will find a hidden stash of snacks in the breakroom.",
  "A mysterious stranger will bring you a gift of code.",
  "Your next commit will be blessed by the gods of CI.",
  "Beware the silent bug that lurks in the shadows.",
  "A coffee spill will reveal a brilliant idea.",
  "The stars align for a successful merge.",
  "A stray semicolon will cause a minor adventure.",
  "Your IDE will whisper a secret shortcut.",
  "A forgotten comment will become legendary.",
  "The build will succeed on the third try.",
  "A new branch will sprout like a spring flower.",
  "Your tests will pass with flying colors.",
  "A typo will lead to an unexpected feature.",
  "The repository will gain a new contributor soon.",
  "A bug will turn into a feature by happy accident.",
  "Your pull request will be reviewed with kindness.",
  "A hidden comment will be discovered by future generations.",
  "The CI pipeline will sing a happy tune.",
  "Your code will be refactored into pure poetry.",
  "A mysterious log will reveal a hidden truth."
];

/**
 * Returns a random fortune from the list.
 * @returns {string}
 */
function getFortune() {
  const idx = Math.floor(Math.random() * FORTUNES.length);
  return FORTUNES[idx];
}

/**
 * Main entry point for the GitHub Action.
 */
async function run() {
  try {
    const token = core.getInput('github-token', { required: true });
    const context = github.context;

    // Only act on newly opened issues
    if (context.eventName !== 'issues' || context.payload.action !== 'opened') {
      core.info('Event is not a newly opened issue – exiting.');
      return;
    }

    const issueNumber = context.payload.issue.number;
    const owner = context.repo.owner;
    const repo = context.repo.repo;
    const fortune = getFortune();

    const octokit = github.getOctokit(token);
    await octokit.rest.issues.createComment({
      owner,
      repo,
      issue_number: issueNumber,
      body: `🔮 **Fortune:** ${fortune}`
    });
    core.info(`Posted fortune to issue #${issueNumber}`);
  } catch (error) {
    core.setFailed(error.message);
  }
}

module.exports = { getFortune, run };

if (require.main === module) {
  run();
}
