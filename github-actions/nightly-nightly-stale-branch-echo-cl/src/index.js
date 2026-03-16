const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const staleDays = parseInt(core.getInput('stale_days'), 10);
    const dryRun = core.getBooleanInput('dry_run');
    const excludeBranches = core.getInput('exclude_branches').split(',').map(b => b.trim()).filter(b => b.length > 0);
    const actionType = core.getInput('action_type'); // 'log', 'delete', 'issue'
    const issueLabels = core.getInput('issue_labels').split(',').map(l => l.trim()).filter(l => l.length > 0);
    const githubToken = core.getInput('github_token');

    const octokit = github.getOctokit(githubToken);
    const { owner, repo } = github.context.repo;

    core.info(`Starting stale branch echo cleaner with settings:`);
    core.info(`  Stale days: ${staleDays}`);
    core.info(`  Dry run: ${dryRun}`);
    core.info(`  Exclude branches: ${excludeBranches.join(', ')}`);
    core.info(`  Action type: ${actionType}`);

    const now = new Date();
    const staleBranches = [];
    let branchesProcessed = 0;

    // Fetch all branches
    const { data: branches } = await octokit.rest.repos.listBranches({
      owner,
      repo,
      per_page: 100 // Adjust as needed for large repos
    });

    for (const branch of branches) {
      branchesProcessed++;
      if (excludeBranches.includes(branch.name) || excludeBranches.some(pattern => pattern.endsWith('/*') && branch.name.startsWith(pattern.slice(0, -1)))) {
        core.info(`Skipping excluded branch: ${branch.name}`);
        continue;
      }

      // Get the last commit for the branch
      const { data: commit } = await octokit.rest.repos.getCommit({
        owner,
        repo,
        ref: branch.commit.sha
      });

      const lastCommitDate = new Date(commit.commit.author.date);
      const daysOld = Math.floor((now - lastCommitDate) / (1000 * 60 * 60 * 24));

      if (daysOld >= staleDays) {
        staleBranches.push(branch.name);
        core.info(`Found stale branch: ${branch.name} (last commit ${daysOld} days ago)`);

        if (!dryRun) {
          switch (actionType) {
            case 'delete':
              core.info(`  Deleting branch: ${branch.name}`);
              await octokit.rest.git.deleteRef({
                owner,
                repo,
                ref: `heads/${branch.name}`
              });
              core.info(`  Branch ${branch.name} deleted.`);
              break;
            case 'issue':
              core.info(`  Creating issue for branch: ${branch.name}`);
              await octokit.rest.issues.create({
                owner,
                repo,
                title: `Stale Branch Detected: ${branch.name}`,
                body: `The branch \`${branch.name}\` has not been updated in ${daysOld} days. Consider reviewing or deleting it.`,
                labels: issueLabels
              });
              core.info(`  Issue created for branch ${branch.name}.`);
              break;
            case 'log':
            default:
              core.info(`  Action type 'log' selected. No action taken for ${branch.name}.`);
              break;
          }
        } else {
          core.info(`  Dry run enabled. Would have performed action '${actionType}' for branch ${branch.name}.`);
        }
      } else {
        core.debug(`Branch ${branch.name} is not stale (${daysOld} days old).`);
      }
    }

    core.setOutput('stale_branches_found', JSON.stringify(staleBranches));
    core.setOutput('branches_processed', branchesProcessed);
    core.info(`Stale branch echo cleaner finished. Found ${staleBranches.length} stale branches.`);

  } catch (error) {
    core.setFailed(error.message);
  }
}

// Export for testing, and run directly when executed as a script
if (require.main === module) {
  run();
}
module.exports = { run };
