const core = require('@actions/core');
const fs = require('fs');
const path = require('path');

async function run() {
  try {
    const inputDir = core.getInput('input-dir');
    const outputFile = core.getInput('output-file');

    if (!fs.existsSync(inputDir)) {
      core.setFailed(`Input directory does not exist: ${inputDir}`);
      return;
    }

    const files = fs.readdirSync(inputDir);
    const reports = files.filter(f => f.endsWith('.json'));

    let totalRuns = 0;
    let failedRuns = 0;
    const failures = [];

    for (const file of reports) {
      const filePath = path.join(inputDir, file);
      const content = fs.readFileSync(filePath, 'utf-8');
      let data;
      try {
        data = JSON.parse(content);
      } catch (e) {
        core.warning(`Skipping invalid JSON file: ${file}`);
        continue;
      }

      totalRuns += 1;
      if (!data.success) {
        failedRuns += 1;
        failures.push({ id: data.run_id || file, reason: data.reason || 'Unknown' });
      }
    }

    const successRate = totalRuns > 0 ? ((totalRuns - failedRuns) / totalRuns * 100).toFixed(2) : 0;

    const markdown = `# Chaos Engineering Summary

- Total Runs: ${totalRuns}
- Failed Runs: ${failedRuns}
- Success Rate: ${successRate}%

## Failures

${failures.map(f => `- Run ID: \`${f.id}\` - Reason: ${f.reason}`).join('\n')}`;

    fs.writeFileSync(outputFile, markdown);

    core.setOutput('summary-path', outputFile);
    core.setOutput('total-runs', totalRuns);
    core.setOutput('failed-runs', failedRuns);

  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
