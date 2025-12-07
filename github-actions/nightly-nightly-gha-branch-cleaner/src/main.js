// Nightly GitHub Actions Branch Cleaner
// Main implementation script

const core = require('@actions/core');
const { github } = require('@actions/github');
const { glob } = require('@actions/toolkit');

async function run() {
  try {
    // Get inputs
    const token = core.getInput('github-token', { required: true });
    const protectedBranches = core.getInput('protected-branches', { required: false }) || 'main,master';
    const retentionDays = parseInt(core.getInput('retention-days', { required: false }) || '0', 10);
    const maxBranchesToDelete = parseInt(core.getInput('max-branches-to-delete', { required: false }) || '100', 10);
    const dryRun = core.getBooleanInput('dry-run', { required: false }) || true;
    const verbose = core.getBooleanInput('verbose', { required: false }) || false;

    // Parse protected branches
    const protectedPatterns = protectedBranches.split(',').map(s => s.trim()).filter(Boolean);

    // Initialize GitHub client
    const octokit = github.getOctokit(token);

    // Helper functions
    function log(message) {
      if (verbose) {
        console.log(message);
      }
    }

    function isBranchProtected(branchName, protectedPatterns) {
      return protectedPatterns.some(pattern => {
        const regex = glob.makeRegex(pattern);
        return regex.test(branchName);
      });
    }

    function isBranchExpired(branch, retentionDays) {
      if (retentionDays <= 0) return false;

      // Try to get last commit date from branch protection or commit data
      const lastCommitDate = new Date(branch.commit?.lastCommitDate || branch.commit?.commitDate || branch.commit?.date || Date.now());
      const cutoffDate = new Date();
      cutoffDate.setDate(cutoffDate.getDate() - retentionDays);

      return lastCommitDate < cutoffDate;
    }

    // Get all branches
    log('Fetching all branches...');
    const branches = await octokit.rest.repos.listBranches({
      owner: github.context.repo.owner,
      repo: github.context.repo.repo,
      per_page: 100
    });

    log(`Found ${branches.data.length} branches`);

    // Filter branches to delete
    const branchesToDelete = [];
    const protectedBranchesList = [];

    for (const branch of branches.data) {
      // Skip if branch is protected
      if (isBranchProtected(branch.name, protectedPatterns)) {
        protectedBranchesList.push(branch.name);
        log(`Skipping protected branch: ${branch.name}`);
        continue;
      }

      // Skip if branch is expired
      if (isBranchExpired(branch, retentionDays)) {
        branchesToDelete.push(branch.name);
        log(`Branch marked for deletion: ${branch.name} (expired)`);
      }
    }

    log(`Found ${branchesToDelete.length} branches to delete`);

    // Limit number of branches to delete
    const branchesToDeleteLimited = branchesToDelete.slice(0, maxBranchesToDelete);

    // Perform deletions
    let deletedCount = 0;
    const deletedBranches = [];

    for (const branchName of branchesToDeleteLimited) {
      try {
        if (dryRun) {
          log(`[DRY RUN] Would delete branch: ${branchName}`);
          deletedBranches.push(branchName);
          deletedCount++;
        } else {
          await octokit.rest.git.deleteRef({
            owner: github.context.repo.owner,
            repo: github.context.repo.repo,
            ref: `heads/${branchName}`
          });
          log(`Deleted branch: ${branchName}`);
          deletedBranches.push(branchName);
          deletedCount++;
        }
      } catch (error) {
        log(`Failed to delete branch ${branchName}: ${error.message}`);
      }
    }

    // Set outputs
    core.setOutput('deleted-branches', JSON.stringify(deletedBranches));
    core.setOutput('protected-branches', JSON.stringify(protectedBranchesList));
    core.setOutput('total-deleted', deletedCount.toString());

    // Summary
    const action = dryRun ? 'would delete' : 'deleted';
    console.log(`\n=== Summary ===`);
    console.log(`${action} ${deletedCount} branches`);
    console.log(`Protected ${protectedBranchesList.length} branches`);

    if (deletedBranches.length > 0) {
      console.log(`\nDeleted branches:`);
      deletedBranches.forEach(branch => console.log(`  - ${branch}`));
    }

    if (protectedBranchesList.length > 0) {
      console.log(`\nProtected branches:`);
      protectedBranchesList.forEach(branch => console.log(`  - ${branch}`));
    }

  } catch (error) {
    core.setFailed(`Action failed: ${error.message}`);
  }
}

run();
