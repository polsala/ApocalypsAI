const core = require('@actions/core');
const github = require('@actions/github');
const { run } = require('../src/main');

// Mock the GitHub Actions toolkit
jest.mock('@actions/core');
jest.mock('@actions/github');

describe('nightly-dust-bunny-collector', () => {
  let mockListWorkflowRuns;
  let mockDeleteWorkflowRun;

  beforeEach(() => {
    jest.clearAllMocks();

    // Mock github.context
    github.context = {
      repo: {
        owner: 'test-owner',
        repo: 'test-repo',
      },
    };

    // Mock core.getInput
    core.getInput.mockImplementation((name) => {
      if (name === 'token') return 'mock-token';
      if (name === 'retention-days') return '30';
      return '';
    });

    // Mock Octokit methods
    mockListWorkflowRuns = jest.fn();
    mockDeleteWorkflowRun = jest.fn();

    github.getOctokit.mockReturnValue({
      rest: {
        actions: {
          listWorkflowRunsForRepo: mockListWorkflowRuns,
          deleteWorkflowRun: mockDeleteWorkflowRun,
        },
      },
    });
  });

  test('should delete old workflow runs', async () => {
    // Mock rationale: Simulating GitHub API response for workflow runs.
    // We need runs both older and newer than the retention period.
    const now = new Date();
    const oldDate = new Date();
    oldDate.setDate(now.getDate() - 31); // 31 days old, should be deleted
    const recentDate = new Date();
    recentDate.setDate(now.getDate() - 10); // 10 days old, should be kept

    mockListWorkflowRuns.mockResolvedValueOnce({
      data: {
        workflow_runs: [
          { id: 1, name: 'Old Run 1', created_at: oldDate.toISOString() },
          { id: 2, name: 'Recent Run 1', created_at: recentDate.toISOString() },
          { id: 3, name: 'Old Run 2', created_at: oldDate.toISOString() },
        ],
      },
    }).mockResolvedValueOnce({ // Simulate no more pages
      data: {
        workflow_runs: [],
      },
    });

    mockDeleteWorkflowRun.mockResolvedValue({}); // Mock rationale: Simulate successful deletion.

    await run();

    expect(core.getInput).toHaveBeenCalledWith('token', { required: true });
    expect(core.getInput).toHaveBeenCalledWith('retention-days');
    expect(mockListWorkflowRuns).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      per_page: 100,
      page: 1,
    });
    expect(mockDeleteWorkflowRun).toHaveBeenCalledTimes(2);
    expect(mockDeleteWorkflowRun).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      run_id: 1,
    });
    expect(mockDeleteWorkflowRun).toHaveBeenCalledWith({
      owner: 'test-owner',
      repo: 'test-repo',
      run_id: 3,
    });
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Successfully swept away 2 dust bunnies.'));
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should not delete any runs if none are old enough', async () => {
    // Mock rationale: Simulating GitHub API response where all runs are recent.
    const now = new Date();
    const recentDate = new Date();
    recentDate.setDate(now.getDate() - 10); // 10 days old, should be kept

    mockListWorkflowRuns.mockResolvedValueOnce({
      data: {
        workflow_runs: [
          { id: 1, name: 'Recent Run 1', created_at: recentDate.toISOString() },
          { id: 2, name: 'Recent Run 2', created_at: recentDate.toISOString() },
        ],
      },
    }).mockResolvedValueOnce({
      data: {
        workflow_runs: [],
      },
    });

    await run();

    expect(mockListWorkflowRuns).toHaveBeenCalledTimes(2); // Called once, then again for next page (empty)
    expect(mockDeleteWorkflowRun).not.toHaveBeenCalled();
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Successfully swept away 0 dust bunnies.'));
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should handle API errors during listing workflow runs', async () => {
    // Mock rationale: Simulating a failure in the GitHub API call to list runs.
    mockListWorkflowRuns.mockRejectedValue(new Error('API List Error'));

    await run();

    expect(core.setFailed).toHaveBeenCalledWith('API List Error');
    expect(mockDeleteWorkflowRun).not.toHaveBeenCalled();
  });

  test('should handle API errors during deleting a specific workflow run', async () => {
    // Mock rationale: Simulating a failure in the GitHub API call to delete a specific run.
    const now = new Date();
    const oldDate = new Date();
    oldDate.setDate(now.getDate() - 31);

    mockListWorkflowRuns.mockResolvedValueOnce({
      data: {
        workflow_runs: [
          { id: 1, name: 'Old Run 1', created_at: oldDate.toISOString() },
          { id: 2, name: 'Old Run 2', created_at: oldDate.toISOString() },
        ],
      },
    }).mockResolvedValueOnce({
      data: {
        workflow_runs: [],
      },
    });

    mockDeleteWorkflowRun.mockRejectedValueOnce(new Error('Delete Failed for Run 1')) // Fail for first delete
                         .mockResolvedValueOnce({}); // Succeed for second delete

    await run();

    expect(mockDeleteWorkflowRun).toHaveBeenCalledTimes(2);
    expect(core.warning).toHaveBeenCalledWith(expect.stringContaining('Failed to delete workflow run ID 1: Delete Failed for Run 1'));
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Deleted workflow run: ID 2'));
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Successfully swept away 1 dust bunnies.')); // Only one succeeded
    expect(core.setFailed).not.toHaveBeenCalled(); // Overall action should not fail if one delete fails
  });

  test('should handle invalid retention-days input', async () => {
    core.getInput.mockImplementation((name) => {
      if (name === 'token') return 'mock-token';
      if (name === 'retention-days') return '-5'; // Invalid input
      return '';
    });

    await run();

    expect(core.setFailed).toHaveBeenCalledWith('retention-days must be a positive integer.');
    expect(mockListWorkflowRuns).not.toHaveBeenCalled();
    expect(mockDeleteWorkflowRun).not.toHaveBeenCalled();
  });

  test('should handle zero retention-days input', async () => {
    core.getInput.mockImplementation((name) => {
      if (name === 'token') return 'mock-token';
      if (name === 'retention-days') return '0'; // Invalid input
      return '';
    });

    await run();

    expect(core.setFailed).toHaveBeenCalledWith('retention-days must be a positive integer.');
    expect(mockListWorkflowRuns).not.toHaveBeenCalled();
    expect(mockDeleteWorkflowRun).not.toHaveBeenCalled();
  });

  test('should handle non-numeric retention-days input', async () => {
    core.getInput.mockImplementation((name) => {
      if (name === 'token') return 'mock-token';
      if (name === 'retention-days') return 'abc'; // Invalid input
      return '';
    });

    await run();

    expect(core.setFailed).toHaveBeenCalledWith('retention-days must be a positive integer.');
    expect(mockListWorkflowRuns).not.toHaveBeenCalled();
    expect(mockDeleteWorkflowRun).not.toHaveBeenCalled();
  });

  test('should paginate through workflow runs', async () => {
    // Mock rationale: Simulate multiple pages of workflow runs.
    const now = new Date();
    const oldDate = new Date();
    oldDate.setDate(now.getDate() - 31);

    mockListWorkflowRuns.mockResolvedValueOnce({
      data: {
        workflow_runs: Array(100).fill(null).map((_, i) => ({ id: i + 1, name: `Old Run ${i + 1}`, created_at: oldDate.toISOString() })),
      },
    }).mockResolvedValueOnce({
      data: {
        workflow_runs: [
          { id: 101, name: 'Old Run 101', created_at: oldDate.toISOString() },
        ],
      },
    }).mockResolvedValueOnce({
      data: {
        workflow_runs: [],
      },
    });

    mockDeleteWorkflowRun.mockResolvedValue({}); // Mock rationale: Simulate successful deletion.

    await run();

    expect(mockListWorkflowRuns).toHaveBeenCalledTimes(3);
    expect(mockListWorkflowRuns).toHaveBeenCalledWith({ owner: 'test-owner', repo: 'test-repo', per_page: 100, page: 1 });
    expect(mockListWorkflowRuns).toHaveBeenCalledWith({ owner: 'test-owner', repo: 'test-repo', per_page: 100, page: 2 });
    expect(mockDeleteWorkflowRun).toHaveBeenCalledTimes(101);
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('Successfully swept away 101 dust bunnies.'));
  });
});
