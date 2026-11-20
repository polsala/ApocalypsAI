const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const token = core.getInput('github-token', { required: true });
    const whimsyKeywordsInput = core.getInput('whimsy-keywords');
    const grimKeywordsInput = core.getInput('grim-keywords');
    const minWhimsyCount = parseInt(core.getInput('min-whimsy-count'), 10);
    const failOnGrim = core.getInput('fail-on-grim') === 'true';

    const whimsyKeywords = whimsyKeywordsInput.split(',').map(k => k.trim().toLowerCase()).filter(k => k.length > 0);
    const grimKeywords = grimKeywordsInput.split(',').map(k => k.trim().toLowerCase()).filter(k => k.length > 0);

    const octokit = github.getOctokit(token);

    const pullRequest = github.context.payload.pull_request;

    if (!pullRequest) {
      core.setFailed('This action only runs on pull_request events.');
      return;
    }

    const prTitle = pullRequest.title || '';
    const prBody = pullRequest.body || '';
    const prContent = `${prTitle} ${prBody}`.toLowerCase();

    let whimsyScore = 0;
    for (const keyword of whimsyKeywords) {
      const regex = new RegExp(`\\b${keyword}\\b`, 'g'); // Whole word match
      const matches = prContent.match(regex);
      if (matches) {
        whimsyScore += matches.length;
      }
    }

    let grimFound = false;
    const foundGrimWords = [];
    for (const keyword of grimKeywords) {
      const regex = new RegExp(`\\b${keyword}\\b`, 'g'); // Whole word match
      if (prContent.match(regex)) {
        grimFound = true;
        foundGrimWords.push(keyword);
      }
    }

    core.info(`Whimsy Score: ${whimsyScore}`);
    core.info(`Grim Keywords Found: ${grimFound ? 'Yes' : 'No'}`);
    if (foundGrimWords.length > 0) {
      core.info(`Specific grim words: ${foundGrimWords.join(', ')}`);
    }

    let validationStatus = 'success';
    let commentBody = '';

    if (whimsyScore < minWhimsyCount) {
      validationStatus = 'warning';
      commentBody += `### \uD83C\uDF1F Whimsy Alert! \uD83C\uDF1F\n\nYour PR needs more sparkle! Found ${whimsyScore} whimsical keywords, but at least ${minWhimsyCount} are required.\n\n`;
      core.warning(`PR does not meet minimum whimsy count (${whimsyScore}/${minWhimsyCount}).`);
    }

    if (grimFound) {
      validationStatus = failOnGrim ? 'failure' : 'warning';
      commentBody += `### \uD83D\uDC80 Grimness Detected! \uD83D\uDC80\n\nFound grim keywords: ${foundGrimWords.map(w => `\`${w}\``).join(', ')}. Let's keep things cheerful!\n\n`;
      if (failOnGrim) {
        core.setFailed(`Grim keywords found: ${foundGrimWords.join(', ')}. Failing check as 'fail-on-grim' is true.`);
      } else {
        core.warning(`Grim keywords found: ${foundGrimWords.join(', ')}. This is a warning.`);
      }
    }

    if (commentBody) {
      await octokit.rest.issues.createComment({
        owner: github.context.repo.owner,
        repo: github.context.repo.repo,
        issue_number: pullRequest.number,
        body: commentBody + 'Consider adding more delightful phrases to your title or description!'
      });
    }

    core.setOutput('whimsy-score', whimsyScore);
    core.setOutput('grim-found', grimFound);
    core.setOutput('validation-status', validationStatus);

  } catch (error) {
    core.setFailed(error.message);
  }
}

// Export the run function for testing
module.exports = {
  run
};

// Call run() if not in a test environment
if (require.main === module) {
  run();
}
