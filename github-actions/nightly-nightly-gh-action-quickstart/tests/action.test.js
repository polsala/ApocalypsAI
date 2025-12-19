const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

// Mock the core module
const core = {
  getInput: (name) => {
    const inputs = {
      'workflow-name': 'test-workflow.yml',
      'run-on': 'push',
      'run-on-branch': 'main',
      'job-name': 'test-job',
      'steps': '[{"name": "Checkout", "uses": "actions/checkout@v4"}, {"name": "Hello World", "run": "echo \"Hello, world!\""}]'
    };
    return inputs[name];
  },
  setOutput: () => {},
  info: () => {}
};

// Test workflow generation
const workflow = {
  name: core.getInput('workflow-name'),
  on: {
    [core.getInput('run-on')]: {
      branches: [core.getInput('run-on-branch')]
    }
  },
  jobs: {
    [core.getInput('job-name')]: {
      runs-on: 'ubuntu-latest',
      steps: JSON.parse(core.getInput('steps'))
    }
  }
};

const yamlStr = yaml.dump(workflow);
console.log('Generated workflow YAML:');
console.log(yamlStr);

// Verify the YAML is valid
try {
  const parsed = yaml.load(yamlStr);
  console.log('YAML is valid!');
  console.log('Parsed workflow name:', parsed.name);
} catch (e) {
  console.error('Invalid YAML:', e);
  process.exit(1);
}

console.log('Test passed!');
