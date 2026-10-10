const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const token = core.getInput('github_token', { required: true });
    const thresholdMultiplier = parseFloat(core.getInput('threshold_multiplier') || '2.0');
    const minDurationSeconds = parseInt(core.getInput('min_duration_seconds') || '5', 10);

    const octokit = github.getOctokit(token);
    const { owner, repo } = github.context.repo;
    const runId = github.context.runId;

    core.info(`Scanning workflow run ${runId} for temporal distortions...`);

    const anomalies = [];

    // Fetch workflow jobs for the current run
    // # Mock rationale: In tests, this API call is mocked to provide controlled job and step data.
    const { data: { jobs } } = await octokit.rest.actions.listJobsForWorkflowRun({
      owner,
      repo,
      run_id: runId,
    });

    for (const job of jobs) {
      core.debug(`Processing job: ${job.name} (ID: ${job.id})`);
      const stepDurations = [];
      const stepsWithDuration = [];

      for (const step of job.steps) {
        if (step.status === 'completed' && step.started_at && step.completed_at) {
          const startTime = new Date(step.started_at);
          const endTime = new Date(step.completed_at);
          const durationSeconds = (endTime.getTime() - startTime.getTime()) / 1000;

          if (durationSeconds >= minDurationSeconds) {
            stepDurations.push(durationSeconds);
            stepsWithDuration.push({ name: step.name, duration: durationSeconds });
          }
        }
      }

      if (stepDurations.length > 1) { // Need at least two steps to compare against an average
        const averageDuration = stepDurations.reduce((sum, d) => sum + d, 0) / stepDurations.length;
        core.debug(`Job "${job.name}" average step duration: ${averageDuration.toFixed(2)}s`);

        for (const step of stepsWithDuration) {
          if (step.duration > averageDuration * thresholdMultiplier) {
            const anomaly = {
              job_name: job.name,
              step_name: step.name,
              duration_seconds: step.duration,
              average_job_duration_seconds: averageDuration,
              threshold_multiplier: thresholdMultiplier,
              message: `Step "${step.name}" took ${step.duration.toFixed(2)}s, which is ${(step.duration / averageDuration).toFixed(1)}x the average step duration (${averageDuration.toFixed(2)}s) in job "${job.name}". A chronal anomaly!`
            };
            anomalies.push(anomaly);
            core.warning(anomaly.message);
          }
        }
      } else if (stepDurations.length === 1) {
        core.info(`Job "${job.name}" has only one significant step. No average to compare against.`);
      } else {
        core.info(`Job "${job.name}" has no significant completed steps to analyze.`);
      }
    }

    if (anomalies.length > 0) {
      core.setOutput('anomalies_detected', true);
      core.setOutput('anomaly_report', JSON.stringify(anomalies, null, 2));
      core.setFailed('Temporal distortions detected in workflow steps! Check the anomaly report.');
    } else {
      core.setOutput('anomalies_detected', false);
      core.setOutput('anomaly_report', '[]');
      core.info('All workflow steps appear to be within expected temporal parameters. No distortions detected!');
    }

  } catch (error) {
    core.setFailed(`Chrono-Sentry malfunction: ${error.message}`);
  }
}

if (require.main === module) {
  run();
}

module.exports = run; // Export for testing
