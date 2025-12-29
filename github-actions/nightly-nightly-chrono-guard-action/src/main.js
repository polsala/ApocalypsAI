const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const githubToken = core.getInput('github-token', { required: true });
    const keywordsInput = core.getInput('keywords', { required: false });
    const keywords = keywordsInput.split(',').map(k => k.trim().toLowerCase()).filter(k => k.length > 0);

    const octokit = github.getOctokit(githubToken);
    const { owner, repo } = github.context.repo;
    const prNumber = github.context.payload.pull_request?.number;

    if (!prNumber) {
      core.info('Not a pull request event. Skipping chrono-guard scan.');
      core.setOutput('temporal-anomaly-detected', false);
      return;
    }

    const pr = await octokit.rest.pulls.get({
      owner,
      repo,
      pull_number: prNumber,
    });

    const prTitle = pr.data.title.toLowerCase();
    let detectedKeywords = [];

    // Check PR title
    for (const keyword of keywords) {
      if (prTitle.includes(keyword)) {
        detectedKeywords.push(keyword);
      }
    }

    // Check commit messages
    const commits = await octokit.rest.pulls.listCommits({
      owner,
      repo,
      pull_number: prNumber,
    });

    for (const commit of commits.data) {
      const commitMessage = commit.commit.message.toLowerCase();
      for (const keyword of keywords) {
        if (commitMessage.includes(keyword) && !detectedKeywords.includes(keyword)) {
          detectedKeywords.push(keyword);
        }
      }
    }

    if (detectedKeywords.length > 0) {
      const warningMessage = `🕰️ **Temporal Anomaly Detected!** 🕰️\n\n` +
                             `The Chrono-Guard has detected keywords related to temporal distortions in this Pull Request.\n` +
                             `Detected keywords: \`${detectedKeywords.join(', ')}\`\n\n` +
                             `Please ensure no timelines are being inadvertently (or advertently!) altered. Proceed with caution.\n` +
                             `_This is an automated warning from the ApocalypsAI Nightly Integrator._`;

      await octokit.rest.issues.createComment({
        owner,
        repo,
        issue_number: prNumber,
        body: warningMessage,
      });
      core.warning(`Temporal anomaly detected in PR #${prNumber}. Keywords: ${detectedKeywords.join(', ')}`);
      core.setOutput('temporal-anomaly-detected', true);
    } else {
      core.info('No temporal anomaly keywords detected.');
      core.setOutput('temporal-anomaly-detected', false);
    }

  } catch (error) {
    core.setFailed(error.message);
    core.setOutput('temporal-anomaly-detected', false);
  }
}

if (require.main === module) {
  run();
} else {
  module.exports = { run }; // Export for testing
}
