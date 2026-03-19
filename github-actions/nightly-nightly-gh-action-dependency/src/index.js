const core = require('@actions/core');
const github = require('@actions/github');
const fs = require('fs');
const path = require('path');

async function run() {
  try {
    const workflowPath = core.getInput('workflow_path', { required: true });

    const outdatedDependencies = {};

    const files = fs.readdirSync(workflowPath);

    for (const file of files) {
      if (file.endsWith('.yml') || file.endsWith('.yaml')) {
        const filePath = path.join(workflowPath, file);
        const content = fs.readFileSync(filePath, 'utf8');
        const lines = content.split('\n');

        for (const line of lines) {
          // Basic regex to find 'uses: owner/repo@version'
          // This is a simplified approach and might need refinement for complex cases.
          const match = line.match(/uses:\s*([a-zA-Z0-9-]+\/[a-zA-Z0-9-_]+)@([a-zA-Z0-9.-]+)/);
          if (match) {
            const repo = match[1];
            const version = match[2];

            // In a real-world scenario, you'd fetch the latest version from GitHub API
            // or a dependency registry and compare. For this example, we'll mock it.
            // We'll assume 'v3' for actions/checkout and 'v2' for actions/setup-node are outdated.
            if ((repo === 'actions/checkout' && version !== 'v4') ||
                (repo === 'actions/setup-node' && version !== 'v3')) {
              outdatedDependencies[repo] = version;
            }
          }
        }
      }
    }

    core.setOutput('outdated_dependencies', JSON.stringify(outdatedDependencies));

  } catch (error) {
    core.setFailed(error.message);
  }
}

run();
