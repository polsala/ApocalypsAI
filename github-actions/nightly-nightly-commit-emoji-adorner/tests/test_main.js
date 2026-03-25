// Mock rationale: we replace @actions/core and @actions/github with lightweight stubs so the test runs offline.
const core = require('@actions/core');
const github = require('@actions/github');
const action = require('../src/index');

// Simple in‑memory mock objects
const mockOutputs = {};
core.getInput = (name, opts) => {
  // token is required but its value is irrelevant for the mock
  return 'fake-token';
};
core.setOutput = (name, value) => {
  mockOutputs[name] = value;
};
core.info = () => {};
core.setFailed = (msg) => { throw new Error(msg); };

let createdComment = null;
github.getOctokit = () => ({
  rest: {
    issues: {
      createComment: async ({ owner, repo, issue_number, body }) => {
        createdComment = { owner, repo, issue_number, body };
        return { data: { id: 1 } };
      },
    },
  },
});

github.context = {
  repo: { owner: 'test-owner', repo: 'test-repo' },
  payload: { pull_request: { number: 42 } },
};

(async () => {
  await action.run();
  // Verify that a comment was created with the expected PR number
  if (!createdComment) {
    console.error('No comment was created');
    process.exit(1);
  }
  if (createdComment.issue_number !== 42) {
    console.error('Comment posted to wrong PR');
    process.exit(1);
  }
  // Verify that the comment contains one of the allowed emojis and the static text
  const allowedEmojis = ['🚀','✨','🔥','🌟','💥','🛸','🤖','🧩','🎉','🦄'];
  const emojiFound = allowedEmojis.some(e => createdComment.body.startsWith(e));
  if (!emojiFound) {
    console.error('Comment does not start with a valid emoji');
    process.exit(1);
  }
  if (!createdComment.body.includes('Thanks for the PR!')) {
    console.error('Comment missing expected text');
    process.exit(1);
  }
  // Verify that the action output matches the comment body
  if (mockOutputs['comment'] !== createdComment.body) {
    console.error('Action output does not match comment body');
    process.exit(1);
  }
  console.log('All tests passed');
})();
