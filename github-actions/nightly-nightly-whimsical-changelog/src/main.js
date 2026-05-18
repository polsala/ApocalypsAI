const core = require('@actions/core');
const github = require('@actions/github');
const fs = require('fs');

async function run() {
  try {
    const commitPrefix = core.getInput('commit-prefix', { required: true });
    const outputFile = core.getInput('output-file', { required: true });
    const maxCommits = parseInt(core.getInput('max-commits', { required: true }), 10);

    const token = core.getInput('github-token', { required: true });
    const octokit = github.getOctokit(token);

    const { owner, repo } = github.context.repo;

    core.info(`Scanning up to ${maxCommits} commits in ${owner}/${repo} for prefix: "${commitPrefix}"`);

    const commitsResponse = await octokit.rest.repos.listCommits({
      owner,
      repo,
      per_page: maxCommits,
    });

    const commits = commitsResponse.data;
    let changelogEntries = [];

    for (const commit of commits) {
      const message = commit.commit.message;
      if (message.startsWith(commitPrefix)) {
        const shortSha = commit.sha.substring(0, 7);
        const entry = `- ${message.substring(commitPrefix.length).trim()} (${shortSha})`;
        changelogEntries.push(entry);
      }
    }

    let changelogContent = '';
    if (changelogEntries.length > 0) {
      changelogContent = `## Whimsical Changelog\n\n${changelogEntries.join('\n')}\n`;
      core.info('Generated Whimsical Changelog:\n' + changelogContent);
    } else {
      changelogContent = '## Whimsical Changelog\n\nNo whimsical changes found in recent commits.\n';
      core.info('No whimsical changes found.');
    }

    // Write to file
    fs.writeFileSync(outputFile, changelogContent);
    core.info(`Changelog written to ${outputFile}`);

    core.setOutput('changelog-content', changelogContent);
    core.setOutput('changelog-path', outputFile);

  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
