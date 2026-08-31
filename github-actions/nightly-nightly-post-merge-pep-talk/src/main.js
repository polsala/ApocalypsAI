const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const token = core.getInput('github-token', { required: true });
    const octokit = github.getOctokit(token);

    const pr = github.context.payload.pull_request;

    if (!pr) {
      core.setFailed('This action can only be run on pull_request_target events.');
      return;
    }

    if (!pr.merged) {
      core.info('PR is not merged. Skipping pep talk.');
      return;
    }

    const pepTalks = [
      "Another merge, another step closer to digital salvation! Keep building, survivor.",
      "The code is strong with this one. May your commits be ever green and your deployments swift.",
      "Even in the byte-strewn ruins, your contributions shine like a beacon. Well done!",
      "Remember, every line of code is a shield against the void. You've forged a mighty one today.",
      "Your commit has been assimilated into the collective. Resistance was futile, and now, progress is inevitable. Excellent work!",
      "In the grand tapestry of the apocalypse, your merged PR is a vibrant, uncorrupted thread. Bravo!",
      "May your deployments be as resilient as a cockroach and your bugs as rare as a unicorn. Great job!",
      "The digital wasteland trembles before your merged code. A true architect of the future!",
      "Fear not the compiler's wrath, for your code has passed the ultimate trial. Celebrate this victory!",
      "You've navigated the treacherous waters of code review and emerged victorious. The community salutes you!"
    ];

    const randomPepTalk = pepTalks[Math.floor(Math.random() * pepTalks.length)];

    await octokit.rest.issues.createComment({
      owner: github.context.repo.owner,
      repo: github.context.repo.repo,
      issue_number: pr.number,
      body: `**ApocalypsAI Post-Merge Pep Talk:**\n\n${randomPepTalk}`
    });

    core.info(`Pep talk delivered to PR #${pr.number}.`);

  } catch (error) {
    core.setFailed(error.message);
  }
}

// Export the run function for testing
module.exports = { run };

// Call the run function if not in a test environment
if (require.main === module) {
  run();
}
