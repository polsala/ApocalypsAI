const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const token = core.getInput('token', { required: true });
    const retentionDays = parseInt(core.getInput('retention-days') || '30', 10); // Default to 30 days

    if (isNaN(retentionDays) || retentionDays <= 0) {
      core.setFailed('retention-days must be a positive integer.');
      return;
    }

    const octokit = github.getOctokit(token);
    const owner = github.context.repo.owner;
    const repo = github.context.repo.repo;

    core.info(`Collecting dust bunnies (workflow runs older than ${retentionDays} days) for ${owner}/${repo}...`);

    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - retentionDays);

    let page = 1;
    let totalDeleted = 0;
    let hasMorePages = true;

    while (hasMorePages) {
      const { data: { workflow_runs: runs } } = await octokit.rest.actions.listWorkflowRunsForRepo({
        owner,
        repo,
        per_page: 100, // Max per page
        page,
      });

      if (runs.length === 0) {
        hasMorePages = false;
        break;
      }

      const runsToDelete = runs.filter(run => {
        const runDate = new Date(run.created_at);
        return runDate < cutoffDate;
      });

      for (const run of runsToDelete) {
        try {
          await octokit.rest.actions.deleteWorkflowRun({
            owner,
            repo,
            run_id: run.id,
          });
          core.info(`Deleted workflow run: ID ${run.id}, Name: "${run.name}", Created: ${run.created_at}`);
          totalDeleted++;
        } catch (deleteError) {
          core.warning(`Failed to delete workflow run ID ${run.id}: ${deleteError.message}`);
        }
      }

      if (runs.length < 100) { // If less than max per page, it's the last page
        hasMorePages = false;
      } else {
        page++;
      }
    }

    core.info(`Successfully swept away ${totalDeleted} dust bunnies.`);

  } catch (error) {
    core.setFailed(error.message);
  }
}

module.exports = {
  run
};

if (require.main === module) {
  run();
}
