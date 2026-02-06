const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const token = core.getInput('repo-token', { required: true });
    const staleDays = parseInt(core.getInput('stale-days') || '90', 10);
    const ignoreBranchesInput = core.getInput('ignore-branches') || 'main,master';
    const ignoreBranches = ignoreBranchesInput.split(',').map(b => b.trim()).filter(b => b.length > 0);

    const octokit = github.getOctokit(token);
    const { owner, repo } = github.context.repo;

    core.info(`Scanning for branches older than ${staleDays} days, ignoring: ${ignoreBranches.join(', ')}`);

    const allBranches = await octokit.paginate(octokit.rest.repos.listBranches, {
      owner,
      repo,
      per_page: 100
    });

    const now = new Date();
    const staleBranches = [];

    const whimsicalSuggestions = [
      "Offer it to the Code Goblins for recycling!",
      "Reanimate it with a fresh commit, if it still breathes!",
      "Archive it to the Digital Dustbin, where old code sleeps!",
      "Perform a ritual merge, if its spirit still aligns!",
      "Let it drift into the Void of Unmaintained Features!"
    ];

    let suggestionIndex = 0;

    for (const branch of allBranches) {
      if (ignoreBranches.includes(branch.name)) {
        core.debug(`Ignoring branch: ${branch.name}`);
        continue;
      }

      try {
        const { data: commit } = await octokit.rest.repos.getCommit({
          owner,
          repo,
          ref: branch.commit.sha,
        });

        const lastCommitDate = new Date(commit.commit.author.date);
        const diffTime = Math.abs(now - lastCommitDate);
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

        if (diffDays > staleDays) {
          const suggestion = whimsicalSuggestions[suggestionIndex % whimsicalSuggestions.length];
          staleBranches.push({
            branchName: branch.name,
            lastCommitDate: lastCommitDate.toISOString().split('T')[0], // YYYY-MM-DD
            ageDays: diffDays,
            whimsicalSuggestion: suggestion
          });
          suggestionIndex++;
          core.info(`Stale branch found: ${branch.name} (last commit: ${lastCommitDate.toISOString().split('T')[0]}, ${diffDays} days old) - ${suggestion}`);
        } else {
          core.debug(`Branch ${branch.name} is fresh enough (${diffDays} days old).`);
        }
      } catch (error) {
        core.warning(`Could not get commit details for branch ${branch.name}: ${error.message}`);
      }
    }

    core.setOutput('stale-branches-count', staleBranches.length);
    core.setOutput('stale-branches-report', JSON.stringify(staleBranches, null, 2));

    if (staleBranches.length > 0) {
      core.info(`\n👻 Branch Graveyard Report 👻`);
      core.info(JSON.stringify(staleBranches, null, 2));
    } else {
      core.info('🎉 No stale branches found! Your repository is spick and span!');
    }

  } catch (error) {
    core.setFailed(`Action failed with error: ${error.message}`);
  }
}

run();
