const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const githubToken = core.getInput('github-token', { required: true });
    const setStatusCheck = core.getInput('set-status-check') === 'true';

    const octokit = github.getOctokit(githubToken);

    const pr = github.context.payload.pull_request;
    if (!pr) {
      core.setFailed('This action can only run on pull_request events.');
      return;
    }

    const blessings = [
      "The cosmic dust motes align for this PR. Merge with stardust!",
      "A celestial choir sings praises for your code. Proceed, brave developer!",
      "The void whispers approval. Your changes are destined for greatness.",
      "Beware the space-time continuum, but your PR is safe. For now.",
      "May your merges be swift and your conflicts few, as decreed by the Great Architect of the Universe.",
      "Your code resonates with the universal hum. It is blessed.",
      "The stars have foretold this merge. It shall be glorious!",
      "A ripple in the space-time fabric confirms: this PR is good to go.",
      "By the power of the moon and the stars, this PR is deemed worthy.",
      "The ancient cosmic algorithms have validated your changes. Proceed!"
    ];

    const blessingMessage = blessings[Math.floor(Math.random() * blessings.length)];
    core.setOutput('blessing-message', blessingMessage);
    core.info(`Cosmic Blessing: ${blessingMessage}`);

    // Post comment to PR
    await octokit.rest.issues.createComment({
      owner: github.context.repo.owner,
      repo: github.context.repo.repo,
      issue_number: pr.number,
      body: `✨ **Cosmic Blessing Initiated!** ✨\n\n${blessingMessage}\n\n_May your merges be swift and your deployments smooth._`
    });
    core.info(`Comment posted to PR #${pr.number}.`);

    // Set status check
    if (setStatusCheck) {
      await octokit.rest.repos.createCommitStatus({
        owner: github.context.repo.owner,
        repo: github.context.repo.repo,
        sha: pr.head.sha,
        state: 'success',
        target_url: `https://github.com/${github.context.repo.owner}/${github.context.repo.repo}/pull/${pr.number}/checks`,
        description: blessingMessage,
        context: 'Cosmic Blessing'
      });
      core.info(`Status check "Cosmic Blessing" set to success for commit ${pr.head.sha}.`);
    }

  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
