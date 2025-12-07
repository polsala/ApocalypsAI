const core = require('@actions/core');
const github = require('@actions/github');

/**
 * Determines if a branch is older than the given number of days.
 * @param {string} dateISO ISO date string of the latest commit on the branch.
 * @param {number} days Threshold in days.
 * @returns {boolean}
 */
function isOlderThan(dateISO, days) {
  const branchDate = new Date(dateISO);
  const now = new Date();
  const diffMs = now - branchDate;
  const diffDays = diffMs / (1000 * 60 * 60 * 24);
  return diffDays > days;
}

/**
 * Main entry point.
 * @param {object} [octokit] Optional octokit instance for testing.
 * @param {object} [context] Optional context for testing.
 */
async function run(octokit, context) {
  try {
    const token = core.getInput('github_token', { required: true });
    const daysToKeep = parseInt(core.getInput('days_to_keep') || '7', 10);
    const gh = octokit || github.getOctokit(token);
    const ctx = context || github.context;
    const { owner, repo } = ctx.repo;
    const defaultBranch = ctx.payload.repository.default_branch;

    // List all branches
    const { data: branches } = await gh.rest.repos.listBranches({ owner, repo, per_page: 100 });

    for (const branch of branches) {
      const branchName = branch.name;
      // Skip default branch
      if (branchName === defaultBranch) continue;

      // Check if branch is merged
      const { data: compare } = await gh.rest.repos.compareCommits({
        owner,
        repo,
        base: branchName,
        head: defaultBranch,
      });

      if (!compare.merged) continue; // Not merged yet

      // Get latest commit date on the branch
      const commitDate = branch.commit.commit.author.date;
      if (isOlderThan(commitDate, daysToKeep)) {
        // Delete the branch (delete the ref)
        await gh.rest.git.deleteRef({ owner, repo, ref: `heads/${branchName}` });
        core.info(`Deleted branch ${branchName}`);
      } else {
        core.info(`Keeping branch ${branchName} (age within threshold)`);
      }
    }
  } catch (error) {
    core.setFailed(error.message);
  }
}

module.exports = { run };

if (require.main === module) {
  // When executed directly by the action runtime
  run();
}
