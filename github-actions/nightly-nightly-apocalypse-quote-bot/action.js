const core = require('@actions/core');
const github = require('@actions/github');

try {
  const token = core.getInput('token');
  const issueNumber = core.getInput('issue_number');
  const quotes = core.getInput('quotes').split('\n').filter(q => q.trim());

  const octokit = new github.GitHub(token);
  const randomQuote = quotes[Math.floor(Math.random() * quotes.length)];

  octokit.rest.issues.createComment({
    owner: github.context.repo.owner,
    repo: github.context.repo.repo,
    issue_number: issueNumber,
    body: `🔔 **Daily Apocalypse Quote**:

> ${randomQuote}

*Automated by the End Times Comment Bot* 🤖`
  });

  core.setOutput('posted_quote', randomQuote);
} catch (error) {
  core.setFailed(error.message);
}
