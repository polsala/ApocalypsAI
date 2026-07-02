const core = require('@actions/core');
const github = require('@actions/github');
const { minimatch } = require('minimatch');

async function run() {
  try {
    const staleDays = parseInt(core.getInput('stale-days') || '90', 10);
    const protectedBranchesInput = core.getInput('protected-branches') || 'main,master,develop';
    const repoToken = core.getInput('repo-token', { required: true });

    const protectedBranchPatterns = protectedBranchesInput.split(',').map(p => p.trim()).filter(p => p.length > 0);

    const octokit = github.getOctokit(repoToken);
    const { owner, repo } = github.context.repo;

    core.info(`Checking for branches older than ${staleDays} days in ${owner}/${repo}...`);

    const branches = await octokit.rest.repos.listBranches({
      owner,
      repo,
      per_page: 100 // Max per_page, handle pagination if needed for very large repos
    });

    const now = new Date();
    const staleThreshold = new Date(now.setDate(now.getDate() - staleDays));

    const staleBranches = [];

    for (const branch of branches.data) {
      const branchName = branch.name;

      // Check if branch is protected by pattern matching
      const isProtected = protectedBranchPatterns.some(pattern => minimatch(branchName, pattern));
      if (isProtected) {
        core.info(`Skipping protected branch: ${branchName}`);
        continue;
      }

      // Get the last commit for the branch
      const { data: commit } = await octokit.rest.git.getCommit({
        owner,
        repo,
        commit_sha: branch.commit.sha
      });

      const lastCommitDate = new Date(commit.author.date);

      if (lastCommitDate < staleThreshold) {
        staleBranches.push({
          name: branchName,
          lastCommit: lastCommitDate.toISOString()
        });
        core.info(`Found stale branch: ${branchName} (last commit: ${lastCommitDate.toDateString()})`);
      } else {
        core.debug(`Branch ${branchName} is fresh (last commit: ${lastCommitDate.toDateString()})`);
      }
    }

    const staleBranchesCount = staleBranches.length;
    const staleBranchesJson = JSON.stringify(staleBranches.map(b => b.name));

    let message;
    if (staleBranchesCount > 0) {
      const branchList = staleBranches.map(b => `- ${b.name} (last commit: ${new Date(b.lastCommit).toLocaleDateString()})`).join('\n');
      message = `Oh dear! The Nightly Branch Archivist has unearthed ${staleBranchesCount} branches that seem to have overstayed their welcome. It might be time for a 'Branch Retirement Party'!\n\nHere's the guest list:\n${branchList}\n\nConsider archiving or deleting these branches to keep our digital garden tidy.`;
    } else {
      message = "Hooray! All branches are sparkling clean and actively maintained. No retirement parties needed today!";
    }

    core.setOutput('stale-branches-json', staleBranchesJson);
    core.setOutput('stale-branches-count', staleBranchesCount);
    core.setOutput('stale-branches-message', message);

    core.info(message);

  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
