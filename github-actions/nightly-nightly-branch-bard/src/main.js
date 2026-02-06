const core = require('@actions/core');
const github = require('@actions/github');
const { minimatch } = require('minimatch'); // For glob matching

async function run() {
  try {
    const token = core.getInput('repo-token', { required: true });
    const staleDays = parseInt(core.getInput('stale-days') || '60', 10);
    const ignoreBranchesInput = core.getInput('ignore-branches') || 'main,master,develop';
    const outputType = core.getInput('output-type') || 'summary';
    const issueNumber = core.getInput('issue-number');

    if (outputType === 'issue-comment' && !issueNumber) {
      core.setFailed('issue-number is required when output-type is "issue-comment".');
      return;
    }

    const octokit = github.getOctokit(token);
    const { owner, repo } = github.context.repo;

    const ignorePatterns = ignoreBranchesInput.split(',').map(s => s.trim()).filter(Boolean);

    core.info(`Checking for branches older than ${staleDays} days, ignoring: ${ignorePatterns.join(', ')}`);

    const branches = await octokit.paginate(octokit.rest.repos.listBranches, {
      owner,
      repo,
      per_page: 100,
    });

    const now = new Date();
    const staleThreshold = new Date(now.setDate(now.getDate() - staleDays));

    const staleBranches = [];

    for (const branch of branches) {
      const isIgnored = ignorePatterns.some(pattern => minimatch(branch.name, pattern));
      if (isIgnored) {
        core.info(`Ignoring branch: ${branch.name}`);
        continue;
      }

      // Get the last commit for the branch
      const { data: commit } = await octokit.rest.repos.getCommit({
        owner,
        repo,
        ref: branch.commit.sha,
      });

      const lastCommitDate = new Date(commit.commit.author.date);

      if (lastCommitDate < staleThreshold) {
        const suggestion = generateWhimsicalSuggestion(branch.name);
        staleBranches.push({
          name: branch.name,
          lastCommitDate: lastCommitDate.toISOString(),
          suggestion: suggestion,
        });
        core.info(`Stale branch found: ${branch.name} (last commit: ${lastCommitDate.toDateString()}) - Suggestion: ${suggestion}`);
      }
    }

    let outputMessage = '';
    if (staleBranches.length > 0) {
      outputMessage += `### 📜 Nightly Branch Bard's Archival Suggestions 📜\n\n`;
      outputMessage += `The following branches have been inactive for ${staleDays} days or more and might be ready for archival or deletion:\n\n`;
      staleBranches.forEach(b => {
        outputMessage += `- \`${b.name}\` (Last commit: ${new Date(b.lastCommitDate).toLocaleDateString()}): _${b.suggestion}_\n`;
      });
      outputMessage += `\nConsider tidying up your repository!`;
    } else {
      outputMessage += `### ✨ Repository Tidy! ✨\n\n`;
      outputMessage += `No stale branches found. Your repository is as clean as a freshly swept vault!`;
    }

    core.setOutput('stale-branches-json', JSON.stringify(staleBranches));
    core.setOutput('summary-output', outputMessage);

    if (outputType === 'summary') {
      core.summary.addRaw(outputMessage);
    } else if (outputType === 'issue-comment') {
      await octokit.rest.issues.createComment({
        owner,
        repo,
        issue_number: issueNumber,
        body: outputMessage,
      });
    }

  } catch (error) {
    core.setFailed(error.message);
  }
}

function generateWhimsicalSuggestion(branchName) {
  const themes = [
    "The Forgotten Scroll of", "The Dusty Tome of", "The Whispering Willow Branch of",
    "The Echoing Chamber of", "The Lost Blueprint for", "The Ancient Map to",
    "The Faded Chronicle of", "The Slumbering Seed of", "The Unfinished Symphony of"
  ];
  const actions = [
    "awaiting rediscovery.", "ready for its final rest.", "to be cataloged in the archives.",
    "a relic of a bygone era.", "whispering tales of old.", "ready for the great beyond.",
    "a memory in the digital ether.", "to be swept away by the winds of change."
  ];

  const randomTheme = themes[Math.floor(Math.random() * themes.length)];
  const randomAction = actions[Math.floor(Math.random() * actions.length)];

  return `${randomTheme} \`${branchName}\`, ${randomAction}`;
}

if (require.main === module) {
  run();
}

module.exports = { run, generateWhimsicalSuggestion };
