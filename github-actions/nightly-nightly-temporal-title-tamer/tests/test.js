const core = require('@actions/core');
const github = require('@actions/github');
const { run } = require('../src/main');

// Mock the GitHub Actions toolkit
jest.mock('@actions/core');
jest.mock('@actions/github');

describe('Temporal Title Tamer', () => {
  let createCommentMock;

  beforeEach(() => {
    jest.clearAllMocks();

    // Mock core inputs
    core.getInput.mockImplementation((name) => {
      switch (name) {
        case 'github-token': return 'mock-token';
        case 'anomaly-keywords': return 'time,future,past,paradox';
        case 'comment-template': return 'Anomaly: {title}';
        default: return '';
      }
    });

    // Mock github context
    github.context = {
      payload: {
        pull_request: {
          number: 123,
          title: 'Fixing a bug from the future',
        },
      },
      repo: {
        owner: 'polsala',
        repo: 'ApocalypsAI',
      },
    };

    // Mock octokit
    createCommentMock = jest.fn();
    github.getOctokit.mockReturnValue({
      rest: {
        issues: {
          createComment: createCommentMock,
        },
      },
    });
  });

  test('should detect anomaly and post comment', async () => {
    // Mock rationale: Simulating a PR title with an anomaly keyword.
    github.context.payload.pull_request.title = 'Fixing a bug from the future';

    await run();

    expect(core.setOutput).toHaveBeenCalledWith('anomaly-detected', true);
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'polsala',
      repo: 'ApocalypsAI',
      issue_number: 123,
      body: 'Anomaly: Fixing a bug from the future',
    });
    expect(core.warning).toHaveBeenCalledWith(expect.stringContaining('Temporal anomaly detected'));
  });

  test('should not detect anomaly and not post comment', async () => {
    // Mock rationale: Simulating a PR title without any anomaly keywords.
    github.context.payload.pull_request.title = 'Refactor user authentication';

    await run();

    expect(core.setOutput).toHaveBeenCalledWith('anomaly-detected', false);
    expect(createCommentMock).not.toHaveBeenCalled();
    expect(core.info).toHaveBeenCalledWith('No temporal anomalies detected. All clear for spacetime stability!');
  });

  test('should handle custom keywords', async () => {
    // Mock rationale: Simulating custom anomaly keywords provided by the user.
    core.getInput.mockImplementation((name) => {
      if (name === 'anomaly-keywords') return 'warp,dimension';
      if (name === 'github-token') return 'mock-token';
      if (name === 'comment-template') return 'Anomaly: {title}';
      return '';
    });
    github.context.payload.pull_request.title = 'Warp core stabilization';

    await run();

    expect(core.setOutput).toHaveBeenCalledWith('anomaly-detected', true);
    expect(createCommentMock).toHaveBeenCalled();
  });

  test('should not run if not a pull_request event', async () => {
    // Mock rationale: Simulating a non-pull_request event (e.g., push, issue_comment).
    github.context.payload.pull_request = undefined;

    await run();

    expect(core.info).toHaveBeenCalledWith('This action only runs on pull_request events. Skipping.');
    expect(core.setOutput).toHaveBeenCalledWith('anomaly-detected', false);
    expect(createCommentMock).not.toHaveBeenCalled();
  });

  test('should handle empty keywords gracefully', async () => {
    // Mock rationale: Simulating an empty anomaly-keywords input.
    core.getInput.mockImplementation((name) => {
      if (name === 'anomaly-keywords') return '';
      if (name === 'github-token') return 'mock-token';
      if (name === 'comment-template') return 'Anomaly: {title}';
      return '';
    });
    github.context.payload.pull_request.title = 'A normal title';

    await run();

    expect(core.setOutput).toHaveBeenCalledWith('anomaly-detected', false);
    expect(createCommentMock).not.toHaveBeenCalled();
  });

  test('should handle errors', async () => {
    // Mock rationale: Simulating an error during execution, e.g., invalid token or API issue.
    github.getOctokit.mockImplementation(() => {
      throw new Error('API rate limit exceeded');
    });

    await run();

    expect(core.setFailed).toHaveBeenCalledWith('API rate limit exceeded');
  });
});
