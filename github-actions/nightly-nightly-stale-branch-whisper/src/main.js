const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const token = core.getInput('github-token', { required: true });
    const staleDays = parseInt(core.getInput('stale-days') || '30', 10);
    const defaultBranchName = core.getInput('default-branch') || 'main';
    const issueLabel = core.getInput('issue-label') || 'stale-branch';
    const dryRun = core.getInput('dry-run') === 'true';
    const excludeBranchesInput = core.getInput('exclude-branches') || '';
    const excludeBranches = excludeBranchesInput.split(',').map(b => b.trim()).filter(Boolean);

    const octokit = github.getOctokit(token);
    const { owner, repo } = github.context.repo;

    core.info(`Scanning for branches older than ${staleDays} days, excluding: ${excludeBranches.join(', ')}`);

    const allBranches = await octokit.rest.repos.listBranches({
      owner,
      repo,
      per_page: 100 // Max per_page, handle pagination if more than 100 branches
    });

    const staleBranches = [];
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - staleDays);

    for (const branch of allBranches.data) {
      const branchName = branch.name;

      if (branchName === defaultBranchName) {
        core.debug(`Skipping default branch: ${branchName}`);
        continue;
      }

      if (excludeBranches.some(pattern => {
        try {
          return new RegExp(`^${pattern.replace(/\*/g, '.*')}$`).test(branchName);
        } catch (e) {
          core.warning(`Invalid regex pattern "${pattern}" in exclude-branches: ${e.message}`);
          return false;
        }
      })) {
        core.debug(`Skipping excluded branch: ${branchName}`);
        continue;
      }

      core.debug(`Checking branch: ${branchName}`);

      // Get branch details to find last commit date
      const { data: branchDetails } = await octokit.rest.repos.getBranch({
        owner,
        repo,
        branch: branchName,
      });

      const lastCommitDate = new Date(branchDetails.commit.commit.author.date);

      if (lastCommitDate < cutoffDate) {
        core.info(`Branch '${branchName}' is older than ${staleDays} days (last commit: ${lastCommitDate.toISOString()}).`);

        // Check if the branch is merged into the default branch
        const pullRequests = await octokit.rest.pulls.list({
          owner,
          repo,
          state: 'closed', // Look for closed PRs
          head: `${owner}:${branchName}`, // PRs where this branch is the head
          per_page: 100
        });

        const isMerged = pullRequests.data.some(pr => pr.merged_at !== null);

        if (isMerged) {
          core.info(`Branch '${branchName}' has a merged PR, skipping.`);
          continue;
        }

        staleBranches.push(branchName);
      }
    }

    if (staleBranches.length > 0) {
      const message = `The following branches have been identified as stale (older than ${staleDays} days and not merged into \`${defaultBranchName}\`):\n\n${staleBranches.map(b => `- \`${b}\``).join('\n')}\n\nPlease consider reviewing and pruning these branches if they are no longer needed.`;
      const issueTitle = `A Gentle Whisper from the Repository Depths: Stale Branches Detected!`;

      core.info(`Found ${staleBranches.length} stale branches.`);
      core.info(message);

      if (!dryRun) {
        core.info('Creating a new issue...');
        await octokit.rest.issues.create({
          owner,
          repo,
          title: issueTitle,
          body: message,
          labels: [issueLabel],
        });
        core.info('Issue created successfully.');
      } else {
        core.info('Dry run enabled. No issue created.');
      }
    } else {
      core.info('No stale branches found. The repository is spick and span!');
    }

    core.setOutput('stale-branches-count', staleBranches.length);
    core.setOutput('stale-branches-list', JSON.stringify(staleBranches));

  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
