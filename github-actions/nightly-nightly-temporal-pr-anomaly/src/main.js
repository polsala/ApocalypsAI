const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const githubToken = core.getInput('github-token', { required: true });
    const octokit = github.getOctokit(githubToken);

    const pr = github.context.payload.pull_request;

    if (!pr) {
      core.info('This action only runs on pull_request events. Skipping.');
      return;
    }

    const prTitle = pr.title.toLowerCase();
    core.debug(`PR Title: ${prTitle}`);

    const commitMessages = await getCommitMessages(octokit, pr);
    const allText = prTitle + ' ' + commitMessages.join(' ').toLowerCase();
    core.debug(`All text to scan: ${allText}`);

    const temporalKeywords = [
      'time travel', 'temporal shift', 'paradox', 'future past',
      'alternate timeline', 'chronos', 'spacetime', 'time-warp',
      'dimension jump', 'retrograde', 'anachronism'
    ];

    let anomalyDetected = false;
    for (const keyword of temporalKeywords) {
      if (allText.includes(keyword)) {
        anomalyDetected = true;
        core.info(`Temporal anomaly keyword detected: "${keyword}"`);
        break;
      }
    }

    if (anomalyDetected) {
      const whimsicalWarnings = [
        "Warning: Temporal distortion detected in this Pull Request! Please ensure your changes do not create any unforeseen paradoxes. The Chrono-Guardians are watching.",
        "A ripple in the spacetime continuum has been observed! This PR title or commit message suggests a temporal anomaly. Proceed with caution, lest you unravel the fabric of reality.",
        "Our sensors are flaring! 'Time travel' related keywords detected. Remember, even a small change here could butterfly-effect into a dinosaur-infested future. Or past. It's confusing.",
        "The Temporal Anomaly Detection Unit has flagged this PR. While we appreciate your adventurous spirit, please refrain from altering historical events within the codebase.",
        "Hold on to your timelines! This PR seems to be playing fast and loose with causality. A friendly reminder: no altering the past, present, or future without proper temporal permits.",
        "Whoa, watch out for those temporal eddies! Your PR has triggered our anomaly detectors. Let's keep the codebase's history consistent, shall we?"
      ];
      const randomWarning = whimsicalWarnings[Math.floor(Math.random() * whimsicalWarnings.length)];

      await octokit.rest.issues.createComment({
        owner: github.context.repo.owner,
        repo: github.context.repo.repo,
        issue_number: pr.number,
        body: `### 🚨 Temporal Anomaly Alert! 🚨\n\n${randomWarning}`
      });
      core.info('Whimsical temporal anomaly warning posted to PR.');
    } else {
      core.info('No temporal anomaly keywords detected. All clear for now.');
    }

  } catch (error) {
    core.setFailed(error.message);
  }
}

async function getCommitMessages(octokit, pr) {
  const { data: commits } = await octokit.rest.pulls.listCommits({
    owner: github.context.repo.owner,
    repo: github.context.repo.repo,
    pull_number: pr.number,
  });
  return commits.map(commit => commit.commit.message);
}

// Export the run function for testing
module.exports = run;

// Call run if not in a test environment (e.g., when run by GitHub Actions)
if (require.main === module) {
  run();
}
