const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const token = core.getInput('github-token', { required: true });
    const octokit = github.getOctokit(token);

    const { owner, repo } = github.context.repo;
    const pr = github.context.payload.pull_request;

    if (!pr) {
      core.warning('This action only runs on pull_request events.');
      return;
    }

    if (!pr.merged) {
      core.info('PR is not merged. No affirmation needed.');
      return;
    }

    core.info(`Checking status for merged PR #${pr.number} (commit: ${pr.head.sha})...`);

    // Fetch all check runs for the head commit of the PR
    const { data: checkRuns } = await octokit.rest.checks.listForRef({
      owner,
      repo,
      ref: pr.head.sha,
    });

    let allChecksPassed = true;
    if (checkRuns.check_runs.length === 0) {
      core.warning('No check runs found for this commit. Assuming success for blessing.');
    } else {
      for (const checkRun of checkRuns.check_runs) {
        // We only care about completed checks that are not 'success'
        if (checkRun.status === 'completed' && checkRun.conclusion !== 'success') {
          core.warning(`Check '${checkRun.name}' failed or was not successful (conclusion: ${checkRun.conclusion}).`);
          allChecksPassed = false;
          break;
        }
        // If a check is still in_progress or queued, we cannot determine final success
        if (checkRun.status !== 'completed') {
          core.warning(`Check '${checkRun.name}' is still '${checkRun.status}'. Cannot bless until all checks are completed successfully.`);
          allChecksPassed = false;
          break;
        }
      }
    }

    if (!allChecksPassed) {
      core.info('Not all checks passed successfully. No affirmation posted.');
      return;
    }

    const affirmations = [
      "The void acknowledges your diligence. Well merged, survivor!",
      "Even in the twilight, your code shines bright. A beacon of hope!",
      "The temporal currents are stable. This merge is blessed by the Chrono-Weavers!",
      "A successful integration! The data streams flow smoothly through the fractured reality.",
      "Your contribution ripples positively through the timelines. Excellent work!",
      "Through the cosmic dust, your merge stands strong. A testament to resilience!",
      "The fabric of reality thanks you for this stable merge. Keep up the stellar work!"
    ];

    const affirmationMessage = affirmations[Math.floor(Math.random() * affirmations.length)];

    await octokit.rest.issues.createComment({
      owner,
      repo,
      issue_number: pr.number,
      body: `**ApocalypsAI Blessing:** ${affirmationMessage}`,
    });

    core.setOutput('affirmation-message', affirmationMessage);
    core.info(`Posted affirmation: "${affirmationMessage}"`);

  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
