const core = require('@actions/core');
const github = require('@actions/github');

// Simple glob matcher supporting * and **
function matchesPattern(filePath, pattern) {
  // Escape regex special chars except *
  let regexStr = pattern.replace(/[-/\\^$+?.()|[\]{}]/g, '\\$&');
  // Replace **/ with (.*\/)?
  regexStr = regexStr.replace(/\*\*\//g, '(.*\\/)?');
  // Replace * with [^/]*
  regexStr = regexStr.replace(/\*/g, '[^/]*');
  const regex = new RegExp('^' + regexStr + '$');
  return regex.test(filePath);
}

async function run() {
  try {
    const token = core.getInput('github-token', { required: true });
    const mappingInput = core.getInput('label-mapping');
    const labelMapping = JSON.parse(mappingInput || '{}');
    const emojiList = ['😀','🚀','✨','🧩','🌟'];

    const octokit = github.getOctokit(token);
    const context = github.context;
    const pr = context.payload.pull_request;
    if (!pr) {
      core.setFailed('No pull request found in context.');
      return;
    }
    const owner = context.repo.owner;
    const repo = context.repo.repo;
    const prNumber = pr.number;

    // Get changed files
    const { data: files } = await octokit.rest.pulls.listFiles({ owner, repo, pull_number: prNumber });
    const labelsToAdd = new Set();

    for (const file of files) {
      const filePath = file.filename;
      for (const [pattern, label] of Object.entries(labelMapping)) {
        if (matchesPattern(filePath, pattern)) {
          labelsToAdd.add(label);
        }
      }
    }

    // Add a random emoji label
    const randomIdx = Math.floor(Math.random() * emojiList.length);
    labelsToAdd.add(emojiList[randomIdx]);

    if (labelsToAdd.size > 0) {
      await octokit.rest.issues.addLabels({
        owner,
        repo,
        issue_number: prNumber,
        labels: Array.from(labelsToAdd)
      });
      core.info(`Added labels: ${Array.from(labelsToAdd).join(', ')}`);
    } else {
      core.info('No labels to add.');
    }
  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
