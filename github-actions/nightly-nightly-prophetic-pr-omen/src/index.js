const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const prTitle = core.getInput('pr-title', { required: true });
    const prBody = core.getInput('pr-body');
    const githubToken = core.getInput('github-token', { required: true });

    const omens = [
      "The ancient scrolls foretell: this code shall compile on the first try, or summon a thousand tiny bugs.",
      "A whisper from the void: your changes ripple through the cosmos. Expect either enlightenment or a cosmic rollback.",
      "Behold! The prophecy states: this Pull Request will either bring forth a golden age of stability or a cascade of 'works on my machine' debates.",
      "The stars align: a new feature emerges! Will it be a beacon of innovation or a black hole of technical debt?",
      "The runes reveal: tests shall pass, but the true challenge lies in the user acceptance phase. Prepare for the unexpected.",
      "From the depths of the commit history: a refactor approaches. Will it cleanse the codebase or stir the slumbering kraken?",
      "The oracle speaks: your dependencies are restless. A minor version bump could unleash chaos or harmony.",
      "A fleeting vision: this merge will either be swift and silent, or echo with the cries of broken pipelines.",
      "The cosmic dust settles: performance gains are within reach, but watch out for the phantom memory leak.",
      "The great debugger foresees: a single line change, a universe of impact. Choose wisely, young padawan."
    ];

    const seed = (prTitle + (prBody || '')).length;
    const omenIndex = seed % omens.length;
    const omenMessage = omens[omenIndex];

    core.setOutput('omen-message', omenMessage);

    // Add a comment to the PR
    if (github.context.payload.pull_request) {
      const octokit = github.getOctokit(githubToken);
      const { owner, repo } = github.context.repo;
      const issue_number = github.context.payload.pull_request.number;

      await octokit.rest.issues.createComment({
        owner,
        repo,
        issue_number,
        body: `✨ ApocalypsAI Prophetic Omen ✨\n\n${omenMessage}`
      });
      core.info(`Commented on PR #${issue_number}: ${omenMessage}`);
    } else {
      core.warning('Not a pull request event. Omen will only be set as output, not commented.');
    }

  } catch (error) {
    core.setFailed(error.message);
  }
}

module.exports = { run };
