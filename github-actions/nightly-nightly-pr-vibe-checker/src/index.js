const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const token = core.getInput('github-token', { required: true });
    const threshold = parseFloat(core.getInput('threshold') || '0');
    const positiveKeywordsInput = core.getInput('positive-keywords');
    const negativeKeywordsInput = core.getInput('negative-keywords');
    const checkTitle = core.getInput('check-title') === 'true';
    const checkBody = core.getInput('check-body') === 'true';

    const positiveKeywords = positiveKeywordsInput.split(',').map(k => k.trim().toLowerCase()).filter(k => k.length > 0);
    const negativeKeywords = negativeKeywordsInput.split(',').map(k => k.trim().toLowerCase()).filter(k => k.length > 0);

    const pr = github.context.payload.pull_request;

    if (!pr) {
      core.setFailed('This action only runs on pull_request events.');
      return;
    }

    let textToAnalyze = [];
    if (checkTitle && pr.title) {
      textToAnalyze.push(pr.title);
    }
    if (checkBody && pr.body) {
      textToAnalyze.push(pr.body);
    }

    if (textToAnalyze.length === 0) {
      core.warning('No title or body to analyze based on inputs. Skipping vibe check.');
      core.setOutput('vibe-score', 0);
      core.setOutput('vibe-status', 'Neutral');
      core.setOutput('suggestion', 'No text was analyzed.');
      return;
    }

    const fullText = textToAnalyze.join(' ').toLowerCase();
    let vibeScore = 0;

    positiveKeywords.forEach(keyword => {
      const regex = new RegExp(`\\b${keyword}\\b`, 'g');
      const matches = fullText.match(regex);
      if (matches) {
        vibeScore += matches.length;
      }
    });

    negativeKeywords.forEach(keyword => {
      const regex = new RegExp(`\\b${keyword}\\b`, 'g');
      const matches = fullText.match(regex);
      if (matches) {
        vibeScore -= matches.length;
      }
    });

    let vibeStatus;
    let suggestion = '';

    if (vibeScore >= threshold) {
      vibeStatus = 'High';
      suggestion = 'The vibes are strong with this one! Keep up the positive energy!';
    } else if (vibeScore >= threshold / 2) { // A bit arbitrary, but provides a 'Medium' state
      vibeStatus = 'Medium';
      suggestion = 'The vibes are okay, but a little sparkle could make them shine brighter!';
    } else {
      vibeStatus = 'Low';
      suggestion = 'Oh dear, the vibes are a bit low. Perhaps a cheerful emoji or a positive affirmation could help?';

      // Post a comment to the PR if vibes are low
      const octokit = github.getOctokit(token);
      await octokit.rest.issues.createComment({
        owner: github.context.repo.owner,
        repo: github.context.repo.repo,
        issue_number: pr.number,
        body: `✨ **Vibe Check Alert!** ✨\n\nIt seems the vibes in this PR are a bit low (${vibeScore}).\n\n${suggestion}\n\nLet's keep our spirits high and our code even higher! 🚀`
      });
      core.warning(`PR vibes are low (${vibeScore}). A suggestion has been posted.`);
    }

    core.setOutput('vibe-score', vibeScore);
    core.setOutput('vibe-status', vibeStatus);
    core.setOutput('suggestion', suggestion);

  } catch (error) {
    core.setFailed(error.message);
  }
}

// Call run() if not being tested, or export it for testing
if (require.main === module) {
  run();
} else {
  module.exports = run; // Export for Jest tests
}
