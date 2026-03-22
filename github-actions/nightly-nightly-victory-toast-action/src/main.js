const core = require('@actions/core');
const github = require('@actions/github');

const WHIMSICAL_MESSAGES = [
  "The gears grind no more! Victory is ours, for now.",
  "Dust settles, code runs. Another day, another triumph!",
  "Behold! The apocalypse has been momentarily postponed by our sheer brilliance.",
  "Systems nominal! Time for a celebratory nutrient paste.",
  "Against all odds, the bits aligned. Rejoice, fellow survivors!",
  "The void whispers approval. Or maybe that's just the server fan.",
  "Code compiled, tests passed, world saved (temporarily).",
  "Another successful cycle. The machines are pleased.",
  "Our digital fortress holds! For now, we feast on bytes.",
  "Victory! Now, back to scavenging for more coffee."
];

async function run() {
  try {
    const customMessage = core.getInput('message');
    const githubToken = core.getInput('github-token', { required: true });
    const targetPrNumber = core.getInput('target-pr-number');
    const targetIssueNumber = core.getInput('target-issue-number');

    const octokit = github.getOctokit(githubToken);

    let issueNumber = null;
    let isPullRequest = false;

    if (targetIssueNumber) {
      issueNumber = parseInt(targetIssueNumber, 10);
      if (isNaN(issueNumber)) {
        core.setFailed(`Invalid 'target-issue-number': ${targetIssueNumber}`);
        return;
      }
    } else if (targetPrNumber) {
      issueNumber = parseInt(targetPrNumber, 10);
      isPullRequest = true;
      if (isNaN(issueNumber)) {
        core.setFailed(`Invalid 'target-pr-number': ${targetPrNumber}`);
        return;
      }
    } else if (github.context.payload.pull_request) {
      issueNumber = github.context.payload.pull_request.number;
      isPullRequest = true;
    } else if (github.context.payload.issue) {
      issueNumber = github.context.payload.issue.number;
    }

    if (!issueNumber) {
      core.info('No target PR or Issue found in context or inputs. Logging victory message instead of commenting.');
      const message = customMessage || WHIMSICAL_MESSAGES[Math.floor(Math.random() * WHIMSICAL_MESSAGES.length)];
      core.info(`Victory Message: ${message}`);
      return;
    }

    const owner = github.context.repo.owner;
    const repo = github.context.repo.repo;
    const message = customMessage || WHIMSICAL_MESSAGES[Math.floor(Math.random() * WHIMSICAL_MESSAGES.length)];

    core.info(`Posting victory toast to ${isPullRequest ? 'PR' : 'Issue'} #${issueNumber} in ${owner}/${repo}...`);

    const { data: comment } = await octokit.rest.issues.createComment({
      owner,
      repo,
      issue_number: issueNumber,
      body: `🎉 **Victory Toast!** 🎉\n\n${message}`
    });

    core.info(`Comment posted: ${comment.html_url}`);
    core.setOutput('comment-url', comment.html_url);

  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
