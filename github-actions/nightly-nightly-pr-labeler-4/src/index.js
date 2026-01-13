// Nightly PR Labeler â core logic
// This file is deliberately lightweight and has no external dependencies.

const fs = require('fs');
const https = require('https');

/**
 * Return an array of labels whose keywords appear in the title.
 * @param {string} title Pullârequest title
 * @param {Object} mapping keyword â label (both strings)
 * @returns {string[]} list of labels to apply
 */
function getLabelsForTitle(title, mapping) {
  const lower = title.toLowerCase();
  const labels = [];
  for (const [keyword, label] of Object.entries(mapping)) {
    if (keyword && label && lower.includes(keyword.toLowerCase())) {
      labels.push(label);
    }
  }
  return labels;
}

/**
 * Post labels to the GitHub REST API.
 * @param {string} token GitHub token
 * @param {string} owner repo owner
 * @param {string} repo repo name
 * @param {number} issueNumber PR number (issues API works for PRs)
 * @param {string[]} labels array of label names
 * @returns {Promise<void>}
 */
function postLabels(token, owner, repo, issueNumber, labels) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify({ labels });
    const options = {
      hostname: 'api.github.com',
      path: `/repos/${owner}/${repo}/issues/${issueNumber}/labels`,
      method: 'POST',
      headers: {
        'User-Agent': 'nightly-pr-labeler',
        'Authorization': `token ${token}` ,
        'Accept': 'application/vnd.github+json',
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(data)
      }
    };
    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', (chunk) => body += chunk);
      res.on('end', () => {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve();
        } else {
          reject(new Error(`GitHub API responded ${res.statusCode}: ${body}`));
        }
      });
    });
    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

async function run() {
  try {
    const token = process.env['INPUT_GITHUB-TOKEN'];
    const mappingJson = process.env['INPUT_LABEL-MAPPING'];
    if (!token || !mappingJson) {
      throw new Error('Missing required inputs');
    }
    const mapping = JSON.parse(mappingJson);
    const eventPath = process.env['GITHUB_EVENT_PATH'];
    const eventData = JSON.parse(fs.readFileSync(eventPath, 'utf8'));
    const pr = eventData.pull_request;
    if (!pr) {
      console.log('No pull_request payload â exiting');
      return;
    }
    const title = pr.title || '';
    const labels = getLabelsForTitle(title, mapping);
    if (labels.length === 0) {
      console.log('No matching keywords â nothing to label');
      return;
    }
    const [owner, repo] = process.env['GITHUB_REPOSITORY'].split('/');
    const issueNumber = pr.number;
    await postLabels(token, owner, repo, issueNumber, labels);
    console.log(`Added labels: ${labels.join(', ')}`);
  } catch (error) {
    core.setFailed(error.message);
  }
}

// Export for testing
module.exports = { getLabelsForTitle, postLabels };

if (require.main === module) {
  run();
}

