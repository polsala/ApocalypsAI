const core = require('@actions/core');
const github = require('@actions/github');
const fs = require('fs');

// Mock the GitHub Actions toolkit
jest.mock('@actions/core');
jest.mock('@actions/github');
jest.mock('fs');

// Import the main script to be tested
const run = require('../src/main');

describe('Nightly PR Cheerleader Action', () => {
  let createCommentMock;

  beforeEach(() => {
    jest.clearAllMocks();

    // Mock rationale: core.getInput is an external dependency, mocking it ensures tests are offline and deterministic.
    core.getInput.mockImplementation((name) => {
      switch (name) {
        case 'github-token': return 'mock-token';
        case 'reaction-emojis': return '+1,sparkles,tada';
        case 'affirmations-file': return ''; // Default to no custom file
        default: return '';
      }
    });
    core.info.mockImplementation(console.log);
    core.warning.mockImplementation(console.warn);
    core.setFailed.mockImplementation(console.error);

    // Mock rationale: github.getOctokit().rest.issues.createComment is an external API call, mocking it ensures tests are offline and deterministic.
    createCommentMock = jest.fn().mockResolvedValue({ data: { id: 12345 } });
    github.getOctokit.mockReturnValue({
      rest: {
        issues: {
          createComment: createCommentMock,
        },
      },
    });

    // Mock github.context
    // Mock rationale: github.context is an external dependency, mocking it ensures tests are offline and deterministic.
    github.context = {
      repo: {
        owner: 'polsala',
        repo: 'ApocalypsAI',
      },
      eventName: 'issue_comment',
      payload: {
        action: 'reacted',
        issue: { number: 1 },
        comment: { id: 101, body: 'Great suggestion!' },
        reaction: { content: 'sparkles' },
      },
    };

    // Mock rationale: Math.random is non-deterministic, mocking it ensures tests are repeatable.
    jest.spyOn(Math, 'random').mockReturnValue(0.5); // Will pick the 5th affirmation (index 4) from default list
  });

  afterAll(() => {
    jest.restoreAllMocks();
  });

  test('should post a cheer comment for a valid reaction on an issue comment', async () => {
    await run();

    expect(core.getInput).toHaveBeenCalledWith('github-token', { required: true });
    expect(core.getInput).toHaveBeenCalledWith('reaction-emojis');
    expect(core.getInput).toHaveBeenCalledWith('affirmations-file');
    expect(github.getOctokit).toHaveBeenCalledWith('mock-token');
    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'polsala',
      repo: 'ApocalypsAI',
      issue_number: 1,
      body: expect.stringContaining('This is truly apocalyptic-ally awesome!'),
    });
    expect(core.setOutput).toHaveBeenCalledWith('comment-id', 12345);
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Successfully posted comment ID: 12345'));
  });

  test('should post a cheer comment for a valid reaction on a PR review comment', async () => {
    github.context.eventName = 'pull_request_review_comment';
    github.context.payload = {
      action: 'reacted',
      pull_request: { number: 5 },
      comment: { id: 202, body: 'Looks good to me!' },
      reaction: { content: 'tada' },
    };
    jest.spyOn(Math, 'random').mockReturnValue(0.1); // Pick a different affirmation

    await run();

    expect(createCommentMock).toHaveBeenCalledTimes(1);
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'polsala',
      repo: 'ApocalypsAI',
      issue_number: 5,
      body: expect.stringContaining("You're a star! Keep shining!"), // First affirmation
    });
    expect(core.setOutput).toHaveBeenCalledWith('comment-id', 12345);
  });

  test('should not post a comment for an unsupported event type', async () => {
    github.context.eventName = 'push';
    github.context.payload = { action: 'created' }; // No reaction payload
    await run();

    expect(createCommentMock).not.toHaveBeenCalled();
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining("Event 'push' with action 'created' is not a supported reaction event. Skipping."));
    expect(core.setOutput).not.toHaveBeenCalled();
  });

  test('should not post a comment for an unsupported reaction content', async () => {
    github.context.payload.reaction.content = 'laugh'; // Not in '+1,sparkles,tada'
    await run();

    expect(createCommentMock).not.toHaveBeenCalled();
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining("Reaction 'laugh' is not in the allowed list: +1,sparkles,tada. Skipping."));
    expect(core.setOutput).not.toHaveBeenCalled();
  });

  test('should handle custom affirmations file successfully', async () => {
    core.getInput.mockImplementation((name) => {
      if (name === 'affirmations-file') return 'tests/affirmations.txt';
      if (name === 'github-token') return 'mock-token';
      if (name === 'reaction-emojis') return 'sparkles';
      return '';
    });

    // Mock rationale: fs.readFileSync is an external dependency, mocking it ensures tests are offline and deterministic.
    fs.readFileSync.mockReturnValue('Custom affirmation 1\nCustom affirmation 2\n');
    jest.spyOn(Math, 'random').mockReturnValue(0.0); // Pick first custom affirmation

    await run();

    expect(fs.readFileSync).toHaveBeenCalledWith('tests/affirmations.txt', 'utf8');
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Loaded 2 custom affirmations from tests/affirmations.txt.'));
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'polsala',
      repo: 'ApocalypsAI',
      issue_number: 1,
      body: expect.stringContaining('Custom affirmation 1'),
    });
  });

  test('should use default affirmations if custom file is empty', async () => {
    core.getInput.mockImplementation((name) => {
      if (name === 'affirmations-file') return 'tests/empty_affirmations.txt';
      if (name === 'github-token') return 'mock-token';
      if (name === 'reaction-emojis') return 'sparkles';
      return '';
    });

    // Mock rationale: fs.readFileSync is an external dependency, mocking it ensures tests are offline and deterministic.
    fs.readFileSync.mockReturnValue('\n \n'); // Empty or whitespace-only file
    jest.spyOn(Math, 'random').mockReturnValue(0.5); // Pick 5th default affirmation

    await run();

    expect(fs.readFileSync).toHaveBeenCalledWith('tests/empty_affirmations.txt', 'utf8');
    expect(core.warning).toHaveBeenCalledWith(expect.stringContaining('Custom affirmations file tests/empty_affirmations.txt was empty or contained no valid affirmations. Using default list.'));
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'polsala',
      repo: 'ApocalypsAI',
      issue_number: 1,
      body: expect.stringContaining('This is truly apocalyptic-ally awesome!'),
    });
  });

  test('should use default affirmations if custom file read fails', async () => {
    core.getInput.mockImplementation((name) => {
      if (name === 'affirmations-file') return 'tests/non_existent.txt';
      if (name === 'github-token') return 'mock-token';
      if (name === 'reaction-emojis') return 'sparkles';
      return '';
    });

    // Mock rationale: fs.readFileSync is an external dependency, mocking it ensures tests are offline and deterministic.
    fs.readFileSync.mockImplementation(() => {
      throw new Error('File not found');
    });
    jest.spyOn(Math, 'random').mockReturnValue(0.5); // Pick 5th default affirmation

    await run();

    expect(fs.readFileSync).toHaveBeenCalledWith('tests/non_existent.txt', 'utf8');
    expect(core.warning).toHaveBeenCalledWith(expect.stringContaining('Could not read custom affirmations file at tests/non_existent.txt: File not found. Using default list.'));
    expect(createCommentMock).toHaveBeenCalledWith({
      owner: 'polsala',
      repo: 'ApocalypsAI',
      issue_number: 1,
      body: expect.stringContaining('This is truly apocalyptic-ally awesome!'),
    });
  });

  test('should call setFailed if an error occurs during execution', async () => {
    createCommentMock.mockRejectedValue(new Error('API Error'));

    await run();

    expect(core.setFailed).toHaveBeenCalledWith('API Error');
  });
});
