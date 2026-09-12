const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const githubToken = core.getInput('github-token', { required: true });
    const alignmentKeywordsInput = core.getInput('alignment-keywords');
    const keywords = alignmentKeywordsInput.split(',').map(k => k.trim().toLowerCase()).filter(k => k.length > 0);

    const octokit = github.getOctokit(githubToken);

    const context = github.context;

    if (context.eventName !== 'pull_request') {
      core.warning('This action is intended to run on pull_request events only.');
      core.setOutput('is-aligned', true); // Not a PR, so consider it aligned by default
      return;
    }

    const pr = context.payload.pull_request;
    const prTitle = pr.title.toLowerCase();
    let isAligned = false;

    // Check PR title
    for (const keyword of keywords) {
      if (prTitle.includes(keyword)) {
        isAligned = true;
        break;
      }
    }

    // If not aligned by title, check commit messages
    if (!isAligned) {
      const { data: commits } = await octokit.rest.pulls.listCommits({
        owner: context.repo.owner,
        repo: context.repo.repo,
        pull_number: pr.number,
      });

      for (const commit of commits) {
        const commitMessage = commit.commit.message.toLowerCase();
        for (const keyword of keywords) {
          if (commitMessage.includes(keyword)) {
            isAligned = true;
            break;
          }
        }
        if (isAligned) break;
      }
    }

    core.setOutput('is-aligned', isAligned);

    if (!isAligned) {
      const defaultKeywordsForComment = ['star', 'galaxy', 'nebula'];
      const exampleKeywords = keywords.length > 0 ? keywords.slice(0, 3) : defaultKeywordsForComment;
      const exampleKeywordsString = exampleKeywords.map(k => `'${k}'`).join(', ');

      const commentBody = `Greetings, fellow traveler! The cosmic currents whisper that your recent contribution might benefit from a touch more stellar alignment. Consider infusing your title or messages with words like ${exampleKeywordsString} to truly resonate with the celestial symphony of our repository. May your code shine bright!`;

      await octokit.rest.issues.createComment({
        owner: context.repo.owner,
        repo: context.repo.repo,
        issue_number: pr.number,
        body: commentBody,
      });
      core.info('Cosmic alignment suggestion posted to PR.');
    } else {
      core.info('Cosmic alignment detected! The universe is pleased.');
    }

  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
