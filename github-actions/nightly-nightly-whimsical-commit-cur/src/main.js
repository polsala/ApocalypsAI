const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const token = core.getInput('github-token', { required: true });
    const daysAgo = parseInt(core.getInput('days-ago') || '7', 10);
    const keywordsInput = core.getInput('keywords') || '';
    const emojiPatternsInput = core.getInput('emoji-patterns') || '';

    const octokit = github.getOctokit(token);
    const { owner, repo } = github.context.repo;

    const sinceDate = new Date();
    sinceDate.setDate(sinceDate.getDate() - daysAgo);

    core.info(`Fetching commits for ${owner}/${repo} since ${sinceDate.toISOString()}...`);

    const commits = await octokit.rest.repos.listCommits({
      owner,
      repo,
      since: sinceDate.toISOString(),
      per_page: 100 // Fetch up to 100 commits
    });

    const allCommitMessages = commits.data.map(commit => commit.commit.message);

    const keywords = keywordsInput.split(',').map(k => k.trim().toLowerCase()).filter(k => k);
    const emojiPatterns = emojiPatternsInput.split(',').map(p => p.trim()).filter(p => p).map(p => new RegExp(p, 'i'));

    const isWhimsical = (message) => {
      const lowerMessage = message.toLowerCase();
      if (keywords.some(keyword => lowerMessage.includes(keyword))) {
        return true;
      }
      if (emojiPatterns.some(pattern => pattern.test(message))) {
        return true;
      }
      // Default whimsicality heuristic: if it's not a standard commit type and contains positive words
      const standardCommitTypes = ['feat:', 'fix:', 'docs:', 'chore:', 'refactor:', 'style:', 'test:', 'perf:', 'ci:', 'build:'];
      const isStandardCommit = standardCommitTypes.some(type => lowerMessage.startsWith(type));

      if (!isStandardCommit) {
        const positiveWords = ['joy', 'sparkle', 'magic', 'delight', 'fun', 'yay', 'hooray', 'awesome', 'fantastic', 'celebrate', '✨', '🎉', '🥳', '🚀'];
        if (positiveWords.some(word => lowerMessage.includes(word))) {
            return true;
        }
      }
      return false;
    };

    const whimsicalCommits = allCommitMessages.filter(isWhimsical);

    let summary = 'No particularly whimsical commits found recently. Keep up the good work!\n';
    if (whimsicalCommits.length > 0) {
      summary = `✨ Recent Whimsical Commits (${whimsicalCommits.length}):\n`;
      whimsicalCommits.forEach((msg, index) => {
        summary += `- ${msg.split('\n')[0].trim()}\n`; // Take first line of commit message
      });
    }

    core.setOutput('whimsical-commits', JSON.stringify(whimsicalCommits));
    core.setOutput('whimsical-summary', summary);

  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
