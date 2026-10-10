const core = require('@actions/core');
const github = require('@actions/github');

async function run() {
  try {
    const minTitleLength = parseInt(core.getInput('min_title_length') || '10', 10);
    const maxTitleLength = parseInt(core.getInput('max_title_length') || '100', 10);
    const minBodyLength = parseInt(core.getInput('min_body_length') || '20', 10);
    const maxBodyLength = parseInt(core.getInput('max_body_length') || '500', 10);
    const requiredKeywords = (core.getInput('required_keywords') || '').split(',').map(k => k.trim()).filter(k => k);
    const disallowedKeywords = (core.getInput('disallowed_keywords') || '').split(',').map(k => k.trim()).filter(k => k);
    const failOnInconsistency = core.getInput('fail_on_inconsistency') === 'true';
    const githubToken = core.getInput('github_token');

    const pr = github.context.payload.pull_request;

    if (!pr) {
      core.setFailed('This action only runs on pull_request events.');
      return;
    }

    const prTitle = pr.title || '';
    const prBody = pr.body || '';
    const prNumber = pr.number;
    const repo = github.context.repo;

    let isConsistent = true;
    const inconsistencies = [];

    // Title length check
    if (prTitle.length < minTitleLength) {
      inconsistencies.push(`Title is too short (${prTitle.length} chars). Minimum required: ${minTitleLength}.`);
      isConsistent = false;
    }
    if (prTitle.length > maxTitleLength) {
      inconsistencies.push(`Title is too long (${prTitle.length} chars). Maximum allowed: ${maxTitleLength}.`);
      isConsistent = false;
    }

    // Body length check
    if (prBody.length < minBodyLength) {
      inconsistencies.push(`Description is too short (${prBody.length} chars). Minimum required: ${minBodyLength}.`);
      isConsistent = false;
    }
    if (prBody.length > maxBodyLength) {
      inconsistencies.push(`Description is too long (${prBody.length} chars). Maximum allowed: ${maxBodyLength}.`);
      isConsistent = false;
    }

    // Required keywords check
    for (const keyword of requiredKeywords) {
      if (!prTitle.includes(keyword) && !prBody.includes(keyword)) {
        inconsistencies.push(`Missing required keyword: "${keyword}" in title or description.`);
        isConsistent = false;
      }
    }

    // Disallowed keywords check
    for (const keyword of disallowedKeywords) {
      if (prTitle.includes(keyword) || prBody.includes(keyword)) {
        inconsistencies.push(`Contains disallowed keyword: "${keyword}" in title or description.`);
        isConsistent = false;
      }
    }

    if (!isConsistent) {
      const octokit = github.getOctokit(githubToken);
      const commentBody = `### 🕰️ Chrono-Consistency Anomaly Detected! 🕰️\n\nYour Pull Request seems to be experiencing some temporal drift. Please adjust it to align with the project's established flow.\n\n**Inconsistencies found:**\n${inconsistencies.map(i => `- ${i}`).join('\n')}\n\n*The fabric of time demands precision!*`;

      await octokit.rest.issues.createComment({
        owner: repo.owner,
        repo: repo.repo,
        issue_number: prNumber,
        body: commentBody
      });

      if (failOnInconsistency) {
        core.setFailed(`PR is not chrono-consistent. ${inconsistencies.length} issues found.`);
      } else {
        core.warning(`PR is not chrono-consistent. ${inconsistencies.length} issues found.`);
      }
    } else {
      core.info('PR is perfectly chrono-consistent! The timeline is stable.');
    }

    core.setOutput('is_chrono_consistent', isConsistent);

  } catch (error) {
    core.setFailed(error.message);
  n}
}

run();
