const core = require('@actions/core');
const github = require('@actions/github');

function detectLanguages(files) {
  const extMap = {
    '.js': 'javascript',
    '.ts': 'typescript',
    '.py': 'python',
    '.go': 'go',
    '.rs': 'rust',
    '.java': 'java',
    '.cpp': 'cpp',
    '.c': 'c',
    '.rb': 'ruby',
    '.php': 'php',
    '.sh': 'shell',
    '.html': 'html',
    '.css': 'css',
    '.json': 'json',
    '.yml': 'yaml',
    '.yaml': 'yaml'
  };
  const langs = new Set();
  files.forEach(f => {
    const ext = f.slice(f.lastIndexOf('.')).toLowerCase();
    if (extMap[ext]) langs.add(extMap[ext]);
  });
  return Array.from(langs);
}

async function run() {
  try {
    const token = core.getInput('github-token', { required: true });
    const filesInput = core.getInput('files');
    let files = [];
    if (filesInput) {
      files = JSON.parse(filesInput);
    } else {
      const context = github.context;
      const prNumber = context.payload.pull_request.number;
      const octokit = github.getOctokit(token);
      const { data } = await octokit.rest.pulls.listFiles({
        owner: context.repo.owner,
        repo: context.repo.repo,
        pull_number: prNumber
      });
      files = data.map(f => f.filename);
    }
    const languages = detectLanguages(files);
    if (languages.length === 0) {
      core.info('No recognizable languages found.');
      return;
    }
    const labels = languages.map(l => `lang:${l}`);
    const context = github.context;
    const prNumber = context.payload.pull_request.number;
    const octokit = github.getOctokit(token);
    await octokit.rest.issues.addLabels({
      owner: context.repo.owner,
      repo: context.repo.repo,
      issue_number: prNumber,
      labels
    });
    core.info(`Added labels: ${labels.join(', ')}`);
  } catch (error) {
    core.setFailed(error.message);
  }
}

run();

module.exports = { detectLanguages, run };
