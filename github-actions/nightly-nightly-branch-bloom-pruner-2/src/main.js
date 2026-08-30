const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const token = core.getInput('github-token', { required: true });
    const staleDays = parseInt(core.getInput('stale-days') || '90', 10);
    const defaultBranchName = core.getInput('default-branch') || 'main';
    const dryRun = core.getInput('dry-run') === 'true';

    const octokit = github.getOctokit(token);
    const { owner, repo } = github.context.repo;

    core.info(`Starting Branch Bloom Pruner for ${owner}/${repo}`);
    core.info(`Configuration: stale-days=${staleDays}, default-branch=${defaultBranchName}, dry-run=${dryRun}`);

    const allBranches = await octokit.paginate(octokit.rest.repos.listBranches, {
      owner,
      repo,
      protected: false, // Only consider non-protected branches for pruning
    });

    const defaultBranch = allBranches.find(b => b.name === defaultBranchName);
    if (!defaultBranch) {
      core.setFailed(`Default branch '${defaultBranchName}' not found.`);
      return;
    }
    const defaultBranchSha = defaultBranch.commit.sha;

    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - staleDays);

    const prunedBranches = [];

    for (const branch of allBranches) {
      if (branch.name === defaultBranchName) {
        core.info(`Skipping default branch: ${branch.name}`);
        continue;
      }
      if (branch.protected) {
        core.info(`Skipping protected branch: ${branch.name}`);
        continue;
      }

      const lastCommit = await octokit.rest.repos.getCommit({
        owner,
        repo,
        ref: branch.commit.sha,
      });
      const commitDate = new Date(lastCommit.data.commit.author.date);

      if (commitDate > cutoffDate) {
        core.info(`Branch '${branch.name}' is not stale (last commit: ${commitDate.toISOString()}).`);
        continue;
      }

      // Check if the branch is merged into the default branch
      // A branch is considered merged if its head commit is an ancestor of the default branch's head commit.
      // compareCommits returns 'behind' if the base (default) contains all commits from the head (branch).
      const comparison = await octokit.rest.repos.compareCommits({
        owner,
        repo,
        base: defaultBranchSha,
        head: branch.commit.sha,
      });

      if (comparison.data.status === 'behind' || comparison.data.status === 'identical') {
        core.info(`Branch '${branch.name}' is stale but already merged into '${defaultBranchName}'. Skipping.`);
        continue;
      }

      core.info(`Branch '${branch.name}' is stale (${commitDate.toISOString()}) and unmerged.`);

      if (dryRun) {
        core.info(`[DRY RUN] Would prune branch: ${branch.name}`);
        prunedBranches.push({ name: branch.name, status: 'would be pruned (dry-run)' });
      } else {
        core.info(`Pruning branch: ${branch.name}`);
        try {
          await octokit.rest.git.deleteRef({
            owner,
            repo,
            ref: `heads/${branch.name}`,
          });
          core.info(`Successfully pruned branch: ${branch.name}`);
          prunedBranches.push({ name: branch.name, status: 'pruned' });
        } catch (deleteError) {
          core.error(`Failed to prune branch '${branch.name}': ${deleteError.message}`);
          prunedBranches.push({ name: branch.name, status: `failed to prune: ${deleteError.message}` });
        }
      }
    }

    core.setOutput('pruned-branches', JSON.stringify(prunedBranches));
    core.info('Branch Bloom Pruner finished.');

  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
