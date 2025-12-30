const core = require('@actions/core');
const github = require('@actions/github');

jest.mock('@actions/core');
jest.mock('@actions/github');

const { run, extractEmojis } = require('../src/index');

describe('extractEmojis', () => {
  test('extracts emojis from text', () => {
    const text = 'Add feature 🚀 and fix bug 🐛';
    expect(extractEmojis(text)).toEqual(['🚀', '🐛']);
  });
});

describe('run', () => {
  const mockAddLabels = jest.fn();
  beforeEach(() => {
    jest.clearAllMocks();
    core.getInput.mockReturnValue('fake-token');
    core.info = jest.fn();
    core.setFailed = jest.fn();
    github.getOctokit.mockReturnValue({
      rest: {
        issues: {
          addLabels: mockAddLabels
        }
      }
    });
    github.context = {
      payload: {
        pull_request: {
          title: 'Improve docs 📚',
          number: 42
        }
      },
      repo: {
        owner: 'owner',
        repo: 'repo'
      }
    };
  });

  test('adds documentation label when 📚 emoji is present', async () => {
    await run();
    expect(mockAddLabels).toHaveBeenCalledWith({
      owner: 'owner',
      repo: 'repo',
      issue_number: 42,
      labels: ['documentation']
    });
    expect(core.info).toHaveBeenCalledWith('Added labels: documentation');
  });

  test('does nothing when no matching emojis', async () => {
    github.context.payload.pull_request.title = 'Just a regular title';
    await run();
    expect(mockAddLabels).not.toHaveBeenCalled();
    expect(core.info).toHaveBeenCalledWith('No matching emojis found; nothing to label.');
  });
});
