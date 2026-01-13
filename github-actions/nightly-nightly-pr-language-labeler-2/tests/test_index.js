const core = require('@actions/core');
const github = require('@actions/github');
const { detectLanguages, run } = require('../src/index');

jest.mock('@actions/core');
jest.mock('@actions/github');

describe('detectLanguages', () => {
  test('maps extensions to languages', () => {
    const files = ['app.js', 'main.py', 'script.sh', 'README.md'];
    expect(detectLanguages(files).sort()).toEqual(['javascript', 'python', 'shell'].sort());
  });
});

describe('run', () => {
  const mockAddLabels = jest.fn();
  const mockListFiles = jest.fn().mockResolvedValue({ data: [{ filename: 'test.go' }, { filename: 'lib.rs' }] });
  beforeEach(() => {
    jest.clearAllMocks();
    core.getInput.mockImplementation(name => {
      if (name === 'github-token') return 'fake-token';
      if (name === 'files') return '';
      return '';
    });
    github.context = {
      payload: { pull_request: { number: 42 } },
      repo: { owner: 'owner', repo: 'repo' }
    };
    github.getOctokit.mockReturnValue({
      rest: {
        pulls: { listFiles: mockListFiles },
        issues: { addLabels: mockAddLabels }
      }
    });
  });

  test('adds language labels based on changed files', async () => {
    await run();
    expect(mockAddLabels).toHaveBeenCalledWith({
      owner: 'owner',
      repo: 'repo',
      issue_number: 42,
      labels: ['lang:go', 'lang:rust']
    });
  });

  test('uses provided files input', async () => {
    core.getInput.mockImplementation(name => {
      if (name === 'github-token') return 'fake-token';
      if (name === 'files') return JSON.stringify(['a.rb', 'b.rb']);
      return '';
    });
    await run();
    expect(mockAddLabels).toHaveBeenCalledWith({
      owner: 'owner',
      repo: 'repo',
      issue_number: 42,
      labels: ['lang:ruby']
    });
  });
});
