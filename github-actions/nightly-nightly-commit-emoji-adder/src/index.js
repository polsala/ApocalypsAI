const core = require("@actions/core");
const github = require("@actions/github");
const { computeEmojis } = require("./emoji");

async function run() {
  try {
    const token = core.getInput("repo-token", { required: true });
    const octokit = github.getOctokit(token);
    const context = github.context;

    if (!context.payload.pull_request) {
      core.info("No pull request context, exiting.");
      return;
    }

    const { owner, repo } = context.repo;
    const prNumber = context.payload.pull_request.number;

    // Get commits in the PR
    const commits = await octokit.paginate(octokit.rest.pulls.listCommits, {
      owner,
      repo,
      pull_number: prNumber
    });

    const messages = commits.map(c => c.commit.message);
    const emojis = computeEmojis(messages);
    if (emojis.length === 0) {
      core.info("No matching commit types found, nothing to do.");
      return;
    }

    const emojiPrefix = emojis.join(" ");
    const pr = await octokit.rest.pulls.get({ owner, repo, pull_number: prNumber });
    const originalTitle = pr.data.title;

    // Avoid duplicate prefix
    if (originalTitle.startsWith(emojiPrefix)) {
      core.info("PR title already contains emojis, skipping.");
      return;
    }

    const newTitle = `${emojiPrefix} ${originalTitle}`;
    await octokit.rest.pulls.update({
      owner,
      repo,
      pull_number: prNumber,
      title: newTitle
    });

    core.info(`Updated PR title to: ${newTitle}`);
  } catch (error) {
    core.setFailed(`Action failed with error: ${error}`);
  }
}

run();
