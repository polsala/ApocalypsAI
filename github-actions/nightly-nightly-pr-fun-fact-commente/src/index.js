const core = require('@actions/core');
const github = require('@actions/github');

const FUN_FACTS = [
  "Honey never spoils.",
  "Bananas are berries, but strawberries aren't.",
  "Octopuses have three hearts.",
  "A day on Venus is longer than its year.",
  "There are more stars in the universe than grains of sand on Earth."
];

function getRandomFact() {
  const idx = Math.floor(Math.random() * FUN_FACTS.length);
  return FUN_FACTS[idx];
}

async function run() {
  try {
    const token = core.getInput('github-token', { required: true });
    const fact = getRandomFact();
    core.setOutput('fun_fact', fact);
    core.info(`Selected fun fact: ${fact}`);

    const context = github.context;
    if (!context.payload.pull_request) {
      core.setFailed('No pull request found in context.');
      return;
    }

    const octokit = github.getOctokit(token);
    await octokit.rest.issues.createComment({
      ...context.repo,
      issue_number: context.payload.pull_request.number,
      body: `🤖 **Fun Fact:** ${fact}`
    });
  } catch (error) {
    core.setFailed(error.message);
  }
}

module.exports = { run, getRandomFact };
if (require.main === module) {
  run();
}
