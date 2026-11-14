const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const token = core.getInput('github-token', { required: true });
    const chronicleFile = core.getInput('chronicle-file');
    const entryFormat = core.getInput('entry-format');
    const commitMessageFormat = core.getInput('commit-message');

    const { owner, repo } = github.context.repo;
    const pullRequest = github.context.payload.pull_request;

    if (!pullRequest || !pullRequest.merged) {
      core.info('Skipping: Not a merged pull request event.');
      return;
    }

    const prTitle = pullRequest.title;
    const prNumber = pullRequest.number;
    const prAuthor = pullRequest.user.login;
    const mergeDate = new Date(pullRequest.merged_at).toLocaleDateString('en-US', {
      year: 'numeric', month: 'long', day: 'numeric'
    });

    const newEntry = entryFormat
      .replace(/{PR_TITLE}/g, prTitle)
      .replace(/{PR_NUMBER}/g, prNumber)
      .replace(/{PR_AUTHOR}/g, prAuthor)
      .replace(/{MERGE_DATE}/g, mergeDate);

    const octokit = github.getOctokit(token);

    let existingContent = '';
    let sha = null;

    try {
      const { data } = await octokit.rest.repos.getContent({
        owner,
        repo,
        path: chronicleFile,
        ref: github.context.ref // Use the branch the PR merged into
      });
      existingContent = Buffer.from(data.content, 'base64').toString('utf8');
      sha = data.sha;
    } catch (error) {
      if (error.status === 404) {
        core.info(`Chronicle file '${chronicleFile}' not found. Creating a new one.`);
      } else {
        throw error;
      }
    }

    const updatedContent = existingContent ? `${existingContent}\n${newEntry}` : `${newEntry}`;
    const commitMessage = commitMessageFormat.replace(/{PR_NUMBER}/g, prNumber);

    await octokit.rest.repos.createOrUpdateFileContents({
      owner,
      repo,
      path: chronicleFile,
      message: commitMessage,
      content: Buffer.from(updatedContent).toString('base64'),
      sha: sha, // Required if updating an existing file
      branch: github.context.ref // Commit to the branch the PR merged into
    });

    core.setOutput('chronicle-entry', newEntry);
    core.info(`Successfully updated chronicle file '${chronicleFile}' with entry:\n${newEntry}`);

  } catch (error) {
    core.setFailed(error.message);
  }
}

module.exports = { run };
