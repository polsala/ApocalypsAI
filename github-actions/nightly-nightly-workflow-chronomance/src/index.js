const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const workflowId = core.getInput('workflow_id', { required: true });
    const repoToken = core.getInput('repo_token');
    const thresholdPercent = parseFloat(core.getInput('threshold_percent') || '15');
    const numRunsForAverage = parseInt(core.getInput('num_runs_for_average') || '10', 10);

    if (isNaN(thresholdPercent) || thresholdPercent < 0) {
      core.setFailed('Input "threshold_percent" must be a non-negative number.');
      return;
    }
    if (isNaN(numRunsForAverage) || numRunsForAverage <= 0) {
      core.setFailed('Input "num_runs_for_average" must be a positive integer.');
      return;
    }

    const octokit = github.getOctokit(repoToken);
    const { owner, repo } = github.context.repo;

    core.info(`Monitoring workflow: ${workflowId} in ${owner}/${repo}`);

    // Fetch workflow runs
    const { data: { workflow_runs: allRuns } } = await octokit.rest.actions.listWorkflowRunsForRepo({
      owner,
      repo,
      workflow_id: workflowId,
      status: 'success', // Only consider successful runs for average
      per_page: numRunsForAverage + 1, // Fetch one more than needed to ensure we have a 'latest' and enough for average
    });

    if (!allRuns || allRuns.length === 0) {
      core.warning(`No successful runs found for workflow ID/name: ${workflowId}. Cannot determine temporal mood.`);
      core.setOutput('status', 'unknown');
      core.setOutput('duration_change_percent', '0.00');
      core.setOutput('latest_duration_seconds', '0.00');
      core.setOutput('average_duration_seconds', '0.00');
      return;
    }

    // The latest run is the first one in the list (most recent)
    const latestRun = allRuns[0];
    if (!latestRun) {
      core.warning('Could not find the latest successful run.');
      core.setOutput('status', 'unknown');
      core.setOutput('duration_change_percent', '0.00');
      core.setOutput('latest_duration_seconds', '0.00');
      core.setOutput('average_duration_seconds', '0.00');
      return;
    }

    const latestRunDurationMs = new Date(latestRun.updated_at).getTime() - new Date(latestRun.created_at).getTime();
    const latestRunDurationSeconds = latestRunDurationMs / 1000;

    // Calculate average from previous successful runs (excluding the latest one if it's part of the average pool)
    const runsForAverage = allRuns.slice(1, numRunsForAverage + 1); // Take up to numRunsForAverage *previous* runs

    if (runsForAverage.length === 0) {
      core.warning(`Not enough previous successful runs (${numRunsForAverage} required) found for workflow ID/name: ${workflowId} to calculate a meaningful average. Reporting latest run duration only.`);
      core.setOutput('status', 'unknown');
      core.setOutput('duration_change_percent', '0.00');
      core.setOutput('latest_duration_seconds', latestRunDurationSeconds.toFixed(2));
      core.setOutput('average_duration_seconds', '0.00');
      return;
    }

    const totalDurationMs = runsForAverage.reduce((sum, run) => {
      const duration = new Date(run.updated_at).getTime() - new Date(run.created_at).getTime();
      return sum + duration;
    }, 0);

    const averageDurationMs = totalDurationMs / runsForAverage.length;
    const averageDurationSeconds = averageDurationMs / 1000;

    let status = 'steady';
    let durationChangePercent = 0;

    if (averageDurationMs > 0) {
      durationChangePercent = ((latestRunDurationMs - averageDurationMs) / averageDurationMs) * 100;

      if (durationChangePercent > thresholdPercent) {
        status = 'sluggish';
        core.info(`🚨 Workflow ${workflowId} is feeling sluggish! It ran ${durationChangePercent.toFixed(2)}% slower than average.`);
      } else if (durationChangePercent < -thresholdPercent) {
        status = 'zippy';
        core.info(`⚡ Workflow ${workflowId} is feeling zippy! It ran ${Math.abs(durationChangePercent).toFixed(2)}% faster than average.`);
      } else {
        core.info(`😌 Workflow ${workflowId} is feeling steady. It ran within ${thresholdPercent}% of its average duration.`);
      }
    } else {
      core.info(`Cannot calculate duration change as average duration is zero. Latest run duration: ${latestRunDurationSeconds.toFixed(2)}s.`);
    }

    core.setOutput('status', status);
    core.setOutput('duration_change_percent', durationChangePercent.toFixed(2));
    core.setOutput('latest_duration_seconds', latestRunDurationSeconds.toFixed(2));
    core.setOutput('average_duration_seconds', averageDurationSeconds.toFixed(2));

  } catch (error) {
    core.setFailed(error.message);
  }
}

if (require.main === module) {
  run();
}

module.exports = {
  run,
};
