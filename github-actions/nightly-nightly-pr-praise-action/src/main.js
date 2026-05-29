const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const githubToken = core.getInput('github-token', { required: true });
    const customPraiseMessagesInput = core.getInput('praise-messages');

    const octokit = github.getOctokit(githubToken);

    const payload = github.context.payload;

    // Check if the event is a closed and merged pull request
    if (github.context.eventName === 'pull_request' && payload.action === 'closed' && payload.pull_request && payload.pull_request.merged) {
      const prNumber = payload.pull_request.number;
      const repo = payload.repository.name;
      const owner = payload.repository.owner.login;

      core.info(`PR #${prNumber} in ${owner}/${repo} was merged. Preparing praise...`);

      const defaultPraiseMessages = [
        "Huzzah! Another piece of the digital wasteland tamed. Your code shines brighter than a supernova in a void!",
        "Merge successful! The temporal fabric thanks you for this stable contribution. May your commits always be this harmonious.",
        "A beacon of brilliance in the byte-storm! This merge is a testament to your apocalyptic prowess.",
        "The ancient algorithms whisper their approval. Your PR has been absorbed into the grand tapestry of our collective code. Well done, survivor!",
        "By the flickering light of the server racks, we salute your magnificent merge!",
        "Your contribution has fortified our digital fortress. The ApocalypsAI community is stronger for it!"
      ];

      let praiseMessages = defaultPraiseMessages;
      if (customPraiseMessagesInput) {
        const parsedCustomMessages = customPraiseMessagesInput.split('\n').map(msg => msg.trim()).filter(msg => msg.length > 0);
        if (parsedCustomMessages.length > 0) {
          praiseMessages = parsedCustomMessages;
          core.info(`Using ${praiseMessages.length} custom praise messages.`);
        } else {
          core.info('Custom praise messages input was empty or invalid. Using default messages.');
        }
      }

      const randomPraise = praiseMessages[Math.floor(Math.random() * praiseMessages.length)];

      await octokit.rest.issues.createComment({
        owner,
        repo,
        issue_number: prNumber,
        body: `**ApocalypsAI Integrator Agent says:**\n\n${randomPraise}`
      });

      core.info('Praise comment posted successfully!');
    } else {
      core.info('This action only runs on merged pull requests. No praise needed at this time.');
    }
  } catch (error) {
    core.setFailed(error.message);
  }
}

// Only run if not being imported (e.g., in tests)
if (require.main === module) {
  run();
}

module.exports = { run }; // Export for testing
