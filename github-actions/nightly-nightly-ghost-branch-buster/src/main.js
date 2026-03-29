const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const token = core.getInput('repo-token', { required: true });
    const staleDays = parseInt(core.getInput('stale-days', { required: true }), 10);
    const exemptBranchesInput = core.getInput('exempt-branches');
    const dryRun = core.getBooleanInput('dry-run');
    const deleteStale = core.getBooleanInput('delete-stale');
    const issueLabel = core.getInput('issue-label');
    const issueTitle = core.getInput('issue-title') || 'Stale Branches Detected';

    const exemptBranches = exemptBranchesInput.split(',').map(b => b.trim()).filter(b => b.length > 0);

    const octokit = github.getOctokit(token);
    const { owner, repo } = github.context.repo;

    core.info(`Scanning for branches older than ${staleDays} days.`);
    core.info(`Exempt branches: ${exemptBranches.join(', ')}`);
    core.info(`Dry run: ${dryRun}`);
    core.info(`Delete stale branches: ${deleteStale}`);

    const allBranches = await octokit.paginate(octokit.rest.repos.listBranches, {
      owner,
      repo,
      per_page: 100
    });

    const now = new Date();
    const staleThreshold = new Date(now.setDate(now.getDate() - staleDays));

    let staleBranches = [];
    let deletedBranchesCount = 0;

    for (const branch of allBranches) {
      if (exemptBranches.includes(branch.name)) {
        core.info(`Skipping exempt branch: ${branch.name}`);
        continue;
      }

      // Get the last commit for the branch
      const { data: commit } = await octokit.rest.repos.getCommit({
        owner,
        repo,
        ref: branch.name
      });

      const lastCommitDate = new Date(commit.commit.author.date);

      if (lastCommitDate < staleThreshold) {
        staleBranches.push(branch.name);
        core.info(`Found stale branch: ${branch.name} (last commit: ${lastCommitDate.toISOString()})`);

        if (!dryRun && deleteStale) {
          try {
            await octokit.rest.git.deleteRef({
              owner,
              repo,
              ref: `heads/${branch.name}`
            });
            core.info(`Successfully deleted stale branch: ${branch.name}`);
            deletedBranchesCount++;
          } catch (error) {
            core.error(`Failed to delete branch ${branch.name}: ${error.message}`);
          }
        }
      }
    }

    core.setOutput('stale-branches-count', staleBranches.length);
    core.setOutput('deleted-branches-count', deletedBranchesCount);
    core.setOutput('stale-branches-list', JSON.stringify(staleBranches));

    if (staleBranches.length > 0) {
      let issueBody = `The following branches have not been updated in ${staleDays} days:\n\n`;
      staleBranches.forEach(b => issueBody += `- \`${b}\`\n`);
      issueBody += `\n${dryRun ? 'This was a dry run. No branches were deleted.' : (deleteStale ? 'Stale branches were deleted.' : 'No branches were deleted (delete-stale was false).')}`;

      core.info(issueBody);

      if (issueLabel || issueTitle) {
        try {
          const { data: issue } = await octokit.rest.issues.create({
            owner,
            repo,
            title: issueTitle,
            body: issueBody,
            labels: issueLabel ? [issueLabel] : []
          });
          core.info(`Created issue #${issue.number} for stale branches.`);
        } catch (error) {
          core.error(`Failed to create issue: ${error.message}`);
        }
      }
    } else {
      core.info('No stale branches found. Repository is clean!');
    }

  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
