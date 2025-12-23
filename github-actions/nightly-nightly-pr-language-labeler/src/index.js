const fs = require('fs');
const path = require('path');

// Mapping from file extension to language label suffix
const EXTENSION_MAP = {
  '.py': 'python',
  '.js': 'javascript',
  '.ts': 'typescript',
  '.java': 'java',
  '.go': 'go',
  '.rs': 'rust',
  '.cpp': 'cpp',
  '.c': 'c',
  '.rb': 'ruby',
  '.php': 'php',
  '.sh': 'shell',
  '.html': 'html',
  '.css': 'css',
  '.json': 'json',
  '.yml': 'yaml',
  '.yaml': 'yaml',
  '.md': 'markdown'
};

function getChangedFiles(event) {
  // The generator expects a `changed_files` array in the event payload.
  // This is a simplification for offline testing.
  return event.changed_files || [];
}

function detectLanguages(files) {
  const labels = new Set();
  files.forEach(f => {
    const ext = path.extname(f).toLowerCase();
    const lang = EXTENSION_MAP[ext];
    if (lang) {
      labels.add(lang);
    }
  });
  return labels;
}

// Main execution
function run() {
  const eventPath = process.env.GITHUB_EVENT_PATH;
  if (!eventPath) {
    console.error('GITHUB_EVENT_PATH not set');
    process.exit(1);
  }

  const raw = fs.readFileSync(eventPath, 'utf8');
  const event = JSON.parse(raw);
  const files = getChangedFiles(event);
  const languages = detectLanguages(files);

  const prefix = process.env['INPUT_LABEL_PREFIX'] || 'lang-';
  const outputLabels = Array.from(languages).map(l => `${prefix}${l}`).join(',');

  // Set the output for the action
  console.log(`::set-output name=labels::${outputLabels}`);
}

run();
