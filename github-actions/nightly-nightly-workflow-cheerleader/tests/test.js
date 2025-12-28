const core = require('@actions/core');
const github = require('@actions/github');
const { when } = require('jest-when');

// Mock the GitHub Actions toolkit
jest.mock('@actions/core');
jest.mock('@actions/github');

const run = require('../src/main'); // The action's main script

describe('Nightly Workflow Cheerleader', () => {
  let createCommentMock;

  beforeEach(() => {
    jest.clearAllMocks();

    // Mock core.getInput
    when(core.getInput)
      .calledWith('token', expect.any(Object))
      .mockReturnValue('mock-token');
    when(core.getInput)
      .calledWith('message')
      .mockReturnValue(''); // Default to no custom message
    when(core.getInput)
      .calledWith('issue-number')
      .mockReturnValue(''); // Default to no explicit issue number

    // Mock github.context
    github.context = {
      repo: {
        owner: 'polsala',
        repo: 'ApocalypsAI',
      },
      payload: {}, // Reset payload for each test
      eventName: 'push', // Default event name
    };

    // Mock octokit.rest.issues.createComment
    createCommentMock = jest.fn().mockResolvedValue({
      data: { html_url: 'https://github.com/comment/123' }
    });
    github.getOctokit.mockReturnValue({
      rest: {
        issues: {
          createComment: createCommentMock,
        },
      },
    });
  });

  test('should post a random cheer message on a pull request', async () => {
    // Mock rationale: Simulating a pull_request event context for the action.
    github.context.payload.pull_request = { number: 123 };

    await run();

    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'polsala',
      repo: 'ApocalypsAI',
      issue_number: 123,
      body: expect.stringContaining('✨ **Workflow Cheerleader says:** ✨\n\n'),
    });
    expect(core.setOutput).toHaveBeenCalledWith('comment-url', 'https://github.com/comment/123');
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Comment posted: https://github.com/comment/123'));
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should post a custom cheer message on an issue', async () => {
    // Mock rationale: Simulating an issue event context with a custom message.
    github.context.payload.issue = { number: 456 };
    when(core.getInput)
      .calledWith('message')
      .mockReturnValue('Custom cheer for a job well done!');

    await run();

    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'polsala',
      repo: 'ApocalypsAI',
      issue_number: 456,
      body: '✨ **Workflow Cheerleader says:** ✨\n\nCustom cheer for a job well done!',
    });
    expect(core.setOutput).toHaveBeenCalledWith('comment-url', 'https://github.com/comment/123');
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should use explicit issue-number input if provided', async () => {
    // Mock rationale: Testing the precedence of the 'issue-number' input over context.
    github.context.payload.pull_request = { number: 789 }; // Context PR number
    when(core.getInput)
      .calledWith('issue-number')
      .mockReturnValue('101'); // Explicit issue number

    await run();

    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'polsala',
      repo: 'ApocalypsAI',
      issue_number: 101, // Should use 101, not 789
      body: expect.stringContaining('✨ **Workflow Cheerleader says:** ✨\n\n'),
    });
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should warn and not post if no issue/PR number can be determined', async () => {
    // Mock rationale: Simulating a context where no PR or issue is available.
    github.context.payload = {}; // No PR or issue in payload
    when(core.getInput)
      .calledWith('issue-number')
      .mockReturnValue(''); // No explicit issue number

    await run();

    expect(createCommentMock).not.toHaveBeenCalled();
    expect(core.warning).toHaveBeenCalledWith('Could not determine an issue or pull request number to comment on. Skipping comment.');
    expect(core.setOutput).not.toHaveBeenCalled();
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should handle API errors gracefully', async () => {
    // Mock rationale: Simulating an API error during comment creation.
    github.context.payload.pull_request = { number: 123 };
    const errorMessage = 'API rate limit exceeded';
    createCommentMock.mockRejectedValue(new Error(errorMessage));

    await run();

    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(core.setFailed).toHaveBeenCalledWith(errorMessage);
    expect(core.setOutput).not.toHaveBeenCalled();
  });

  test('should not post if issue-number is invalid (e.g., 0)', async () => {
    // Mock rationale: Testing invalid issue-number input.
    when(core.getInput)
      .calledWith('issue-number')
      .mockReturnValue('0');

    await run();

    expect(createCommentMock).not.toHaveBeenCalled();
    expect(core.warning).toHaveBeenCalledWith('Could not determine an issue or pull request number to comment on. Skipping comment.');
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should not post if issue-number is invalid (e.g., non-numeric)', async () => {
    // Mock rationale: Testing invalid issue-number input.
    when(core.getInput)
      .calledWith('issue-number')
      .mockReturnValue('not-a-number');

    await run();

    expect(createCommentMock).not.toHaveBeenCalled();
    expect(core.warning).toHaveBeenCalledWith('Could not determine an issue or pull request number to comment on. Skipping comment.');
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should log a warning for workflow_run context without direct PR/Issue', async () => {
    // Mock rationale: Simulating a workflow_run event without a direct PR/Issue payload.
    github.context.payload.workflow_run = { id: 12345 };
    github.context.eventName = 'workflow_run';

    await run();

    expect(createCommentMock).not.toHaveBeenCalled();
    expect(core.warning).toHaveBeenCalledWith('No direct pull request or issue found in workflow_run context. Skipping comment.');
    expect(core.setFailed).not.toHaveBeenCalled();
  });
});
