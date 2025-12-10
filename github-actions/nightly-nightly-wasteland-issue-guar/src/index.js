const core = require('@actions/core');
const github = require('@actions/github');
const fs = require('fs');
const yaml = require('yaml');

try {
  const token = core.getInput('token');
  const tipsFile = core.getInput('tips-file');
  const octokit = new github.GitHub(token);

  // Load tips
  const tipsContent = fs.readFileSync(tipsFile, 'utf8');
  const tips = yaml.parse(tipsContent);
  const randomTip = tips[Math.floor(Math.random() * tips.length)];

  // Mock rationale: Simulate GitHub API interaction
  const mockIssue = {
    number: 123,
    owner: 'test-owner',
    repo: 'test-repo'
  };

  // In real implementation:
  // const {context} = github;
  // const issueNumber = context.payload.issue.number;

  // Add label
  octokit.issues.addLabels({
    owner: mockIssue.owner,
    repo: mockIssue.repo,
    issue_number: mockIssue.number,
    labels: ['wasteland-guardian']
  });

  // Add comment
  octokit.issues.createComment({
    owner: mockIssue.owner,
    repo: mockIssue.repo,
    issue_number: mockIssue.number,
    body: `🌵 **Survival Tip:** ${randomTip}
> Stay hydrated in the digital wasteland!`
  });

  core.setOutput('added_tip', randomTip);
} catch (error) {
  core.setFailed(error.message);
}
