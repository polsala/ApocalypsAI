const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const githubToken = core.getInput('github-token', { required: true });
    const anomalyKeywordsInput = core.getInput('anomaly-keywords');
    const commentTemplate = core.getInput('comment-template');

    const anomalyKeywords = anomalyKeywordsInput.split(',').map(k => k.trim().toLowerCase()).filter(k => k.length > 0);

    const octokit = github.getOctokit(githubToken);

    const pullRequest = github.context.payload.pull_request;

    if (!pullRequest) {
      core.info('This action only runs on pull_request events. Skipping.');
      core.setOutput('anomaly-detected', false);
      return;
    }

    const prTitle = pullRequest.title;
    const prNumber = pullRequest.number;
    const repo = github.context.repo;

    core.info(`Checking PR title: "${prTitle}" for temporal anomalies.`);

    let anomalyDetected = false;
    const detectedKeywords = [];

    for (const keyword of anomalyKeywords) {
      if (prTitle.toLowerCase().includes(keyword)) {
        anomalyDetected = true;
        detectedKeywords.push(keyword);
      }
    }

    core.setOutput('anomaly-detected', anomalyDetected);

    if (anomalyDetected) {
      core.warning(`Temporal anomaly detected in PR title: "${prTitle}" (keywords: ${detectedKeywords.join(', ')})`);
      const commentBody = commentTemplate.replace(/{title}/g, prTitle);

      await octokit.rest.issues.createComment({
        owner: repo.owner,
        repo: repo.repo,
        issue_number: prNumber,
        body: commentBody
      });
      core.info('Comment posted on PR.');
    } else {
      core.info('No temporal anomalies detected. All clear for spacetime stability!');
    }

  } catch (error) {
    core.setFailed(error.message);
  }
}

if (require.main === module) {
  run();
} else {
  module.exports = { run }; // Export for testing
}
