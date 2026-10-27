const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const token = core.getInput('github-token', { required: true });
    const alignedKeywordsInput = core.getInput('aligned-keywords');
    const misalignedKeywordsInput = core.getInput('misaligned-keywords');
    const alignmentThreshold = parseInt(core.getInput('alignment-threshold') || '1', 10);
    const misalignmentThreshold = parseInt(core.getInput('misalignment-threshold') || '1', 10);
    const commentOnAlignment = core.getInput('comment-on-alignment') === 'true';
    const commentOnMisalignment = core.getInput('comment-on-misalignment') === 'true';

    const alignedKeywords = alignedKeywordsInput.split(',').map(k => k.trim().toLowerCase()).filter(Boolean);
    const misalignedKeywords = misalignedKeywordsInput.split(',').map(k => k.trim().toLowerCase()).filter(Boolean);

    const pullRequest = github.context.payload.pull_request;

    if (!pullRequest) {
      core.setFailed('This action only runs on pull_request events.');
      return;
    }

    const prTitle = pullRequest.title.toLowerCase();
    const prBody = (pullRequest.body || '').toLowerCase();
    const prNumber = pullRequest.number;

    let alignedCount = 0;
    let misalignedCount = 0;

    for (const keyword of alignedKeywords) {
      if (prTitle.includes(keyword) || prBody.includes(keyword)) {
        alignedCount++;
      }
    }

    for (const keyword of misalignedKeywords) {
      if (prTitle.includes(keyword) || prBody.includes(keyword)) {
        misalignedCount++;
      }
    }

    const octokit = github.getOctokit(token);
    const repo = github.context.repo;

    let isAligned = false;
    let commentMessage = '';

    if (misalignedCount >= misalignmentThreshold) {
      isAligned = false;
      if (commentOnMisalignment) {
        commentMessage = `### 🌠 Cosmic Alignment Alert! 🌠\n\nIt seems the celestial bodies are suggesting a slight adjustment to this Pull Request. The current title or description might contain keywords (${misalignedKeywords.filter(k => prTitle.includes(k) || prBody.includes(k)).join(', ')}) that indicate a temporary or unaligned state.\n\nConsider refining your message to better reflect the stellar purpose of this contribution! A clearer path leads to a brighter galaxy. ✨`;
      }
    } else if (alignedCount >= alignmentThreshold) {
      isAligned = true;
      if (commentOnAlignment) {
        commentMessage = `### ✨ Stellar Contribution Detected! ✨\n\nThe cosmic energies align perfectly with this Pull Request! Your contribution is radiating positive vibes across the repository. Keep up the harmonious work! 🚀`;
      }
    } else {
      // Neither strongly aligned nor misaligned, default to not aligned for caution
      isAligned = false;
      if (commentOnMisalignment) {
        commentMessage = `### 🌌 A Whisper from the Void 🌌\n\nThis Pull Request is a mystery to the cosmos! While not misaligned, it lacks strong indicators of cosmic purpose. Perhaps a few more aligned keywords or a clearer description would help the universe understand its true potential. 🌟`;
      }
    }

    if (commentMessage) {
      await octokit.rest.issues.createComment({
        owner: repo.owner,
        repo: repo.repo,
        issue_number: prNumber,
        body: commentMessage,
      });
      core.info(`Commented on PR #${prNumber}:\n${commentMessage}`);
    }

    core.setOutput('is-aligned', isAligned);
    core.info(`PR #${prNumber} is-aligned: ${isAligned}`);

  } catch (error) {
    core.setFailed(error.message);
  }
}

module.exports = run;
