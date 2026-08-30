const core = require('@actions/core');
const github = require('@actions/github');
const fs = require('fs');
const path = require('path');
const glob = require('glob');

// Mocking for deterministic testing
let mockFs = null;
let mockGlob = null;

function setMockFs(mock) {
  mockFs = mock;
}

function setMockGlob(mock) {
  mockGlob = mock;
}

function getFs() {
  return mockFs || fs;
}

function getGlob() {
  return mockGlob || glob;
}

function isValidYaml(filePath) {
  const content = getFs().readFileSync(filePath, 'utf8');
  try {
    // Basic YAML parsing check. A more robust check would involve a full YAML parser.
    // For this whimsical utility, we'll assume valid YAML if it doesn't throw on simple parsing.
    // In a real-world scenario, a dedicated YAML linter would be better.
    JSON.parse(JSON.stringify(require('js-yaml').load(content))); // Use js-yaml for parsing
    return true;
  } catch (e) {
    core.warning(`YAML parsing error in ${filePath}: ${e.message}`);
    return false;
  }
}

function lintWorkflowFile(filePath) {
  core.info(`Linting workflow file: ${filePath}`);
  let issues = [];

  // Basic checks for common GitHub Actions patterns
  const content = getFs().readFileSync(filePath, 'utf8');

  // Check for 'on:' trigger
  if (!content.includes('on:')) {
    issues.push('Workflow must have an `on:` trigger defined.');
  }

  // Check for 'jobs:' section
  if (!content.includes('jobs:')) {
    issues.push('Workflow must have a `jobs:` section defined.');
  }

  // Check for 'runs-on:' within jobs
  if (!content.match(/jobs:\s*\w+:\s*runs-on:/)) {
    issues.push('Each job must define a `runs-on:` runner.');
  }

  // Whimsical check: Ensure at least one job has a 'name' that sounds fun
  const jobNames = content.match(/jobs:\s*\w+:\s*name:\s*(.*)/g);
  if (!jobNames || !jobNames.some(name => name.toLowerCase().includes('fun') || name.toLowerCase().includes('adventure') || name.toLowerCase().includes('quest'))) {
    issues.push('Consider giving at least one job a more adventurous name for morale!');
  }

  // Check for secrets usage without explicit masking (basic check)
  if (content.includes('secrets.') && !content.includes('secrets.MASKED')) {
    issues.push('Be cautious when using `secrets.` directly. Consider using `secrets.MASKED` or specific secret names.');
  }

  // Check for common typos or deprecated keywords (example)
  if (content.includes('checkout@v1')) {
    issues.push('`actions/checkout@v1` is deprecated. Please use a newer version like `@v3` or `@v4`.');
  }

  return {
    filePath,
    issues,
    isValid: issues.length === 0
  };
}

async function run() {
  try {
    const workflowPathPattern = core.getInput('workflow_path') || '.github/workflows/*.yml';
    core.info(`Looking for workflows matching pattern: ${workflowPathPattern}`);

    const workflowFiles = getGlob().sync(workflowPathPattern, {
      nodir: true,
      absolute: true
    });

    if (workflowFiles.length === 0) {
      core.warning('No workflow files found matching the pattern. No linting performed.');
      core.setOutput('lint_status', 'success');
      core.setOutput('lint_summary', 'No workflow files found to lint.');
      return;
    }

    let allLintResults = [];
    let overallSuccess = true;

    for (const filePath of workflowFiles) {
      if (isValidYaml(filePath)) {
        const result = lintWorkflowFile(filePath);
        allLintResults.push(result);
        if (!result.isValid) {
          overallSuccess = false;
          core.error(`Linting failed for ${result.filePath}:`);
          result.issues.forEach(issue => core.error(`  - ${issue}`));
        } else {
          core.info(`Linting passed for ${result.filePath}`);
        }
      } else {
        overallSuccess = false;
        core.error(`Skipping linting for ${filePath} due to YAML parsing errors.`);
        allLintResults.push({
          filePath,
          issues: ['Invalid YAML structure.'],
          isValid: false
        });
      }
    }

    const summary = `Linting completed. ${allLintResults.filter(r => r.isValid).length} files passed, ${allLintResults.filter(r => !r.isValid).length} files failed.`;
    core.setOutput('lint_summary', summary);

    if (overallSuccess) {
      core.info('All GitHub Actions workflows linted successfully! Your automation is looking sharp!');
      core.setOutput('lint_status', 'success');
    } else {
      core.setFailed('Some GitHub Actions workflows failed linting. Please review the errors above.');
      core.setOutput('lint_status', 'failure');
    }

  } catch (error) {
    core.setFailed(`Action failed with error: ${error.message}`);
  }
}

// Exporting for testing purposes
module.exports = {
  run,
  lintWorkflowFile,
  isValidYaml,
  setMockFs,
  setMockGlob,
  getFs,
  getGlob
};
