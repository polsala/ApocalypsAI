const core = require('@actions/core');
const github = require('@actions/github');

function generateWhimsicalMessage(conclusion) {
  switch (conclusion) {
    case 'success':
      const successMessages = [
        "Huzzah! The gears of destiny turn smoothly. Your workflow danced a jig and won!",
        "Victory! The digital spirits rejoice. Your code is a beacon in the void.",
        "A flawless execution! Even the cosmic dust bunnies are applauding.",
        "Success! The matrix hums with contentment. Another step towards a brighter tomorrow.",
        "Behold, a triumph! Your workflow has achieved peak whimsy and functionality."
      ];
      return successMessages[Math.floor(Math.random() * successMessages.length)];
    case 'failure':
      const failureMessages = [
        "Oh dear, a temporal hiccup! The workflow stumbled, but fear not, the void offers second chances.",
        "Alas, the cosmic alignment was off! Your workflow encountered a glitch in the matrix. Debug with courage!",
        "A momentary lapse in the spacetime continuum! The workflow faltered, but every failure is a lesson.",
        "The digital gremlins had their fun! Your workflow hit a snag. A cup of tea and a fresh perspective might help.",
        "Worry not, brave coder! The universe merely tests your resolve. This workflow shall rise again!"
      ];
      return failureMessages[Math.floor(Math.random() * failureMessages.length)];
    case 'cancelled':
      const cancelledMessages = [
        "A strategic retreat! The workflow decided to ponder its existence another day.",
        "The cosmic winds shifted! Your workflow chose a different path. Perhaps a nap was in order.",
        "Interrupted by the whispers of the void! The workflow paused, awaiting new directives.",
        "A moment of reflection! The workflow was called back, but its spirit remains.",
        "The journey was cut short, but the wisdom gained endures. Onward to the next adventure!"
      ];
      return cancelledMessages[Math.floor(Math.random() * cancelledMessages.length)];
    default:
      return `The workflow concluded with '${conclusion}'. The universe offers its neutral observation.`;
  }
}

async function run() {
  try {
    const githubToken = core.getInput('github-token', { required: true });
    const workflowConclusion = core.getInput('workflow-conclusion', { required: true });
    const prNumber = core.getInput('pr-number');

    const message = generateWhimsicalMessage(workflowConclusion);
    core.setOutput('whimsical-message', message);

    if (prNumber) {
      const octokit = github.getOctokit(githubToken);
      const { owner, repo } = github.context.repo;

      core.info(`Posting comment on PR #${prNumber} in ${owner}/${repo}...`);
      const { data: comment } = await octokit.rest.issues.createComment({
        owner,
        repo,
        issue_number: prNumber,
        body: `### Nightly Workflow Whimsy Agent Says:\n\n${message}`
      });
      core.setOutput('comment-id', comment.id);
      core.info(`Comment posted: ${comment.html_url}`);
    } else {
      core.info('No PR number provided. Skipping comment posting.');
    }

  } catch (error) {
    core.setFailed(error.message);
  }
}

// Export for testing
module.exports = {
  generateWhimsicalMessage,
  run
};

// Only run if not being tested
if (require.main === module) {
  run();
}
