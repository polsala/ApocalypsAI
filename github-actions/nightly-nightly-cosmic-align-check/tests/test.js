const core = require('@actions/core');
const github = require('@actions/github');
const { when } = require('jest-when');

// Mock the @actions/core and @actions/github modules
jest.mock('@actions/core');
jest.mock('@actions/github');

describe('Nightly Cosmic Alignment Checker', () => {
  let createCommentMock;
  let listCommitsMock;

  beforeEach(() => {
    jest.clearAllMocks();

    // Mock github.getOctokit
    createCommentMock = jest.fn();
    listCommitsMock = jest.fn();

    github.getOctokit.mockReturnValue({
      rest: {
        issues: {
          createComment: createCommentMock,
        },
        pulls: {
          listCommits: listCommitsMock,
        },
      },
    });

    // Mock github.context for pull_request event
    github.context = {
      eventName: 'pull_request',
      payload: {
        pull_request: {
          number: 123,
          title: 'A regular PR title',
        },
      },
      repo: {
        owner: 'test-owner',
        repo: 'test-repo',
      },
    };

    // Mock core.getInput
    when(core.getInput)
      .calledWith('github-token', expect.any(Object))
      .thenReturn('mock-token');
    when(core.getInput)
      .calledWith('alignment-keywords')
      .thenReturn('star,galaxy,nebula');
  });

  // Mock rationale: We mock @actions/core and @actions/github to isolate the action's logic from actual GitHub API calls and environment variables. This ensures deterministic, offline testing without requiring a real GitHub context or token.

  test('should set is-aligned to true if PR title contains a keyword', async () => {
    github.context.payload.pull_request.title = 'Feature: Add a new galaxy component';
    require('../src/main'); // Load the action
    await new Promise(process.nextTick); // Allow async operations to complete

    expect(core.setOutput).toHaveBeenCalledWith('is-aligned', true);
    expect(createCommentMock).not.toHaveBeenCalled();
  });

  test('should set is-aligned to true if a commit message contains a keyword', async () => {
    github.context.payload.pull_request.title = 'Regular title';
    listCommitsMock.mockResolvedValueOnce({
      data: [
        { commit: { message: 'Fix: Some bug' } },
        { commit: { message: 'Feat: Implement a new nebula effect' } },
      ],
    });

    require('../src/main');
    await new Promise(process.nextTick);

    expect(core.setOutput).toHaveBeenCalledWith('is-aligned', true);
    expect(createCommentMock).not.toHaveBeenCalled();
  });

  test('should set is-aligned to false and post a comment if no keywords are found', async () => {
    github.context.payload.pull_request.title = 'Simple update';
    listCommitsMock.mockResolvedValueOnce({
      data: [
        { commit: { message: 'Initial commit' } },
        { commit: { message: 'Another change' } },
      ],
    });

    require('../src/main');
    await new Promise(process.nextTick);

    expect(core.setOutput).toHaveBeenCalledWith('is-aligned', false);
    expect(createCommentMock).toHaveBeenCalledWith(expect.objectContaining({
      issue_number: 123,
      body: expect.stringContaining('cosmic currents whisper')
    }));
  });

  test('should use custom alignment keywords if provided', async () => {
    when(core.getInput)
      .calledWith('alignment-keywords')
      .thenReturn('moon,sun');
    github.context.payload.pull_request.title = 'Lunar module update';

    require('../src/main');
    await new Promise(process.nextTick);

    expect(core.setOutput).toHaveBeenCalledWith('is-aligned', true);
    expect(createCommentMock).not.toHaveBeenCalled();
  });

  test('should post a comment with default keywords if alignment-keywords input is empty', async () => {
    when(core.getInput)
      .calledWith('alignment-keywords')
      .thenReturn('');
    github.context.payload.pull_request.title = 'Any title';
    listCommitsMock.mockResolvedValueOnce({
      data: [
        { commit: { message: 'Any commit' } },
      ],
    });

    require('../src/main');
    await new Promise(process.nextTick);

    expect(core.setOutput).toHaveBeenCalledWith('is-aligned', false);
    expect(createCommentMock).toHaveBeenCalledWith(expect.objectContaining({
      issue_number: 123,
      body: expect.stringContaining("'star', 'galaxy', 'nebula'")
    }));
  });

  test('should not post a comment if already aligned', async () => {
    github.context.payload.pull_request.title = 'A stellar new feature';
    require('../src/main');
    await new Promise(process.nextTick);

    expect(core.setOutput).toHaveBeenCalledWith('is-aligned', true);
    expect(createCommentMock).not.toHaveBeenCalled();
  });

  test('should warn and set is-aligned to true if not a pull_request event', async () => {
    github.context.eventName = 'push';
    require('../src/main');
    await new Promise(process.nextTick);

    expect(core.warning).toHaveBeenCalledWith('This action is intended to run on pull_request events only.');
    expect(core.setOutput).toHaveBeenCalledWith('is-aligned', true);
    expect(createCommentMock).not.toHaveBeenCalled();
  });

  test('should call setFailed on error', async () => {
    listCommitsMock.mockRejectedValueOnce(new Error('API error'));
    require('../src/main');
    await new Promise(process.nextTick);

    expect(core.setFailed).toHaveBeenCalledWith('API error');
  });
});
