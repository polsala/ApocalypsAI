const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const staleDays = parseInt(core.getInput('stale-days', { required: true }));
    const token = core.getInput('repo-token', { required: true });
    const octokit = github.getOctokit(token);

    const { owner, repo } = github.context.repo;

    core.info(`Checking for branches older than ${staleDays} days in ${owner}/${repo}...`);

    // Mock rationale: Control current date for deterministic staleness checks in tests.
    const now = new Date();
    const cutoffDate = new Date(now.setDate(now.getDate() - staleDays));

    const branches = await octokit.rest.repos.listBranches({
      owner,
      repo,
      per_page: 100 // Max per page
    });

    let staleBranches = [];
    const protectedBranches = ['main', 'master', 'develop']; // Could be an input for more flexibility

    for (const branch of branches.data) {
      if (protectedBranches.includes(branch.name)) {
        core.info(`Skipping protected branch: ${branch.name}`);
        continue;
      }

      // Get the last commit for the branch
      const { data: commit } = await octokit.rest.repos.getCommit({
        owner,
        repo,
        ref: branch.name,
      });

      const lastCommitDate = new Date(commit.commit.author.date);

      if (lastCommitDate < cutoffDate) {
        core.info(`Found stale branch: ${branch.name} (last commit: ${lastCommitDate.toISOString()})`);
        staleBranches.push({
          name: branch.name,
          lastCommitDate: lastCommitDate,
          author: commit.commit.author.name,
          authorEmail: commit.commit.author.email,
          committerLogin: commit.author ? commit.author.login : 'unknown', // Use commit.author for GitHub login
        });
      }
    }

    core.info(`Found ${staleBranches.length} stale branches.`);

    for (const staleBranch of staleBranches) {
      let notificationMessage = `🤖 **Branch Rot Monitor Alert!** 🤖\n\n`;
      notificationMessage += `The branch \`${staleBranch.name}\` appears to be stale.\n`;
      notificationMessage += `Last commit was on ${staleBranch.lastCommitDate.toDateString()} by ${staleBranch.author}.\n\n`;
      notificationMessage += `Please consider merging it, updating it, or deleting it to keep our repository tidy!\n`;
      notificationMessage += `(This message was brought to you by the ApocalypsAI Nightly Integrator.)`;

      // Try to find an open PR for this branch
      const pulls = await octokit.rest.pulls.list({
        owner,
        repo,
        state: 'open',
        head: `${owner}:${staleBranch.name}`,
      });

      if (pulls.data.length > 0) {
        const pr = pulls.data[0]; // Assume the first one is the relevant one
        core.info(`Commenting on PR #${pr.number} for branch ${staleBranch.name}`);
        await octokit.rest.issues.createComment({
          owner,
          repo,
          issue_number: pr.number,
          body: notificationMessage,
        });
      } else {
        core.info(`Opening an issue for stale branch ${staleBranch.name}`);
        await octokit.rest.issues.create({
          owner,
          repo,
          title: `[Stale Branch Alert] ${staleBranch.name} needs attention!`,
          body: notificationMessage,
          assignees: staleBranch.committerLogin !== 'unknown' ? [staleBranch.committerLogin] : [],
        });
      }
    }

    core.setOutput('stale-branches-count', staleBranches.length);

  } catch (error) {
    core.setFailed(error.message);
  }
}

// Only run if this file is executed directly (not imported as a module)
if (require.main === module) {
  run();
}

module.exports = run; // Export for testing
