const core = require('@actions/core');
const { generateForecast } = require('./forecast');

try {
  const issueCount = parseInt(core.getInput('issue_count'), 10);
  const prCount = parseInt(core.getInput('pr_count'), 10);
  const forecast = generateForecast(issueCount, prCount);
  core.setOutput('forecast', forecast);
  console.log(forecast);
  // Optional: post a comment if a token is supplied (omitted for simplicity)
} catch (error) {
  core.setFailed(error.message);
}
