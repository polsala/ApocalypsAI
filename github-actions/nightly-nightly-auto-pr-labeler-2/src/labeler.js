const fs = require('fs');

function getLabelFromTitle(title) {
  const lower = title.toLowerCase();
  if (lower.startsWith('feat')) return 'feature';
  if (lower.startsWith('fix')) return 'bug';
  if (lower.startsWith('docs')) return 'documentation';
  if (lower.startsWith('chore')) return 'chore';
  if (lower.startsWith('refactor')) return 'refactor';
  return null;
}

function main() {
  const eventPath = process.env.GITHUB_EVENT_PATH;
  if (!eventPath) {
    console.error('GITHUB_EVENT_PATH not set');
    process.exit(1);
  }
  const raw = fs.readFileSync(eventPath, 'utf8');
  const event = JSON.parse(raw);
  const title = event.pull_request?.title;
  if (!title) {
    console.error('No PR title found in event payload');
    process.exit(1);
  }
  const label = getLabelFromTitle(title);
  if (!label) {
    console.log(`No matching label for title: "${title}"`);
    return;
  }
  // Emit as a workflow output (GitHub Actions syntax)
  console.log(`::set-output name=label::${label}`);
  // Placeholder for real API call:
  // console.log(`Would add label '${label}' to PR #${event.pull_request.number}`);
}

if (require.main === module) {
  main();
}

module.exports = { getLabelFromTitle };
