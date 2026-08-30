const { expect } = require('@jest/globals');
const core = require('@actions/core');
const github = require('@actions/github');
const { when } = require('jest-when');
const { run } = require('../src/main'); // Import the run function

// Mock rationale: We need to mock GitHub Actions toolkit functions and Octokit
// to ensure tests are deterministic, offline, and don't make actual API calls.
// This allows us to control the inputs and verify the outputs/side effects.
jest.mock('@actions/core');
jest.mock('@actions/github');

describe('Nightly PR Praise Action', () => {
  let createCommentMock;

  beforeEach(() => {
    jest.clearAllMocks();

    // Mock core.getInput
    when(core.getInput)
      .calledWith('github-token', expect.any(Object))
      .mockReturnValue('mock-token');
    when(core.getInput)
      .calledWith('praise-messages')
      .mockReturnValue(''); // Default to no custom messages

    // Mock github.getOctokit
    createCommentMock = jest.fn();
    github.getOctokit.mockReturnValue({
      rest: {
        issues: {
          createComment: createCommentMock,
        },
      },
    });

    // Mock console.log for cleaner test output
    jest.spyOn(console, 'log').mockImplementation(() => {});
    jest.spyOn(core, 'info').mockImplementation(() => {});
    jest.spyOn(core, 'setFailed').mockImplementation(() => {});
  });

  afterAll(() => {
    jest.restoreAllMocks();
  });

  it('should post a praise comment when a PR is merged', async () => {
    // Mock rationale: Simulate a 'pull_request' event with 'closed' action and 'merged: true'
    github.context = {
      eventName: 'pull_request',
      payload: {
        action: 'closed',
        pull_request: {
          number: 123,
          merged: true,
        },
        repository: {
          name: 'ApocalypsAI',
          owner: { login: 'polsala' },
        },
      },
    };

    await run(); // Call the exported run function

    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(createCommentMock).toHaveBeenCalledWith(expect.objectContaining({
      owner: 'polsala',
      repo: 'ApocalypsAI',
      issue_number: 123,
      body: expect.stringContaining('ApocalypsAI Integrator Agent says:')
    }));
    expect(core.info).toHaveBeenCalledWith('Praise comment posted successfully!');
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  it('should not post a comment if the PR is not merged', async () => {
    // Mock rationale: Simulate a 'pull_request' event with 'closed' action but 'merged: false'
    github.context = {
      eventName: 'pull_request',
      payload: {
        action: 'closed',
        pull_request: {
          number: 124,
          merged: false,
        },
        repository: {
          name: 'ApocalypsAI',
          owner: { login: 'polsala' },
        },
      },
    };

    await run(); // Call the exported run function

    expect(createCommentMock).not.toHaveBeenCalled();
    expect(core.info).toHaveBeenCalledWith('This action only runs on merged pull requests. No praise needed at this time.');
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  it('should not post a comment if the event is not a pull_request', async () => {
    // Mock rationale: Simulate a 'push' event, which should be ignored by the action
    github.context = {
      eventName: 'push',
      payload: {},
    };

    await run(); // Call the exported run function

    expect(createCommentMock).not.toHaveBeenCalled();
    expect(core.info).toHaveBeenCalledWith('This action only runs on merged pull requests. No praise needed at this time.');
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  it('should use custom praise messages if provided', async () => {
    // Mock rationale: Simulate providing custom messages via input
    when(core.getInput)
      .calledWith('praise-messages')
      .mockReturnValue('Custom praise 1\nCustom praise 2');

    github.context = {
      eventName: 'pull_request',
      payload: {
        action: 'closed',
        pull_request: {
          number: 125,
          merged: true,
        },
        repository: {
          name: 'ApocalypsAI',
          owner: { login: 'polsala' },
        },
      },
    };

    await run(); // Call the exported run function

    expect(createCommentMock).toHaveBeenCalledTimes(1);
    const postedBody = createCommentMock.mock.calls[0][0].body;
    expect(postedBody).toMatch(/ApocalypsAI Integrator Agent says:/);
    expect(postedBody).toMatch(/(Custom praise 1|Custom praise 2)/);
    expect(core.info).toHaveBeenCalledWith('Using 2 custom praise messages.');
  });

  it('should fall back to default messages if custom messages input is empty after parsing', async () => {
    // Mock rationale: Simulate providing an empty or whitespace-only custom messages input
    when(core.getInput)
      .calledWith('praise-messages')
      .mockReturnValue('\n \n');

    github.context = {
      eventName: 'pull_request',
      payload: {
        action: 'closed',
        pull_request: {
          number: 126,
          merged: true,
        },
        repository: {
          name: 'ApocalypsAI',
          owner: { login: 'polsala' },
        },
      },
    };

    await run(); // Call the exported run function

    expect(createCommentMock).toHaveBeenCalledTimes(1);
    const postedBody = createCommentMock.mock.calls[0][0].body;
    expect(postedBody).toMatch(/ApocalypsAI Integrator Agent says:/);
    // Check if it contains one of the default messages (e.g., the first one)
    expect(postedBody).toMatch(/Huzzah! Another piece of the digital wasteland tamed./);
    expect(core.info).toHaveBeenCalledWith('Custom praise messages input was empty or invalid. Using default messages.');
  });

  it('should call setFailed if an error occurs', async () => {
    // Mock rationale: Simulate an error during Octokit API call
    createCommentMock.mockImplementation(() => {
      throw new Error('API error');
    });

    github.context = {
      eventName: 'pull_request',
      payload: {
        action: 'closed',
        pull_request: {
          number: 127,
          merged: true,
        },
        repository: {
          name: 'ApocalypsAI',
          owner: { login: 'polsala' },
        },
      },
    };

    await run(); // Call the exported run function

    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(core.setFailed).toHaveBeenCalledWith('API error');
  });
});
