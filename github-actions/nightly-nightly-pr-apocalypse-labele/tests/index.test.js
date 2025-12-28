// Mock rationale: we replace @actions/github and @actions/core with lightweight fakes to test logic without network calls.

jest.mock('@actions/core');
jest.mock('@actions/github');

const core = require('@actions/core');
const github = require('@actions/github');

// Import the action after mocks are set up
const action = require('../src/index');

describe('nightly-pr-apocalypse-labeler', () => {
  const mockAddLabels = jest.fn();
  const originalContext = { ...github.context };

  beforeEach(() => {
    jest.clearAllMocks();
    // Mock inputs
    core.getInput.mockImplementation(name => {
      if (name === 'github-token') return 'fake-token';
      if (name === 'keywords') return 'apocalypse,doom';
      return '';
    });
    // Mock GitHub context for a PR event
    github.context.eventName = 'pull_request';
    github.context.payload = {
      pull_request: {
        number: 42,
        title: 'Doomsday is coming!'
      }
    };
    github.context.repo = { owner: 'octocat', repo: 'hello-world' };
    // Mock Octokit
    github.getOctokit.mockReturnValue({
      rest: {
        issues: {
          addLabels: mockAddLabels
        }
      }
    });
  });

  afterAll(() => {
    // Restore original context to avoid side effects
    github.context = originalContext;
  });

  test('adds label when keyword is present', async () => {
    await require('../src/index'); // run the action
    expect(mockAddLabels).toHaveBeenCalledWith({
      owner: 'octocat',
      repo: 'hello-world',
      issue_number: 42,
      labels: ['apocalypse']
    });
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('does not add label when no keyword matches', async () => {
    github.context.payload.pull_request.title = 'Add new feature X';
    await require('../src/index');
    expect(mockAddLabels).not.toHaveBeenCalled();
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('skips non‑pull_request events', async () => {
    github.context.eventName = 'push';
    await require('../src/index');
    expect(mockAddLabels).not.toHaveBeenCalled();
    expect(core.info).toHaveBeenCalledWith('Event is not a pull_request, skipping.');
  });
});
