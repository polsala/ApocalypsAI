const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const token = core.getInput('github-token');
    const optimismMessagesInput = core.getInput('optimism-messages');
    const negativeKeywordsInput = core.getInput('negative-keywords');
    const threshold = parseInt(core.getInput('threshold'), 10);

    const octokit = github.getOctokit(token);
    const context = github.context;

    let title = '';
    let body = '';
    let issueNumber = 0;

    if (context.payload.pull_request) {
      title = context.payload.pull_request.title;
      body = context.payload.pull_request.body || '';
      issueNumber = context.payload.pull_request.number;
    } else if (context.payload.issue) {
      title = context.payload.issue.title;
      body = context.payload.issue.body || '';
      issueNumber = context.payload.issue.number;
    } else {
      core.info('This action only runs on pull_request or issue events. Skipping.');
      return;
    }

    if (!issueNumber) {
      core.info('Could not determine issue or pull request number. Skipping.');
      return;
    }

    const textToAnalyze = `${title} ${body}`.toLowerCase();
    const negativeKeywords = negativeKeywordsInput.split(',').map(k => k.trim()).filter(k => k.length > 0);
    const optimismMessages = optimismMessagesInput.split('\n').map(m => m.trim()).filter(m => m.length > 0);

    let negativeCount = 0;
    for (const keyword of negativeKeywords) {
      if (textToAnalyze.includes(keyword)) {
        negativeCount++;
      }
    }

    core.info(`Detected ${negativeCount} negative keywords. Threshold is ${threshold}.`);

    if (negativeCount >= threshold) {
      const randomMessage = optimismMessages[Math.floor(Math.random() * optimismMessages.length)];
      core.info(`Injecting optimism: \"${randomMessage}\"
`);

      await octokit.rest.issues.createComment({
        owner: context.repo.owner,
        repo: context.repo.repo,
        issue_number: issueNumber,
        body: `_A Glimmer of Optimism from ApocalypsAI_:\n\n${randomMessage}`
      });
      core.setOutput('optimism-injected', 'true');
    } else {
      core.info('No significant negative sentiment detected. No optimism injected.');
      core.setOutput('optimism-injected', 'false');
    }

  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
