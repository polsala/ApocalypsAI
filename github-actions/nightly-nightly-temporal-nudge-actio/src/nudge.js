const core = require('@actions/core');
const github = require('@actions/github');

async function run(core, github) {
    try {
        const token = core.getInput('repo-token', { required: true });
        const staleDays = parseInt(core.getInput('stale-days') || '30', 10);
        const nudgeMessage = core.getInput('nudge-message') || 'A whisper from the temporal currents suggests this thread might appreciate a fresh perspective. What new insights have emerged from the time-stream?';
        const labelsToIgnore = core.getInput('labels-to-ignore').split(',').map(label => label.trim()).filter(label => label.length > 0);
        const dryRun = core.getInput('dry-run') === 'true';

        const { owner, repo } = github.context.repo;
        const octokit = github.getOctokit(token);

        core.info(`Checking for stale issues and PRs in ${owner}/${repo} older than ${staleDays} days.`);
        if (labelsToIgnore.length > 0) {
            core.info(`Ignoring items with labels: ${labelsToIgnore.join(', ')}`);
        }
        if (dryRun) {
            core.info('Dry run enabled: No comments will be posted.');
        }

        const staleDate = new Date();
        staleDate.setDate(staleDate.getDate() - staleDays);

        // Fetch issues (excluding pull requests)
        const issues = await octokit.rest.issues.listForRepo({
            owner,
            repo,
            state: 'open',
            per_page: 100, // Max per page
        });

        // Fetch pull requests
        const pullRequests = await octokit.rest.pulls.list({
            owner,
            repo,
            state: 'open',
            per_page: 100, // Max per page
        });

        const allOpenItems = [
            ...issues.data.filter(item => !item.pull_request), // Filter out PRs from issues list
            ...pullRequests.data
        ];

        for (const item of allOpenItems) {
            const itemType = item.pull_request ? 'PR' : 'Issue';
            const itemUrl = item.html_url;
            const itemNumber = item.number;
            const itemUpdatedAt = new Date(item.updated_at);

            if (itemUpdatedAt < staleDate) {
                core.info(`Found potentially stale ${itemType} #${itemNumber} (${item.title}). Last updated: ${itemUpdatedAt.toISOString()}`);

                const hasIgnoredLabel = item.labels.some(label => labelsToIgnore.includes(label.name));
                if (hasIgnoredLabel) {
                    core.info(`  ${itemType} #${itemNumber} has an ignored label. Skipping.`);
                    continue;
                }

                // Check if a nudge comment already exists
                const comments = await octokit.rest.issues.listComments({
                    owner,
                    repo,
                    issue_number: itemNumber,
                });

                const hasNudgeComment = comments.data.some(comment => comment.body.includes(nudgeMessage));
                if (hasNudgeComment) {
                    core.info(`  ${itemType} #${itemNumber} already has a nudge comment. Skipping.`);
                    continue;
                }

                if (dryRun) {
                    core.info(`Dry run: Would have nudged ${itemType} #${itemNumber} (${item.title}) at ${itemUrl}`);
                } else {
                    core.info(`Nudging ${itemType} #${itemNumber} (${item.title}) at ${itemUrl}`);
                    await octokit.rest.issues.createComment({
                        owner,
                        repo,
                        issue_number: itemNumber,
                        body: nudgeMessage,
                    });
                }
            }
        }
    } catch (error) {
        core.setFailed(error.message);
    }
}

// Only run if not being imported for testing
if (require.main === module) {
    run(core, github);
}

module.exports = { run }; // Export for testing
