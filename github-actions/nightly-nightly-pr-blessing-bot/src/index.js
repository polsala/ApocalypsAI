const core = require('@actions/core');
const github = require('@actions/github');

const affirmations = [
  "May your code be ever-resilient against the digital decay!",
  "Another beacon of hope merged into the main timeline!",
  "The void approves of this contribution. Well done, survivor!",
  "Your commit shines brighter than a supernova in the dark expanse.",
  "In the grand tapestry of the apocalypse, your contribution is a vibrant thread!",
  "This merge strengthens the very fabric of our digital reality. Bravo!",
  "A successful merge! The cosmic dust settles, revealing your brilliance.",
  "Your efforts echo through the temporal rifts. A job well done!",
  "The ancient algorithms whisper their approval for this pristine merge.",
  "May your next commit be as flawless as this merge was impactful!"
];

const emojis = [
  "✨", "🌌", "🚀", "🌟", "💖", "🔮", "🌠", "💫", "🎉", "✅"
];

const quotes = [
  "Even in the darkest timelines, a single line of code can ignite a new dawn. - The Compiler's Creed",
  "The future is not written, but coded. And you, my friend, are a master scribe. - Oracle of the Binary Star",
  "Through the static and the noise, your contribution rings clear. - Echoes from the Server Graveyard",
  "To merge is to transcend. To build is to survive. - The Architect's Axiom",
  "Let your code be a shield against the entropy. - The Last Debugger's Lament"
];

function getRandomElement(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

async function run() {
  try {
    const githubToken = core.getInput('github-token', { required: true });
    const blessingType = core.getInput('blessing-type') || 'affirmation';

    const octokit = github.getOctokit(githubToken);
    const { owner, repo } = github.context.repo;

    if (github.context.eventName !== 'pull_request' || github.context.payload.action !== 'closed' || !github.context.payload.pull_request.merged) {
      core.info('This action only runs on merged pull requests. Skipping.');
      return;
    }

    const prNumber = github.context.payload.pull_request.number;
    let blessingMessage;

    switch (blessingType.toLowerCase()) {
      case 'emoji':
        blessingMessage = getRandomElement(emojis);
        break;
      case 'quote':
        blessingMessage = getRandomElement(quotes);
        break;
      case 'affirmation':
      default:
        blessingMessage = getRandomElement(affirmations);
        break;
    }

    await octokit.rest.issues.createComment({
      owner,
      repo,
      issue_number: prNumber,
      body: `✨ ApocalypsAI Blessing ✨\n\n${blessingMessage}`
    });

    core.setOutput('blessing-message', blessingMessage);
    core.info(`Posted blessing to PR #${prNumber}: "${blessingMessage}"`);

  } catch (error) {
    core.setFailed(error.message);
  }
}

// Export the run function for testing
module.exports = {
  run
};

// Call run directly when the script is executed
if (require.main === module) {
  run();
}
