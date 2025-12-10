const { Octokit } = require('@actions/github');
const { addLabels, createComment } = require('../src/index');

jest.mock('@actions/core');
jest.mock('@actions/github');

const mockTip = 'Remember to commit often';
const mockIssue = {
  number: 456,
  owner: 'test-owner',
  repo: 'test-repo'
};

describe('Wasteland Issue Guardian', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('Adds label and comment to new issue', async () => {
    const octokit = new Octokit();
    octokit.issues.addLabels.mockResolvedValue({});
    octokit.issues.createComment.mockResolvedValue({});

    await addLabels(octokit, mockIssue.owner, mockIssue.repo, mockIssue.number);
    await createComment(octokit, mockIssue.owner, mockIssue.repo, mockIssue.number, mockTip);

    expect(octokit.issues.addLabels).toHaveBeenCalledWith({
      owner: mockIssue.owner,
      repo: mockIssue.repo,
      issue_number: mockIssue.number,
      labels: ['wasteland-guardian']
    });

    expect(octokit.issues.createComment).toHaveBeenCalledWith({
      owner: mockIssue.owner,
      repo: mockIssue.repo,
      issue_number: mockIssue.number,
      body: expect.stringContaining(mockTip)
    });
  });
});
