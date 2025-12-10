const core = require('@actions/core');
const github = require('@actions/github');
const { when } = require('jest-when'); // For more flexible mocking

// Mock the GitHub Actions toolkit
jest.mock('@actions/core');
jest.mock('@actions/github');

// Mock the Octokit client
const mockCreateComment = jest.fn();
const mockOctokit = {
  rest: {
    issues: {
      createComment: mockCreateComment,
    },
  },
};

// Mock github.getOctokit to return our mock client
when(github.getOctokit).calledWith(expect.any(String)).mockReturnValue(mockOctokit);

// Mock github.context for pull request payload
const mockContext = {
  repo: {
    owner: 'test-owner',
    repo: 'test-repo',
  },
  payload: {
    pull_request: {
      number: 123,
      body: 'This is a test PR description.',
    },
  },
};
github.context = mockContext;

// Import the main action logic
const run = require('../src/main');

describe('Nightly PR Apoc Advisor', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    // Reset inputs for each test
    core.getInput.mockImplementation((name) => {
      if (name === 'github-token') return 'mock-token';
      if (name === 'wisdom-keyword') return 'survival tip'; // Default
      return '';
    });
  });

  test('should post a comment if no wisdom keyword is found', async () => {
    // Mock rationale: Simulating a PR description without the keyword.
    github.context.payload.pull_request.body = 'This PR fixes a bug.';
    mockCreateComment.mockResolvedValueOnce({ data: { id: 456 } }); // Mock rationale: Simulating a successful API call to create a comment.

    await run();

    expect(core.getInput).toHaveBeenCalledWith('github-token', { required: true });
    expect(core.getInput).toHaveBeenCalledWith('wisdom-keyword');
    expect(mockCreateComment).toHaveBeenCalledTimes(1);
    expect(mockCreateComment).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      issue_number: 123,
      body: expect.stringContaining('Apocalyptic Wisdom Advisory'),
    });
    expect(core.setOutput).toHaveBeenCalledWith('comment-id', 456);
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Posted apocalyptic wisdom to PR #123. Comment ID: 456'));
  });

  test('should not post a comment if wisdom keyword is found (case-insensitive)', async () => {
    // Mock rationale: Simulating a PR description that already contains the keyword.
    github.context.payload.pull_request.body = 'This PR includes a SURVIVAL TIP for the ages.';

    await run();

    expect(core.getInput).toHaveBeenCalledWith('github-token', { required: true });
    expect(core.getInput).toHaveBeenCalledWith('wisdom-keyword');
    expect(mockCreateComment).not.toHaveBeenCalled();
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('PR #123 already contains the keyword "survival tip". No advice needed.'));
  });

  test('should use a custom wisdom keyword', async () => {
    // Mock rationale: Simulating a custom keyword input.
    core.getInput.mockImplementation((name) => {
      if (name === 'github-token') return 'mock-token';
      if (name === 'wisdom-keyword') return 'apocalyptic insight';
      return '';
    });
    github.context.payload.pull_request.body = 'This PR is great.';
    mockCreateComment.mockResolvedValueOnce({ data: { id: 789 } }); // Mock rationale: Simulating a successful API call.

    await run();

    expect(core.getInput).toHaveBeenCalledWith('wisdom-keyword');
    expect(mockCreateComment).toHaveBeenCalledTimes(1);
    expect(mockCreateComment).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      issue_number: 123,
      body: expect.stringContaining('Consider adding your own **apocalyptic insight** to the PR description next time!'),
    });
  });

  test('should handle empty PR body gracefully', async () => {
    // Mock rationale: Simulating a PR with an empty description.
    github.context.payload.pull_request.body = null;
    mockCreateComment.mockResolvedValueOnce({ data: { id: 101 } }); // Mock rationale: Simulating a successful API call.

    await run();

    expect(mockCreateComment).toHaveBeenCalledTimes(1);
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Posted apocalyptic wisdom to PR #123. Comment ID: 101'));
  });

  test('should set failed status on error', async () => {
    // Mock rationale: Simulating an error during API call.
    github.context.payload.pull_request.body = 'No wisdom here.';
    const errorMessage = 'API error';
    mockCreateComment.mockRejectedValueOnce(new Error(errorMessage)); // Mock rationale: Simulating an API error.

    await run();

    expect(mockCreateComment).toHaveBeenCalledTimes(1);
    expect(core.setFailed).toHaveBeenCalledWith(errorMessage);
  });

  test('should warn and skip if not a pull_request event', async () => {
    // Mock rationale: Simulating a workflow run not triggered by a pull_request.
    github.context.payload.pull_request = undefined;

    await run();

    expect(core.warning).toHaveBeenCalledWith('This action only runs on pull_request events. Skipping.');
    expect(mockCreateComment).not.toHaveBeenCalled();
  });
});
