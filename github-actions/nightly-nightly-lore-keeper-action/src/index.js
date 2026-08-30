const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const githubToken = core.getInput('github-token', { required: true });
    const loreKeywordsInput = core.getInput('lore-keywords', { required: true });
    const checkPrTitle = core.getBooleanInput('check-pr-title', { required: false });
    const checkPrBody = core.getBooleanInput('check-pr-body', { required: false });
    const failOnMismatch = core.getBooleanInput('fail-on-mismatch', { required: false });

    const octokit = github.getOctokit(githubToken);
    const pullRequest = github.context.payload.pull_request;

    if (!pullRequest) {
      core.warning('This action only runs on pull_request events. Skipping.');
      core.setOutput('lore-compliant', true);
      return;
    }

    const prTitle = pullRequest.title || '';
    const prBody = pullRequest.body || '';
    const issueNumber = pullRequest.number;

    const loreKeywords = loreKeywordsInput.split(',').map(k => k.trim()).filter(k => k.length > 0);

    let allKeywordsFound = true;
    const missingKeywords = [];

    for (const keyword of loreKeywords) {
      const regex = new RegExp(keyword, 'i'); // Case-insensitive search
      let foundInContent = false;

      if (checkPrTitle && prTitle.match(regex)) {
        foundInContent = true;
      }
      if (checkPrBody && prBody.match(regex)) {
        foundInContent = true;
      }

      if (!foundInContent) {
        allKeywordsFound = false;
        missingKeywords.push(keyword);
      }
    }

    if (!allKeywordsFound) {
      const commentBody = `Greetings, fellow survivor! The Chronal Weave detects a slight temporal distortion in your narrative.\n\nIt seems the following lore elements are missing from your Pull Request title or description:\n\n- ${missingKeywords.join('\n- ')}\n\nPerhaps infuse your message with more echoes of the Void, or a whisper of the Wasteland? Let's keep our lore consistent for the sake of the timeline!`;

      await octokit.rest.issues.createComment({
        owner: github.context.repo.owner,
        repo: github.context.repo.repo,
        issue_number: issueNumber,
        body: commentBody,
      });

      core.setOutput('lore-compliant', false);
      if (failOnMismatch) {
        core.setFailed('Lore compliance check failed. Missing required lore keywords.');
      }
    } else {
      core.info('Lore compliance check passed. Your contribution resonates with the echoes of the void.');
      core.setOutput('lore-compliant', true);
    }

  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
