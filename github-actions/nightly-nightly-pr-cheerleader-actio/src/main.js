const core = require('@actions/core');
const github = require('@actions/github');
const fs = require('fs');

async function run() {
  try {
    const githubToken = core.getInput('github-token', { required: true });
    const reactionEmojisInput = core.getInput('reaction-emojis');
    const affirmationsFilePath = core.getInput('affirmations-file');

    const octokit = github.getOctokit(githubToken);

    const allowedEmojis = reactionEmojisInput.split(',').map(e => e.trim()).filter(Boolean);

    let affirmations = [
      "You're a star! Keep shining!",
      "Fantastic work! The void is proud!",
      "Your brilliance illuminates the darkest corners!",
      "A true beacon of progress!",
      "This is truly apocalyptic-ally awesome!",
      "Keep up the stellar work, survivor!",
      "Your efforts are building a better tomorrow, today!",
      "Magnificent! A triumph against the entropy!",
      "The cosmos applauds your dedication!",
      "Absolutely radiant! What a contribution!"
    ];

    if (affirmationsFilePath) {
      try {
        const customAffirmations = fs.readFileSync(affirmationsFilePath, 'utf8')
                                     .split('\n')
                                     .map(line => line.trim())
                                     .filter(Boolean);
        if (customAffirmations.length > 0) {
          affirmations = customAffirmations;
          core.info(`Loaded ${affirmations.length} custom affirmations from ${affirmationsFilePath}.`);
        } else {
          core.warning(`Custom affirmations file ${affirmationsFilePath} was empty or contained no valid affirmations. Using default list.`);
        }
      } catch (error) {
        core.warning(`Could not read custom affirmations file at ${affirmationsFilePath}: ${error.message}. Using default list.`);
      }
    }

    const { eventName, payload } = github.context;
    let issueNumber;
    let reactionContent;

    if (eventName === 'issue_comment' && payload.action === 'reacted') {
      issueNumber = payload.issue.number;
      reactionContent = payload.reaction.content;
      core.info(`Detected reaction '${reactionContent}' on issue comment #${payload.comment.id} in issue #${issueNumber}.`);
    } else if (eventName === 'pull_request_review_comment' && payload.action === 'reacted') {
      issueNumber = payload.pull_request.number; // PRs are issues
      reactionContent = payload.reaction.content;
      core.info(`Detected reaction '${reactionContent}' on PR review comment #${payload.comment.id} in PR #${issueNumber}.`);
    } else {
      core.info(`Event '${eventName}' with action '${payload.action}' is not a supported reaction event. Skipping.`);
      return;
    }

    if (!issueNumber) {
      core.warning('Could not determine issue or pull request number. Skipping.');
      return;
    }

    if (!allowedEmojis.includes(reactionContent)) {
      core.info(`Reaction '${reactionContent}' is not in the allowed list: ${allowedEmojis.join(', ')}. Skipping.`);
      return;
    }

    const randomAffirmation = affirmations[Math.floor(Math.random() * affirmations.length)];
    const commentToPost = `✨ **Cheerleader Bot says:** ✨\n\n${randomAffirmation}\n\n*(Triggered by a '${reactionContent}' reaction on a comment.)*`;

    core.info(`Posting cheer to issue/PR #${issueNumber}...`);
    const { data: newComment } = await octokit.rest.issues.createComment({
      owner: github.context.repo.owner,
      repo: github.context.repo.repo,
      issue_number: issueNumber,
      body: commentToPost
    });

    core.setOutput('comment-id', newComment.id);
    core.info(`Successfully posted comment ID: ${newComment.id}`);

  } catch (error) {
    core.setFailed(error.message);
  }
}

// Only run if not being imported by a test
if (require.main === module) {
  run();
}

module.exports = run; // Export for testing
