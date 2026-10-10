const core = require('@actions/core');
const github = require('@actions/github');

// Mock the @actions/core and @actions/github modules
jest.mock('@actions/core');
jest.mock('@actions/github', () => ({
  getOctokit: jest.fn(() => ({
    rest: {
      issues: {
        createComment: jest.fn(),
      },
    },
  })),
  context: {
    repo: {
      owner: 'polsala',
      repo: 'ApocalypsAI',
    },
    payload: {
      pull_request: {
        number: 123,
        title: 'Default PR Title',
        body: 'Default PR Body with some content.',
      },
    },
  },
}));

// Mock the main script
const run = require('../src/main'); // This will execute the main.js file

describe('PR Chrono-Consistency Enforcer', () => {
  let createCommentMock;

  beforeEach(() => {
    jest.clearAllMocks();
    createCommentMock = github.getOctokit().rest.issues.createComment;

    // Reset inputs to default for each test
    core.getInput.mockImplementation((name) => {
      switch (name) {
        case 'min_title_length': return '10';
        case 'max_title_length': return '100';
        case 'min_body_length': return '20';
        case 'max_body_length': return '500';
        case 'required_keywords': return '';
        case 'disallowed_keywords': return '';
        case 'fail_on_inconsistency': return 'true';
        case 'github_token': return 'mock-token';
        default: return '';
      }
    });
  });

  // Mock rationale: We are testing the action's logic, not the GitHub API itself.
  // Mocking @actions/core and @actions/github allows us to control inputs,
  // simulate PR data, and verify outputs and API calls without network requests.

  test('should pass if PR is consistent with default rules', async () => {
    await run();
    expect(core.setFailed).not.toHaveBeenCalled();
    expect(core.setOutput).toHaveBeenCalledWith('is_chrono_consistent', true);
    expect(createCommentMock).not.toHaveBeenCalled();
  });

  test('should fail if title is too short', async () => {
    github.context.payload.pull_request.title = 'Short'; // Length 5
    await run();
    expect(core.setFailed).toHaveBeenCalledWith(expect.stringContaining('PR is not chrono-consistent'));
    expect(core.setOutput).toHaveBeenCalledWith('is_chrono_consistent', false);
    expect(createCommentMock).toHaveBeenCalledWith(expect.objectContaining({
      body: expect.stringContaining('Title is too short (5 chars). Minimum required: 10.'),
    }));
  });

  test('should fail if title is too long', async () => {
    github.context.payload.pull_request.title = 'a'.repeat(101); // Length 101
    await run();
    expect(core.setFailed).toHaveBeenCalledWith(expect.stringContaining('PR is not chrono-consistent'));
    expect(core.setOutput).toHaveBeenCalledWith('is_chrono_consistent', false);
    expect(createCommentMock).toHaveBeenCalledWith(expect.objectContaining({
      body: expect.stringContaining('Title is too long (101 chars). Maximum allowed: 100.'),
    }));
  });

  test('should fail if body is too short', async () => {
    github.context.payload.pull_request.body = 'Too short.'; // Length 10
    await run();
    expect(core.setFailed).toHaveBeenCalledWith(expect.stringContaining('PR is not chrono-consistent'));
    expect(core.setOutput).toHaveBeenCalledWith('is_chrono_consistent', false);
    expect(createCommentMock).toHaveBeenCalledWith(expect.objectContaining({
      body: expect.stringContaining('Description is too short (10 chars). Minimum required: 20.'),
    }));
  });

  test('should fail if body is too long', async () => {
    github.context.payload.pull_request.body = 'b'.repeat(501); // Length 501
    await run();
    expect(core.setFailed).toHaveBeenCalledWith(expect.stringContaining('PR is not chrono-consistent'));
    expect(core.setOutput).toHaveBeenCalledWith('is_chrono_consistent', false);
    expect(createCommentMock).toHaveBeenCalledWith(expect.objectContaining({
      body: expect.stringContaining('Description is too long (501 chars). Maximum allowed: 500.'),
    }));
  });

  test('should fail if required keyword is missing', async () => {
    core.getInput.mockImplementation((name) => {
      if (name === 'required_keywords') return 'feature,bug';
      return jest.requireActual('@actions/core').getInput(name); // Use actual for others
    });
    github.context.payload.pull_request.title = 'Update docs';
    github.context.payload.pull_request.body = 'Fix typos.';
    await run();
    expect(core.setFailed).toHaveBeenCalledWith(expect.stringContaining('PR is not chrono-consistent'));
    expect(core.setOutput).toHaveBeenCalledWith('is_chrono_consistent', false);
    expect(createCommentMock).toHaveBeenCalledWith(expect.objectContaining({
      body: expect.stringContaining('Missing required keyword: "feature" in title or description.'),
    }));
    expect(createCommentMock).toHaveBeenCalledWith(expect.objectContaining({
      body: expect.stringContaining('Missing required keyword: "bug" in title or description.'),
    }));
  });

  test('should pass if required keyword is present', async () => {
    core.getInput.mockImplementation((name) => {
      if (name === 'required_keywords') return 'feature';
      return jest.requireActual('@actions/core').getInput(name);
    });
    github.context.payload.pull_request.title = 'Add new feature';
    github.context.payload.pull_request.body = 'This is a new feature.';
    await run();
    expect(core.setFailed).not.toHaveBeenCalled();
    expect(core.setOutput).toHaveBeenCalledWith('is_chrono_consistent', true);
    expect(createCommentMock).not.toHaveBeenCalled();
  });

  test('should fail if disallowed keyword is present', async () => {
    core.getInput.mockImplementation((name) => {
      if (name === 'disallowed_keywords') return 'WIP,draft';
      return jest.requireActual('@actions/core').getInput(name);
    });
    github.context.payload.pull_request.title = 'WIP: Add new feature';
    github.context.payload.pull_request.body = 'This is a draft feature.';
    await run();
    expect(core.setFailed).toHaveBeenCalledWith(expect.stringContaining('PR is not chrono-consistent'));
    expect(core.setOutput).toHaveBeenCalledWith('is_chrono_consistent', false);
    expect(createCommentMock).toHaveBeenCalledWith(expect.objectContaining({
      body: expect.stringContaining('Contains disallowed keyword: "WIP" in title or description.'),
    }));
    expect(createCommentMock).toHaveBeenCalledWith(expect.objectContaining({
      body: expect.stringContaining('Contains disallowed keyword: "draft" in title or description.'),
    }));
  });

  test('should not fail if fail_on_inconsistency is false', async () => {
    core.getInput.mockImplementation((name) => {
      if (name === 'fail_on_inconsistency') return 'false';
      return jest.requireActual('@actions/core').getInput(name);
    });
    github.context.payload.pull_request.title = 'Short'; // Inconsistent
    await run();
    expect(core.setFailed).not.toHaveBeenCalled();
    expect(core.warning).toHaveBeenCalledWith(expect.stringContaining('PR is not chrono-consistent'));
    expect(core.setOutput).toHaveBeenCalledWith('is_chrono_consistent', false);
    expect(createCommentMock).toHaveBeenCalled();
  });

  test('should handle empty PR body gracefully', async () => {
    github.context.payload.pull_request.body = '';
    await run();
    expect(core.setFailed).toHaveBeenCalledWith(expect.stringContaining('PR is not chrono-consistent'));
    expect(core.setOutput).toHaveBeenCalledWith('is_chrono_consistent', false);
    expect(createCommentMock).toHaveBeenCalledWith(expect.objectContaining({
      body: expect.stringContaining('Description is too short (0 chars). Minimum required: 20.'),
    }));
  });

  test('should handle no pull_request payload', async () => {
    github.context.payload.pull_request = null;
    await run();
    expect(core.setFailed).toHaveBeenCalledWith('This action only runs on pull_request events.');
    expect(core.setOutput).not.toHaveBeenCalled();
    expect(createCommentMock).not.toHaveBeenCalled();
  });
});
