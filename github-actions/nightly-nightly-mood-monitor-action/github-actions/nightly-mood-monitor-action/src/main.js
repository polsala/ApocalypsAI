const core = require('@actions/core');
const github = require('@actions/github');

/**
 * Analyzes the sentiment and thematic consistency of a given text.
 * @param {string} text - The text to analyze.
 * @param {string[]} positiveKeywords - List of positive keywords.
 * @param {string[]} negativeKeywords - List of negative keywords.
 * @param {string[]} thematicKeywords - List of thematic keywords.
 * @param {number} neutralThreshold - Threshold for neutral sentiment.
 * @returns {{mood: string, score: number, suggestions: string[]}}
 */
function analyzeMood(text, positiveKeywords, negativeKeywords, thematicKeywords, neutralThreshold) {
    const lowerText = text.toLowerCase();
    let positiveScore = 0;
    let negativeScore = 0;
    let thematicScore = 0;
    const suggestions = [];

    // Count positive keywords
    positiveKeywords.forEach(keyword => {
        if (lowerText.includes(keyword)) {
            positiveScore++;
        }
    });

    // Count negative keywords
    negativeKeywords.forEach(keyword => {
        if (lowerText.includes(keyword)) {
            negativeScore++;
        }
    });

    // Count thematic keywords
    thematicKeywords.forEach(keyword => {
        if (lowerText.includes(keyword)) {
            thematicScore++;
        }
    });

    let mood = 'neutral';
    let score = positiveScore - negativeScore;

    if (score > neutralThreshold) {
        mood = 'positive';
    } else if (score < -neutralThreshold) {
        mood = 'negative';
    }

    if (thematicKeywords.length > 0 && thematicScore === 0) {
        suggestions.push("The void whispers for more thematic flair! Consider adding terms like 'wasteland', 'anomaly', or 'scavenge' to your description.");
        if (mood === 'neutral') {
            mood = 'off-topic'; // More specific if no thematic words and neutral sentiment
        }
    } else if (thematicScore > 0) {
        if (mood === 'neutral') {
            mood = 'thematic'; // If neutral but has thematic words, it's thematic
        }
        suggestions.push("Excellent thematic integration! Your words resonate with the spirit of ApocalypsAI.");
    }

    if (mood === 'positive') {
        suggestions.push("Your message radiates hope in the desolate future! Keep that spirit alive, survivor!");
    } else if (mood === 'negative') {
        suggestions.push("A tremor of despair detected. Remember, even in the darkest rifts, solutions can be found. Let's rephrase for resilience!");
    }

    return { mood, score, suggestions };
}

async function run() {
    try {
        const token = core.getInput('github-token', { required: true });
        const positiveKeywords = core.getInput('positive-keywords').split(',').map(s => s.trim()).filter(Boolean);
        const negativeKeywords = core.getInput('negative-keywords').split(',').map(s => s.trim()).filter(Boolean);
        const thematicKeywords = core.getInput('thematic-keywords').split(',').map(s => s.trim()).filter(Boolean);
        const neutralThreshold = parseFloat(core.getInput('neutral-threshold'));

        const octokit = github.getOctokit(token);
        const payload = github.context.payload;

        let content = '';
        let issueNumber;

        if (github.context.eventName === 'issues') {
            content = `${payload.issue.title}\n${payload.issue.body || ''}`;
            issueNumber = payload.issue.number;
        } else if (github.context.eventName === 'pull_request_target') {
            content = `${payload.pull_request.title}\n${payload.pull_request.body || ''}`;
            issueNumber = payload.pull_request.number;
        } else {
            core.info('This action only runs on issues or pull_request_target events. Skipping.');
            return;
        }

        if (!issueNumber) {
            core.setFailed('Could not determine issue or pull request number.');
            return;
        }

        const { mood, suggestions } = analyzeMood(content, positiveKeywords, negativeKeywords, thematicKeywords, neutralThreshold);

        core.setOutput('mood-status', mood);

        if (suggestions.length > 0) {
            const commentBody = `### ApocalypsAI Mood Monitor Report\n\nDetected Mood: **${mood.charAt(0).toUpperCase() + mood.slice(1)}**\n\n${suggestions.map(s => `- ${s}`).join('\n')}\n\n*Stay vigilant, survivor!*`;
            await octokit.rest.issues.createComment({
                owner: github.context.repo.owner,
                repo: github.context.repo.repo,
                issue_number: issueNumber,
                body: commentBody
            });
            core.info(`Commented on #${issueNumber}: ${commentBody}`);
        }

    } catch (error) {
        core.setFailed(error.message);
    }
}

module.exports = { analyzeMood, run }; // Export for testing

if (require.main === module) {
    run();
}
