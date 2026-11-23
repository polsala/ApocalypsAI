const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const token = core.getInput('github-token', { required: true });
    const prTitleKeywords = core.getInput('pr-title-keywords').split(',').map(k => k.trim().toLowerCase()).filter(Boolean);
    const prBodyMinLength = parseInt(core.getInput('pr-body-min-length'), 10);
    const maxLinesChanged = parseInt(core.getInput('max-lines-changed'), 10);
    const blessingMessage = core.getInput('blessing-message');
    const failureMessage = core.getInput('failure-message');

    const octokit = github.getOctokit(token);
    const { owner, repo } = github.context.repo;
    const prNumber = github.context.payload.pull_request ? github.context.payload.pull_request.number : null;

    if (!prNumber) {
      core.setFailed('Could not get PR number from context. This action only runs on pull_request events.');
      return;
    }

    const prTitle = github.context.payload.pull_request.title || '';
    const prBody = github.context.payload.pull_request.body || '';
    const additions = github.context.payload.pull_request.additions || 0;
    const deletions = github.context.payload.pull_request.deletions || 0;
    const totalLinesChanged = additions + deletions;

    core.info(`Checking PR #${prNumber}: "${prTitle}"`);
    core.info(`Body length: ${prBody.length}, Total lines changed: ${totalLinesChanged}`);

    let isBlessed = true;
    const reasons = [];

    // Check title keywords
    const titleLower = prTitle.toLowerCase();
    const hasKeyword = prTitleKeywords.some(keyword => titleLower.includes(keyword));
    if (prTitleKeywords.length > 0 && !hasKeyword) {
      isBlessed = false;
      reasons.push(`PR title must contain one of: ${prTitleKeywords.join(', ')}.`);
    }

    // Check body length
    if (prBody.length < prBodyMinLength) {
      isBlessed = false;
      reasons.push(`PR body must be at least ${prBodyMinLength} characters long.`);
    }

    // Check lines changed
    if (totalLinesChanged > maxLinesChanged) {
      isBlessed = false;
      reasons.push(`Total lines changed (${totalLinesChanged}) exceeds maximum allowed (${maxLinesChanged}).`);
    }

    let commentBody;
    if (isBlessed) {
      commentBody = blessingMessage;
      core.info('PR is Celestially Aligned!');
    } else {
      commentBody = `${failureMessage}\n\n**Reasons for non-alignment:**\n${reasons.map(r => `- ${r}`).join('\n')}`;
      core.warning('PR requires further alignment.');
    }

    await octokit.rest.issues.createComment({
      owner,
      repo,
      issue_number: prNumber,
      body: commentBody
    });

    core.setOutput('is-blessed', isBlessed);

    if (!isBlessed) {
      core.setFailed('PR did not achieve Celestial Alignment.');
    }

  } catch (error) {
    core.setFailed(error.message);
  }
}

module.exports = {
  run
};

if (require.main === module) {
  run();
}
