const core = require('@actions/core');
const github = require('@actions/github');
const { when } = require('jest-when');

// Mock the GitHub Actions toolkit
jest.mock('@actions/core');
jest.mock('@actions/github');

describe('Nightly Whimsical Encouragement Action', () => {
  let createCommentMock;
  let getInputMock;
  let setOutputMock;
  let setFailedMock;
  let infoMock;

  beforeEach(() => {
    jest.clearAllMocks();

    // Mock core.getInput
    getInputMock = core.getInput;
    when(getInputMock).calledWith('github-token', expect.anything()).mockReturnValue('mock-token');
    when(getInputMock).calledWith('label-to-trigger', expect.anything()).mockReturnValue('needs-cheering');
    when(getInputMock).calledWith('messages', expect.anything()).mockReturnValue(JSON.stringify([
      "Message 1: You're doing great!",
      "Message 2: Keep up the fantastic work!",
      "Message 3: Your efforts are truly inspiring!"
    ]));

    // Mock core.setOutput and core.setFailed
    setOutputMock = core.setOutput;
    setFailedMock = core.setFailed;
    infoMock = core.info;

    // Mock github.getOctokit().rest.issues.createComment
    createCommentMock = jest.fn().mockResolvedValue({ data: { id: 123, html_url: 'http://mock.url/comment/123' } });
    github.getOctokit.mockReturnValue({
      rest: {
        issues: {
          createComment: createCommentMock
        }
      }
    });

    // Mock Math.random to ensure deterministic message selection
    // Mock rationale: Math.random is non-deterministic. Mocking it ensures tests always pick the same message for predictable assertions.
    jest.spyOn(Math, 'random').mockReturnValue(0.5); // Will pick the middle message (index 1)
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  it('should post a comment on a PR with the trigger label', async () => {
    // Mock rationale: github.context is an external dependency representing the GitHub event payload. Mocking it allows simulating different event types and payloads offline.
    github.context = {
      eventName: 'pull_request',
      payload: {
        pull_request: {
          number: 1,
          labels: [{ name: 'needs-cheering' }, { name: 'bug' }]
        }
      },
      repo: { owner: 'test-owner', repo: 'test-repo' }
    };

    // Import the action's main logic after mocks are set up
    const main = require('../src/main');
    await main.run();

    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      issue_number: 1,
      body: 'Message 2: Keep up the fantastic work!' // Based on Math.random(0.5) and 3 messages
    });
    expect(setOutputMock).toHaveBeenCalledWith('comment-id', 123);
    expect(setFailedMock).not.toHaveBeenCalled();
    expect(infoMock).toHaveBeenCalledWith("Processing Pull Request #1");
    expect(infoMock).toHaveBeenCalledWith("Label 'needs-cheering' found. Posting whimsical encouragement.");
  });

  it('should post a comment on an issue with the trigger label', async () => {
    // Mock rationale: github.context is an external dependency representing the GitHub event payload. Mocking it allows simulating different event types and payloads offline.
    github.context = {
      eventName: 'issues',
      payload: {
        issue: {
          number: 5,
          labels: [{ name: 'feature' }, { name: 'needs-cheering' }]
        }
      },
      repo: { owner: 'test-owner', repo: 'test-repo' }
    };

    const main = require('../src/main');
    await main.run();

    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      issue_number: 5,
      body: 'Message 2: Keep up the fantastic work!'
    });
    expect(setOutputMock).toHaveBeenCalledWith('comment-id', 123);
    expect(setFailedMock).not.toHaveBeenCalled();
    expect(infoMock).toHaveBeenCalledWith("Processing Issue #5");
    expect(infoMock).toHaveBeenCalledWith("Label 'needs-cheering' found. Posting whimsical encouragement.");
  });

  it('should not post a comment if the PR does not have the trigger label', async () => {
    // Mock rationale: github.context is an external dependency representing the GitHub event payload. Mocking it allows simulating different event types and payloads offline.
    github.context = {
      eventName: 'pull_request',
      payload: {
        pull_request: {
          number: 2,
          labels: [{ name: 'bug' }]
        }
      },
      repo: { owner: 'test-owner', repo: 'test-repo' }
    };

    const main = require('../src/main');
    await main.run();

    expect(createCommentMock).not.toHaveBeenCalled();
    expect(setOutputMock).not.toHaveBeenCalled();
    expect(setFailedMock).not.toHaveBeenCalled();
    expect(infoMock).toHaveBeenCalledWith("Processing Pull Request #2");
    expect(infoMock).toHaveBeenCalledWith("Label 'needs-cheering' not found on #2. Skipping.");
  });

  it('should not post a comment if the issue does not have the trigger label', async () => {
    // Mock rationale: github.context is an external dependency representing the GitHub event payload. Mocking it allows simulating different event types and payloads offline.
    github.context = {
      eventName: 'issues',
      payload: {
        issue: {
          number: 6,
          labels: [{ name: 'enhancement' }]
        }
      },
      repo: { owner: 'test-owner', repo: 'test-repo' }
    };

    const main = require('../src/main');
    await main.run();

    expect(createCommentMock).not.toHaveBeenCalled();
    expect(setOutputMock).not.toHaveBeenCalled();
    expect(setFailedMock).not.toHaveBeenCalled();
    expect(infoMock).toHaveBeenCalledWith("Processing Issue #6");
    expect(infoMock).toHaveBeenCalledWith("Label 'needs-cheering' not found on #6. Skipping.");
  });

  it('should handle missing issue/PR number gracefully', async () => {
    // Mock rationale: github.context is an external dependency representing the GitHub event payload. Mocking it allows simulating different event types and payloads offline.
    github.context = {
      eventName: 'pull_request',
      payload: {},
      repo: { owner: 'test-owner', repo: 'test-repo' }
    };

    const main = require('../src/main');
    await main.run();

    expect(createCommentMock).not.toHaveBeenCalled();
    expect(setOutputMock).not.toHaveBeenCalled();
    expect(setFailedMock).not.toHaveBeenCalled();
    expect(infoMock).toHaveBeenCalledWith('Could not determine issue or pull request number. Skipping.');
  });

  it('should set action as failed on error', async () => {
    // Mock rationale: github.context is an external dependency representing the GitHub event payload. Mocking it allows simulating different event types and payloads offline.
    github.context = {
      eventName: 'pull_request',
      payload: {
        pull_request: {
          number: 3,
          labels: [{ name: 'needs-cheering' }]
        }
      },
      repo: { owner: 'test-owner', repo: 'test-repo' }
    };
    createCommentMock.mockRejectedValue(new Error('API Error'));

    const main = require('../src/main');
    await main.run();

    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(setFailedMock).toHaveBeenCalledWith('API Error');
  });

  it('should not run if event is not pull_request or issues', async () => {
    // Mock rationale: github.context is an external dependency representing the GitHub event payload. Mocking it allows simulating different event types and payloads offline.
    github.context = {
      eventName: 'push',
      payload: {},
      repo: { owner: 'test-owner', repo: 'test-repo' }
    };

    const main = require('../src/main');
    await main.run();

    expect(createCommentMock).not.toHaveBeenCalled();
    expect(setOutputMock).not.toHaveBeenCalled();
    expect(setFailedMock).not.toHaveBeenCalled();
    expect(infoMock).toHaveBeenCalledWith('Not a pull_request or issues event, or payload is missing. Skipping.');
  });
});
