const core = require('@actions/core');
const github = require('@actions/github');
const { when } = require('jest-when');

// Mock the @actions/core and @actions/github modules
jest.mock('@actions/core');
jest.mock('@actions/github');

describe('Nightly Victory Toast Action', () => {
  let createCommentMock;
  let setOutputMock;
  let setFailedMock;
  let infoMock;
  let originalMath;

  beforeEach(() => {
    jest.clearAllMocks();

    // Mock core functions
    setOutputMock = jest.spyOn(core, 'setOutput');
    setFailedMock = jest.spyOn(core, 'setFailed');
    infoMock = jest.spyOn(core, 'info');

    // Mock github context
    github.context = {
      repo: {
        owner: 'test-owner',
        repo: 'test-repo',
      },
      payload: {},
    };

    // Mock octokit rest client
    createCommentMock = jest.fn().mockResolvedValue({
      data: { html_url: 'https://github.com/test-owner/test-repo/issues/1/comments/1' },
    });
    github.getOctokit.mockReturnValue({
      rest: {
        issues: {
          createComment: createCommentMock,
        },
      },
    });

    // Store original Math object to restore later
    originalMath = global.Math;
  });

  afterEach(() => {
    // Restore original Math object after each test
    global.Math = originalMath;
  });

  // Mock rationale: We are testing the action's logic for processing inputs and calling the GitHub API.
  // We do not want to make actual network requests to GitHub during tests. Mocking `@actions/core`
  // allows us to control inputs and verify outputs/failures. Mocking `@actions/github` and its
  // `getOctokit` method allows us to simulate the GitHub API client and verify that `createComment`
  // is called with the correct parameters, without needing a real GitHub token or repository.
  // Mocking `Math.random` ensures deterministic selection of whimsical messages.

  test('should post a custom message to a specified PR number', async () => {
    when(core.getInput).calledWith('message').thenReturn('Custom victory message!');
    when(core.getInput).calledWith('github-token', expect.any(Object)).thenReturn('mock-token');
    when(core.getInput).calledWith('target-pr-number').thenReturn('123');
    when(core.getInput).calledWith('target-issue-number').thenReturn('');

    // Dynamically import the main script after mocks are set up
    const main = require('../src/main');
    await main.run(); // Call the run function directly

    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      issue_number: 123,
      body: '🎉 **Victory Toast!** 🎉\n\nCustom victory message!',
    });
    expect(setOutputMock).toHaveBeenCalledWith('comment-url', 'https://github.com/test-owner/test-repo/issues/1/comments/1');
    expect(setFailedMock).not.toHaveBeenCalled();
  });

  test('should post a random message to a PR from context', async () => {
    when(core.getInput).calledWith('message').thenReturn('');
    when(core.getInput).calledWith('github-token', expect.any(Object)).thenReturn('mock-token');
    when(core.getInput).calledWith('target-pr-number').thenReturn('');
    when(core.getInput).calledWith('target-issue-number').thenReturn('');

    github.context.payload.pull_request = { number: 456 };

    // Mock Math.random to ensure deterministic message selection (index 5)
    global.Math = {
      ...originalMath,
      random: () => 0.5
    };

    const main = require('../src/main');
    await main.run();

    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(createCommentMock.mock.calls[0][0].issue_number).toBe(456);
    expect(createCommentMock.mock.calls[0][0].body).toBe('🎉 **Victory Toast!** 🎉\n\nThe void whispers approval. Or maybe that\'s just the server fan.');
    expect(setOutputMock).toHaveBeenCalledWith('comment-url', 'https://github.com/test-owner/test-repo/issues/1/comments/1');
    expect(setFailedMock).not.toHaveBeenCalled();
  });

  test('should post a random message to a specified Issue number', async () => {
    when(core.getInput).calledWith('message').thenReturn('');
    when(core.getInput).calledWith('github-token', expect.any(Object)).thenReturn('mock-token');
    when(core.getInput).calledWith('target-pr-number').thenReturn('');
    when(core.getInput).calledWith('target-issue-number').thenReturn('789');

    // Mock Math.random to ensure deterministic message selection (index 1)
    global.Math = {
      ...originalMath,
      random: () => 0.1
    };

    const main = require('../src/main');
    await main.run();

    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(createCommentMock.mock.calls[0][0].issue_number).toBe(789);
    expect(createCommentMock.mock.calls[0][0].body).toBe('🎉 **Victory Toast!** 🎉\n\nDust settles, code runs. Another day, another triumph!');
    expect(setOutputMock).toHaveBeenCalledWith('comment-url', 'https://github.com/test-owner/test-repo/issues/1/comments/1');
    expect(setFailedMock).not.toHaveBeenCalled();
  });

  test('should log message if no target PR/Issue is found', async () => {
    when(core.getInput).calledWith('message').thenReturn('No target here!');
    when(core.getInput).calledWith('github-token', expect.any(Object)).thenReturn('mock-token');
    when(core.getInput).calledWith('target-pr-number').thenReturn('');
    when(core.getInput).calledWith('target-issue-number').thenReturn('');

    github.context.payload = {}; // No PR or Issue in context

    const main = require('../src/main');
    await main.run();

    expect(createCommentMock).not.toHaveBeenCalled();
    expect(setOutputMock).not.toHaveBeenCalled();
    expect(setFailedMock).not.toHaveBeenCalled();
    expect(infoMock).toHaveBeenCalledWith('No target PR or Issue found in context or inputs. Logging victory message instead of commenting.');
    expect(infoMock).toHaveBeenCalledWith('Victory Message: No target here!');
  });

  test('should fail if github-token is not provided', async () => {
    when(core.getInput).calledWith('message').thenReturn('Custom message');
    when(core.getInput).calledWith('github-token', expect.any(Object)).thenReturn(''); // Missing token
    when(core.getInput).calledWith('target-pr-number').thenReturn('123');
    when(core.getInput).calledWith('target-issue-number').thenReturn('');

    const main = require('../src/main');
    await main.run();

    expect(setFailedMock).toHaveBeenCalledWith('Input required and not supplied: github-token');
    expect(createCommentMock).not.toHaveBeenCalled();
    expect(setOutputMock).not.toHaveBeenCalled();
  });

  test('should fail if target-pr-number is invalid', async () => {
    when(core.getInput).calledWith('message').thenReturn('Custom message');
    when(core.getInput).calledWith('github-token', expect.any(Object)).thenReturn('mock-token');
    when(core.getInput).calledWith('target-pr-number').thenReturn('not-a-number');
    when(core.getInput).calledWith('target-issue-number').thenReturn('');

    const main = require('../src/main');
    await main.run();

    expect(setFailedMock).toHaveBeenCalledWith('Invalid \'target-pr-number\': not-a-number');
    expect(createCommentMock).not.toHaveBeenCalled();
    expect(setOutputMock).not.toHaveBeenCalled();
  });

  test('should fail if target-issue-number is invalid', async () => {
    when(core.getInput).calledWith('message').thenReturn('Custom message');
    when(core.getInput).calledWith('github-token', expect.any(Object)).thenReturn('mock-token');
    when(core.getInput).calledWith('target-pr-number').thenReturn('');
    when(core.getInput).calledWith('target-issue-number').thenReturn('not-a-number');

    const main = require('../src/main');
    await main.run();

    expect(setFailedMock).toHaveBeenCalledWith('Invalid \'target-issue-number\': not-a-number');
    expect(createCommentMock).not.toHaveBeenCalled();
    expect(setOutputMock).not.toHaveBeenCalled();
  });

  test('should prioritize target-issue-number over target-pr-number', async () => {
    when(core.getInput).calledWith('message').thenReturn('Issue priority test');
    when(core.getInput).calledWith('github-token', expect.any(Object)).thenReturn('mock-token');
    when(core.getInput).calledWith('target-pr-number').thenReturn('100');
    when(core.getInput).calledWith('target-issue-number').thenReturn('200');

    const main = require('../src/main');
    await main.run();

    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      issue_number: 200,
      body: '🎉 **Victory Toast!** 🎉\n\nIssue priority test',
    });
    expect(setOutputMock).toHaveBeenCalledWith('comment-url', 'https://github.com/test-owner/test-repo/issues/1/comments/1');
    expect(setFailedMock).not.toHaveBeenCalled();
  });

  test('should prioritize target-pr-number over context PR', async () => {
    when(core.getInput).calledWith('message').thenReturn('PR priority test');
    when(core.getInput).calledWith('github-token', expect.any(Object)).thenReturn('mock-token');
    when(core.getInput).calledWith('target-pr-number').thenReturn('300');
    when(core.getInput).calledWith('target-issue-number').thenReturn('');

    github.context.payload.pull_request = { number: 400 }; // Context PR exists

    const main = require('../src/main');
    await main.run();

    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      issue_number: 300,
      body: '🎉 **Victory Toast!** 🎉\n\nPR priority test',
    });
    expect(setOutputMock).toHaveBeenCalledWith('comment-url', 'https://github.com/test-owner/test-repo/issues/1/comments/1');
    expect(setFailedMock).not.toHaveBeenCalled();
  });
});
