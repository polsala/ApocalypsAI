// Mock rationale: we replace @actions/core and @actions/github with simple stubs
const assert = require('assert');

// Mock core
const core = {
  inputs: {
    'github-token': 'fake-token',
    'label-mapping': '{"*.md":"docs"}'
  },
  getInput(name, opts) {
    if (opts && opts.required && !(name in this.inputs)) {
      throw new Error(`Missing required input ${name}`);
    }
    return this.inputs[name] || '';
  },
  setFailed(msg) { throw new Error(msg); },
  info(msg) { /* no‑op */ }
};

// Mock github context and octokit
const github = {
  context: {
    repo: { owner: 'owner', repo: 'repo' },
    payload: { pull_request: { number: 42 } }
  },
  getOctokit(token) {
    return {
      rest: {
        pulls: {
          listFiles: async () => ({ data: [ { filename: 'README.md' }, { filename: 'src/app.js' } ] })
        },
        issues: {
          addLabels: async ({ owner, repo, issue_number, labels }) => {
            // Capture arguments for assertion
            github.captured = { owner, repo, issue_number, labels };
          }
        }
      }
    };
  }
};

// Replace Math.random to make emoji selection deterministic
Math.random = () => 0; // selects first emoji '😀'

// Load the action code with injected mocks
const proxyquire = require('proxyquire').noCallThru();
const action = proxyquire('../src/index.js', {
  '@actions/core': core,
  '@actions/github': github
});

(async () => {
  // The action runs automatically on import; we just await its completion
  // Since the original file calls run() at the end, we need to wait a tick
  await new Promise(resolve => setTimeout(resolve, 0));
  // Verify that labels were added correctly
  const expectedLabels = ['docs', '😀'];
  assert.deepStrictEqual(github.captured.labels.sort(), expectedLabels.sort(), 'Labels should match expected set');
  console.log('All tests passed.');
})();
