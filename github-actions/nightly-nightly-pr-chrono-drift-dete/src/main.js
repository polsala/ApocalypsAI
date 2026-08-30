const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const token = core.getInput('github-token', { required: true });
    const futureDateThresholdDays = parseInt(core.getInput('future-date-threshold-days') || '7', 10);
    const stalePrThresholdDays = parseInt(core.getInput('stale-pr-threshold-days') || '30', 10);
    const ignoreDrafts = core.getInput('ignore-drafts') === 'true';

    const { pull_request: pr } = github.context.payload;

    if (!pr) {
      core.warning('This action only runs on pull_request events. Skipping.');
      return;
    }

    // const octokit = github.getOctokit(token); // Not strictly needed for current logic, but good to keep for future API calls
    // const owner = github.context.repo.owner;
    // const repo = github.context.repo.repo;
    // const prNumber = pr.number;

    const driftDetails = [];
    let chronoDriftDetected = false;

    const now = new Date();
    now.setHours(0, 0, 0, 0); // Normalize to start of day for comparison

    // 1. Check for future-dated claims in title/body
    const prContent = `${pr.title || ''} ${pr.body || ''}`;
    // Regex to find common date formats: YYYY-MM-DD, M/D/YYYY, Month D, YYYY
    const dateRegex = /\b(\d{4}-\d{2}-\d{2}|\d{1,2}\/\d{1,2}\/\d{4}|(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},\s+\d{4})\b/gi;
    let match;
    while ((match = dateRegex.exec(prContent)) !== null) {
      try {
        const matchedDate = new Date(match[0]);
        matchedDate.setHours(0, 0, 0, 0);

        const diffTime = matchedDate.getTime() - now.getTime();
        const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

        if (diffDays > futureDateThresholdDays) {
          chronoDriftDetected = true;
          driftDetails.push({
            type: 'future-dated-claim',
            date: match[0],
            context: match.input.substring(Math.max(0, match.index - 20), match.index + match[0].length + 20).trim(),
            message: `Found a date "${match[0]}" which is ${diffDays} days in the future, exceeding the ${futureDateThresholdDays}-day threshold.`
          });
          core.warning(`Chrono-Drift: ${driftDetails[driftDetails.length - 1].message}`);
        }
      } catch (e) {
        // Ignore invalid date formats that Date constructor might parse unexpectedly
      }
    }

    // 2. Check for stale PRs
    if (ignoreDrafts && pr.draft) {
      core.info('PR is a draft and ignore-drafts is true. Skipping stale PR check.');
    } else {
      const prCreatedAt = new Date(pr.created_at);
      const prUpdatedAt = new Date(pr.updated_at);

      const ageDays = Math.ceil((now.getTime() - prCreatedAt.getTime()) / (1000 * 60 * 60 * 24));
      const daysSinceLastUpdate = Math.ceil((now.getTime() - prUpdatedAt.getTime()) / (1000 * 60 * 60 * 24));

      // A PR is considered stale if it's old AND hasn't been updated recently (e.g., half the stale threshold)
      if (ageDays > stalePrThresholdDays && daysSinceLastUpdate > stalePrThresholdDays / 2) {
        chronoDriftDetected = true;
        driftDetails.push({
          type: 'stale-pr',
          pr_age_days: ageDays,
          days_since_last_update: daysSinceLastUpdate,
          message: `PR has been open for ${ageDays} days and last updated ${daysSinceLastUpdate} days ago, exceeding stale thresholds.`
        });
        core.warning(`Chrono-Drift: ${driftDetails[driftDetails.length - 1].message}`);
      }
    }

    core.setOutput('chrono-drift-detected', chronoDriftDetected);
    core.setOutput('drift-details', JSON.stringify(driftDetails));

    if (chronoDriftDetected) {
      core.setFailed('Chrono-Drift detected! Please review the PR for temporal inconsistencies.');
    }

  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
