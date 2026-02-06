const core = require('@actions/core');
const github = require('@actions/github');
const fs = require('fs');
const path = require('path');

async function run() {
  try {
    const githubToken = core.getInput('github-token', { required: true });
    const targetType = core.getInput('target-type') || 'pr-comment';
    const statusContext = core.getInput('status-context') || 'build-omen-oracle';

    const octokit = github.getOctokit(githubToken);

    // Load omens from omens.json
    const omensPath = path.join(__dirname, 'omens.json');
    const omens = JSON.parse(fs.readFileSync(omensPath, 'utf8'));

    // Select a random omen
    const selectedOmen = omens[Math.floor(Math.random() * omens.length)];
    core.setOutput('omen', selectedOmen);

    const { owner, repo } = github.context.repo;

    if (targetType === 'pr-comment') {
      const prNumber = github.context.payload.pull_request?.number;

      if (!prNumber) {
        core.warning('No pull request found in context. Skipping PR comment.');
        return;
      }

      core.info(`Posting omen to PR #${prNumber}: "${selectedOmen}"`);
      await octokit.rest.issues.createComment({
        owner,
        repo,
        issue_number: prNumber,
        body: `🔮 Build Omen Oracle says: ${selectedOmen}`
      });
      core.info('Omen posted as PR comment.');

    } else if (targetType === 'commit-status') {
      const sha = github.context.sha;

      core.info(`Setting commit status for ${sha} with omen: "${selectedOmen}"`);
      await octokit.rest.repos.createCommitStatus({
        owner,
        repo,
        sha,
        state: 'success', // Always success as it runs on success()
        description: selectedOmen,
        context: statusContext
      });
      core.info('Omen posted as commit status.');

    } else {
      core.setFailed(`Invalid target-type: ${targetType}. Must be 'pr-comment' or 'commit-status'.`);
    }

  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
