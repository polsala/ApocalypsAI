const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const whimsyKeywordsInput = core.getInput('whimsy-keywords', { required: true });
    const targetType = core.getInput('target-type', { required: false }) || 'pr_title';
    const githubToken = core.getInput('github-token') || process.env.GITHUB_TOKEN;

    const keywords = whimsyKeywordsInput.split(',').map(k => k.trim().toLowerCase()).filter(k => k.length > 0);

    if (keywords.length === 0) {
      core.warning('No whimsy keywords provided. This action will always pass.');
      core.setOutput('whimsy-detected', true);
      return;
    }

    let contentToCheck = '';
    if (targetType === 'pr_title') {
      if (github.context.eventName === 'pull_request' && github.context.payload.pull_request) {
        contentToCheck = github.context.payload.pull_request.title;
      } else {
        core.warning('Action triggered outside of a pull_request event, but target-type is "pr_title". Skipping check.');
        core.setOutput('whimsy-detected', true); // Pass by default if context is wrong
        return;
      }
    } else if (targetType === 'commit_message') {
      if (github.context.eventName === 'push' && github.context.payload.head_commit) {
        contentToCheck = github.context.payload.head_commit.message;
      } else if (github.context.eventName === 'pull_request' && github.context.payload.pull_request && github.context.payload.pull_request.head.sha) {
        // For PRs, get the latest commit message on the head branch
        if (!githubToken) {
          core.setFailed('GITHUB_TOKEN is required to fetch commit messages for PRs when target-type is "commit_message".');
          return;
        }
        const octokit = github.getOctokit(githubToken);
        const { owner, repo } = github.context.repo;
        const commitSha = github.context.payload.pull_request.head.sha;
        core.info(`Fetching commit message for SHA: ${commitSha}`);
        const { data: commit } = await octokit.rest.git.getCommit({
          owner,
          repo,
          commit_sha: commitSha
        });
        contentToCheck = commit.message;
      } else {
        core.warning('Action triggered outside of a push or pull_request event, or no head_commit/PR context found, but target-type is "commit_message". Skipping check.');
        core.setOutput('whimsy-detected', true); // Pass by default if context is wrong
        return;
      }
    } else {
      core.setFailed(`Invalid target-type: ${targetType}. Must be "pr_title" or "commit_message".`);
      return;
    }

    const contentLower = contentToCheck.toLowerCase();
    const foundWhimsy = keywords.some(keyword => contentLower.includes(keyword));

    core.info(`Checking for whimsy in "${contentToCheck}" (target: ${targetType}). Keywords: [${keywords.join(', ')}]`);

    if (foundWhimsy) {
      core.info('Whimsy detected! The ApocalypsAI approves.');
      core.setOutput('whimsy-detected', true);
    } else {
      core.setFailed('No whimsy detected. Please add a touch of ApocalypsAI magic to your ' + (targetType === 'pr_title' ? 'PR title' : 'commit message') + '.');
      core.setOutput('whimsy-detected', false);
    }

  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
