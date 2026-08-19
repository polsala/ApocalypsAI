const { generateWhimsicalMessage, run } = require('../src/index');
const core = require('@actions/core');
const github = require('@actions/github');

// Mock the GitHub Actions toolkit
jest.mock('@actions/core');
jest.mock('@actions/github');

describe('generateWhimsicalMessage', () => {
  test('should return a success message for "success" conclusion', () => {
    const message = generateWhimsicalMessage('success');
    expect(message).toMatch(/Huzzah!|Victory!|A flawless execution!|Success!|Behold, a triumph!/);
  });

  test('should return a failure message for "failure" conclusion', () => {
    const message = generateWhimsicalMessage('failure');
    expect(message).toMatch(/Oh dear,|Alas,|A momentary lapse|The digital gremlins|Worry not,/);
  });

  test('should return a cancelled message for "cancelled" conclusion', () => {
    const message = generateWhimsicalMessage('cancelled');
    expect(message).toMatch(/strategic retreat!|cosmic winds shifted!|Interrupted by the whispers|moment of reflection!|journey was cut short,/);
  });

  test('should return a default message for unknown conclusion', () => {
    const message = generateWhimsicalMessage('unknown');
    expect(message).toBe("The workflow concluded with 'unknown'. The universe offers its neutral observation.");
  });
});

describe('run', () => {
  let createCommentMock;

  beforeEach(() => {
    // Mock rationale: We need to mock @actions/core and @actions/github to prevent actual API calls
    // and to control inputs/outputs for deterministic testing.
    core.getInput.mockImplementation((name) => {
      if (name === 'github-token') return 'mock-token';
      if (name === 'workflow-conclusion') return 'success';
      if (name === 'pr-number') return '123';
      return '';
    });
    core.setOutput.mockImplementation(jest.fn());
    core.setFailed.mockImplementation(jest.fn());
    core.info.mockImplementation(jest.fn());

    createCommentMock = jest.fn().mockResolvedValue({ data: { id: 456, html_url: 'mock-url' } });
    github.getOctokit.mockReturnValue({
      rest: {
        issues: {
          createComment: createCommentMock,
        },
      },
    });
    github.context = {
      repo: {
        owner: 'polsala',
        repo: 'ApocalypsAI',
      },
    };
  });

  afterEach(() => {
    jest.clearAllMocks();
  });

  test('should post a comment if pr-number is provided', async () => {
    await run();

    expect(core.getInput).toHaveBeenCalledWith('github-token', { required: true });
    expect(core.getInput).toHaveBeenCalledWith('workflow-conclusion', { required: true });
    expect(core.getInput).toHaveBeenCalledWith('pr-number');
    expect(core.setOutput).toHaveBeenCalledWith('whimsical-message', expect.any(String));
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'polsala',
      repo: 'ApocalypsAI',
      issue_number: '123',
      body: expect.stringContaining('### Nightly Workflow Whimsy Agent Says:\n\n'),
    });
    expect(core.setOutput).toHaveBeenCalledWith('comment-id', 456);
    expect(core.info).toHaveBeenCalledWith('Comment posted: mock-url');
  });

  test('should not post a comment if pr-number is not provided', async () => {
    core.getInput.mockImplementation((name) => {
      if (name === 'github-token') return 'mock-token';
      if (name === 'workflow-conclusion') return 'failure';
      if (name === 'pr-number') return ''; // No PR number
      return '';
    });

    await run();

    expect(createCommentMock).not.toHaveBeenCalled();
    expect(core.info).toHaveBeenCalledWith('No PR number provided. Skipping comment posting.');
    expect(core.setOutput).toHaveBeenCalledWith('whimsical-message', expect.any(String));
    expect(core.setOutput).not.toHaveBeenCalledWith('comment-id', expect.any(Number));
  });

  test('should call setFailed on error', async () => {
    core.getInput.mockImplementation(() => {
      throw new Error('Test error');
    });

    await run();

    expect(core.setFailed).toHaveBeenCalledWith('Test error');
  });
});
