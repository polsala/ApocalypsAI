// Auto‑label PRs by file extensions
function detectLabels(files) {
  const extMap = {
    '.py': 'language:python',
    '.js': 'language:javascript',
    '.ts': 'language:typescript',
    '.go': 'language:go',
    '.rs': 'language:rust',
    '.sh': 'language:shell',
    '.java': 'language:java',
    '.cpp': 'language:cpp',
    '.c': 'language:c',
    '.rb': 'language:ruby',
    '.php': 'language:php',
    '.html': 'language:html',
    '.css': 'language:css',
    '.md': 'language:markdown'
  };
  const labels = new Set();
  files.forEach(f => {
    const ext = f.slice(f.lastIndexOf('.')).toLowerCase();
    if (extMap[ext]) {
      labels.add(extMap[ext]);
    }
  });
  return Array.from(labels);
}

// When run as an action, read INPUT_FILES env var (comma‑separated)
if (require.main === module) {
  const filesEnv = process.env['INPUT_FILES'] || '';
  const files = filesEnv.split(',').filter(Boolean);
  const labels = detectLabels(files);
  // Output for GitHub Actions (v2)
  const fs = require('fs');
  const outputPath = process.env['GITHUB_OUTPUT'];
  if (outputPath) {
    fs.appendFileSync(outputPath, `labels=${labels.join(',')}\n`);
  } else {
    console.log('Detected labels:', labels);
  }
}

// Export for testing
module.exports = {detectLabels};
