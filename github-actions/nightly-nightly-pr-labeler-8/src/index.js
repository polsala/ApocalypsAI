const fs = require('fs');

function determineLabels(files) {
  const labels = new Set();
  for (const f of files) {
    if (f.startsWith('docs/') || f.endsWith('.md')) {
      labels.add('documentation');
    }
    if (f.startsWith('tests/') || f.endsWith('.test.js') || f.endsWith('.spec.js')) {
      labels.add('tests');
    }
    if (f.startsWith('.github/') || f.includes('workflow')) {
      labels.add('ci');
    }
    if (f.endsWith('.py')) {
      labels.add('python');
    }
  }
  return Array.from(labels);
}

// GitHub provides the event payload path in GITHUB_EVENT_PATH
const eventPath = process.env.GITHUB_EVENT_PATH;
if (!eventPath) {
  console.error('GITHUB_EVENT_PATH not set');
  process.exit(1);
}
let event;
try {
  event = JSON.parse(fs.readFileSync(eventPath, 'utf8'));
} catch (e) {
  console.error('Failed to read event payload:', e.message);
  process.exit(1);
}

// Expect a custom field "files" array for simplicity
const files = Array.isArray(event.files) ? event.files : [];
const labels = determineLabels(files);
// Output JSON array to stdout – callers can capture this output
console.log(JSON.stringify(labels));
