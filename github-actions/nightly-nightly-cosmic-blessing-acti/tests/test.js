const core = require('@actions/core');
const github = require('@actions/github');
const { run } = require('../src/main');

// Mock the GitHub Actions toolkit
jest.mock('@actions/core');
jest.mock('@actions/github');

describe('Cosmic Blessing Action', () => {
  let createCommentMock;
  let getInputMock;
  let setOutputMock;
  let setFailedMock;
  let infoMock;

  beforeEach(() => {
    jest.clearAllMocks();

    // Mock core functions
    getInputMock = core.getInput.mockImplementation((name) => {
      if (name === 'token') return 'mock-token';
      if (name === 'blessings') return ''; // Default to no custom blessings
      return '';
    });
    setOutputMock = core.setOutput.mockImplementation(() => {});
    setFailedMock = core.setFailed.mockImplementation(() => {});
    infoMock = core.info.mockImplementation(() => {});

    // Mock github context and octokit
    createCommentMock = jest.fn();
    github.getOctokit.mockReturnValue({
      rest: {
        issues: {
          createComment: createCommentMock,
        },
      },
    });

    // Mock github.context
    github.context = {
      repo: {
        owner: 'test-owner',
        repo: 'test-repo',
      },
      payload: {},
      eventName: 'pull_request', // Default event
    };

    // Mock Math.random to ensure deterministic blessing selection for tests
    // Mock rationale: Math.random is non-deterministic, mocking it ensures tests are repeatable.
    jest.spyOn(Math, 'random').mockReturnValue(0.5); // Will pick the middle blessing from default or custom list
  });

  afterAll(() => {
    jest.restoreAllMocks(); // Restore Math.random to its original implementation
  });

  test('should post a default blessing to a pull request', async () => {
    github.context.payload.pull_request = { number: 123 };

    await run();

    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      issue_number: 123,
      body: expect.any(String), // The specific blessing depends on Math.random mock
    });
    expect(setOutputMock).toHaveBeenCalledWith('blessing-message', expect.any(String));
    expect(setFailedMock).not.toHaveBeenCalled();
  });

  test('should post a default blessing to an issue', async () => {
    github.context.payload.issue = { number: 456 };
    github.context.eventName = 'issues';

    await run();

    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      issue_number: 456,
      body: expect.any(String),
    });
    expect(setOutputMock).toHaveBeenCalledWith('blessing-message', expect.any(String));
    expect(setFailedMock).not.toHaveBeenCalled();
  });

  test('should use custom blessings if provided', async () => {
    getInputMock.mockImplementation((name) => {
      if (name === 'token') return 'mock-token';
      if (name === 'blessings') return 'Custom Blessing 1,Custom Blessing 2,Custom Blessing 3';
      return '';
    });
    github.context.payload.pull_request = { number: 789 };
    // With Math.random(0.5), it should pick the second custom blessing (index 1)
    // Mock rationale: Math.random is non-deterministic, mocking it ensures tests are repeatable.
    jest.spyOn(Math, 'random').mockReturnValue(0.5);

    await run();

    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      issue_number: 789,
      body: 'Custom Blessing 2',
    });
    expect(setOutputMock).toHaveBeenCalledWith('blessing-message', 'Custom Blessing 2');
  });

  test('should not post a comment if no PR or issue context', async () => {
    github.context.payload = {}; // No PR or issue
    github.context.eventName = 'push'; // A different event

    await run();

    expect(createCommentMock).not.toHaveBeenCalled();
    expect(infoMock).toHaveBeenCalledWith('Not a pull request or issue event. Skipping comment.');
    expect(setOutputMock).toHaveBeenCalledWith('blessing-message', 'No comment posted (not PR/issue event).');
    expect(setFailedMock).not.toHaveBeenCalled();
  });

  test('should call setFailed on error', async () => {
    getInputMock.mockImplementation((name) => {
      if (name === 'token') throw new Error('Token error');
      return '';
    });
    github.context.payload.pull_request = { number: 123 };

    await run();

    expect(setFailedMock).toHaveBeenCalledWith('Token error');
    expect(createCommentMock).not.toHaveBeenCalled();
  });
});
