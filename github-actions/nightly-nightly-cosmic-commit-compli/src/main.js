const core = require('@actions/core');
const github = require('@actions/github');

const cosmicCompliments = [
  "Your code shines brighter than a supernova!",
  "A truly stellar contribution, worthy of the cosmos!",
  "You've engineered a masterpiece, a true cosmic marvel!",
  "This commit is a gravitational pull towards perfection!",
  "Your logic is as clear and vast as the Milky Way!",
  "Behold, a celestial achievement in code!",
  "Your work is out of this world!",
  "May your commits always be as brilliant as a distant quasar!",
  "This code is a beacon of light in the darkest void!",
  "You've aligned the stars with this magnificent contribution!"
];

async function run() {
  try {
    const githubToken = core.getInput('github-token', { required: true });
    const complimentTarget = core.getInput('compliment-target');
    const customCompliment = core.getInput('compliment-message');

    const octokit = github.getOctokit(githubToken);
    const { owner, repo } = github.context.repo;

    let compliment = customCompliment || cosmicCompliments[Math.floor(Math.random() * cosmicCompliments.length)];
    core.setOutput('compliment', compliment);

    if (complimentTarget === 'pr-merge' && github.context.eventName === 'pull_request_target') {
      const pr = github.context.payload.pull_request;
      if (pr && pr.merged) {
        core.info(`PR #${pr.number} was merged. Posting cosmic compliment.`);
        await octokit.rest.issues.createComment({
          owner,
          repo,
          issue_number: pr.number,
          body: `✨ **Cosmic Compliment from ApocalypsAI:** ✨\n\n${compliment}`
        });
        core.info(`Compliment posted on PR #${pr.number}.`);
      } else {
        core.info(`PR #${pr.number} was closed but not merged. No compliment.`);
      }
    } else if (complimentTarget === 'push' && github.context.eventName === 'push') {
      const commitSha = github.context.sha;
      core.info(`Push event detected for commit ${commitSha}. Posting cosmic compliment.`);
      await octokit.rest.repos.createCommitComment({
        owner,
        repo,
        commit_sha: commitSha,
        body: `✨ **Cosmic Compliment from ApocalypsAI:** ✨\n\n${compliment}`
      });
      core.info(`Compliment posted on commit ${commitSha}.`);
    } else {
      core.warning(`Action triggered by unsupported event type or target: ${github.context.eventName} with target ${complimentTarget}. No compliment posted.`);
    }

  } catch (error) {
    core.setFailed(error.message);
  }
}

// Only run if this file is executed directly (not imported as a module)
if (require.main === module) {
  run();
}

module.exports = {
  run
};
