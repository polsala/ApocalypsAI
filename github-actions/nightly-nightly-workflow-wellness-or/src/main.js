const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const token = core.getInput('github-token', { required: true });
    const daysToCheck = parseInt(core.getInput('days-to-check') || '7', 10);

    if (isNaN(daysToCheck) || daysToCheck <= 0) {
      core.setFailed('days-to-check must be a positive number.');
      return;
    }

    const octokit = github.getOctokit(token);
    const { owner, repo } = github.context.repo;

    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - daysToCheck);

    let allRuns = [];
    let page = 1;
    let hasMore = true;

    // Fetch workflow runs, paginating if necessary
    while (hasMore) {
      const response = await octokit.rest.actions.listWorkflowRunsForRepo({
        owner,
        repo,
        per_page: 100, // Max per page
        page,
        created: `>=${cutoffDate.toISOString()}`, // Filter by creation date
      });

      allRuns = allRuns.concat(response.data.workflow_runs);
      if (response.data.workflow_runs.length < 100) {
        hasMore = false;
      } else {
        page++;
      }
    }

    const relevantRuns = allRuns.filter(run => new Date(run.created_at) >= cutoffDate);

    if (relevantRuns.length === 0) {
      core.setOutput('wellness-report', `The Workflow Oracle finds no recent runs in the last ${daysToCheck} days. The digital winds are calm, or perhaps too calm... 💨`);
      return;
    }

    const totalRuns = relevantRuns.length;
    const successfulRuns = relevantRuns.filter(run => run.conclusion === 'success').length;
    const failedRuns = relevantRuns.filter(run => run.conclusion === 'failure').length;
    const cancelledRuns = relevantRuns.filter(run => run.conclusion === 'cancelled').length;
    const pendingRuns = relevantRuns.filter(run => ['queued', 'in_progress', 'waiting'].includes(run.status)).length;

    let totalDurationMs = 0;
    relevantRuns.forEach(run => {
      if (run.created_at && run.updated_at) {
        totalDurationMs += new Date(run.updated_at).getTime() - new Date(run.created_at).getTime();
      }
    });
    const averageDurationSeconds = totalRuns > 0 ? Math.round((totalDurationMs / totalRuns) / 1000) : 0;

    let report = '';

    if (failedRuns === 0 && pendingRuns === 0) {
      report = `The Workflow Forest is flourishing! 🌳 All ${totalRuns} recent runs (last ${daysToCheck} days) completed successfully. The average run took ${averageDurationSeconds} seconds. A truly harmonious digital ecosystem!`;
    } else if (failedRuns > 0 && successfulRuns === 0) {
      report = `A storm brews in the Workflow Peaks! ⛈️ All ${totalRuns} recent runs (last ${daysToCheck} days) have failed. Immediate attention is required to calm these digital tempests!`;
    } else if (failedRuns > 0) {
      const successRate = ((successfulRuns / totalRuns) * 100).toFixed(1);
      report = `The Workflow River flows, but with some rapids! 🌊 Out of ${totalRuns} recent runs (last ${daysToCheck} days), ${successfulRuns} succeeded and ${failedRuns} encountered obstacles. Success rate: ${successRate}%. Let's navigate these waters carefully.`;
    } else if (pendingRuns > 0) {
      report = `The Workflow Loom is busy weaving! 🧵 ${pendingRuns} runs are currently in progress or queued. The digital threads are being spun with great diligence.`;
    } else if (cancelledRuns > 0) {
      report = `The Workflow Compass points to new directions! 🧭 ${cancelledRuns} runs were cancelled. Perhaps a change of course was needed.`;
    } else {
      report = `The Workflow Oracle observes ${totalRuns} runs (last ${daysToCheck} days) with various outcomes. The digital tapestry is rich with activity!`;
    }

    core.setOutput('wellness-report', report);

  } catch (error) {
    core.setFailed(error.message);
  }
}

module.exports = run;
