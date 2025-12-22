const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const token = core.getInput('github-token', { required: true });
    const messagesInput = core.getInput('messages');
    const triggerOnFirstPr = core.getBooleanInput('trigger-on-first-pr');
    const triggerOnNoComments = core.getBooleanInput('trigger-on-no-comments');

    const octokit = github.getOctokit(token);
    const { owner, repo } = github.context.repo;
    const prNumber = github.context.payload.pull_request.number;
    const prAuthor = github.context.payload.pull_request.user.login;

    core.info(`Processing PR #${prNumber} by ${prAuthor} in ${owner}/${repo}`);

    const messages = messagesInput.split('\n').map(msg => msg.trim()).filter(msg => msg.length > 0);
    if (messages.length === 0) {
      core.warning('No messages provided. Skipping.');
      return;
    }

    let shouldWhisper = false;

    // Check for no comments
    if (triggerOnNoComments) {
      const { data: comments } = await octokit.rest.issues.listComments({
        owner,
        repo,
        issue_number: prNumber,
      });
      const humanComments = comments.filter(comment => comment.user.type !== 'Bot');
      if (humanComments.length === 0) {
        core.info('No human comments found on this PR. Considering whispering.');
        shouldWhisper = true;
      } else {
        core.info('Human comments found on this PR. Not whispering due to trigger-on-no-comments.');
      }
    } else {
      shouldWhisper = true; // If not checking for no comments, proceed to other checks or whisper
    }

    // Check for first-time contributor
    if (shouldWhisper && triggerOnFirstPr) {
      const { data: pullRequests } = await octokit.rest.pulls.list({
        owner,
        repo,
        state: 'all', // Include open and closed PRs
        creator: prAuthor,
      });

      // Filter out the current PR to count previous PRs
      const previousPrs = pullRequests.filter(pr => pr.number !== prNumber);

      if (previousPrs.length === 0) {
        core.info(`${prAuthor} is a first-time contributor. Considering whispering.`);
        shouldWhisper = true;
      } else {
        core.info(`${prAuthor} has previous PRs. Not whispering due to trigger-on-first-pr.`);
        shouldWhisper = false; // Override previous shouldWhisper if this condition fails
      }
    }

    if (shouldWhisper) {
      const randomMessage = messages[Math.floor(Math.random() * messages.length)];
      core.info(`Whispering: "${randomMessage}"`);
      await octokit.rest.issues.createComment({
        owner,
        repo,
        issue_number: prNumber,
        body: randomMessage,
      });
      core.setOutput('whispered', 'true');
      core.setOutput('message', randomMessage);
    } else {
      core.info('Conditions not met for whispering. Skipping.');
      core.setOutput('whispered', 'false');
    }

  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
