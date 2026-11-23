const core = require('@actions/core');
const github = require('@actions/github');
const { run } = require('../src/index');

// Mock the GitHub Actions toolkit
jest.mock('@actions/core');
jest.mock('@actions/github');

describe('Nightly Workflow Chronomancer', () => {
  let listWorkflowRunsForRepoMock;

  beforeEach(() => {
    jest.clearAllMocks();

    // Mock rationale: Simulate the GitHub repository context without needing a real repository.
    github.context = {
      repo: {
        owner: 'test-owner',
        repo: 'test-repo',
      },
    };

    // Mock rationale: Prevent actual GitHub API calls during testing. We control the data returned.
    listWorkflowRunsForRepoMock = jest.fn();
    github.getOctokit.mockReturnValue({
      rest: {
        actions: {
          listWorkflowRunsForRepo: listWorkflowRunsForRepoMock,
        },
      },
    });
  });

  // Helper to create mock run data
  const createMockRun = (id, createdAt, updatedAt, status = 'success') => ({
    id,
    created_at: new Date(createdAt).toISOString(),
    updated_at: new Date(updatedAt).toISOString(),
    status,
    conclusion: status === 'success' ? 'success' : 'failure',
  });

  it('should report "steady" if the latest run is within the threshold', async () => {
    // Mock rationale: Simulate a scenario where workflow runs are consistent, falling within the acceptable deviation threshold.
    core.getInput
      .mockReturnValueOnce('my-workflow.yml') // workflow_id
      .mockReturnValueOnce('mock-token')      // repo_token
      .mockReturnValueOnce('15')              // threshold_percent
      .mockReturnValueOnce('3');              // num_runs_for_average

    const now = Date.now();
    listWorkflowRunsForRepoMock.mockResolvedValue({
      data: {
        workflow_runs: [
          // Latest run: 100 seconds
          createMockRun(101, now - 100000, now),
          // Previous runs for average: 100, 110, 90 seconds (average ~100)
          createMockRun(100, now - 200000, now - 100000),
          createMockRun(99, now - 310000, now - 200000),
          createMockRun(98, now - 400000, now - 310000),
        ],
      },
    });

    await run();

    expect(core.setOutput).toHaveBeenCalledWith('status', 'steady');
    expect(core.setOutput).toHaveBeenCalledWith('duration_change_percent', '0.00'); // (100-100)/100 * 100 = 0
    expect(core.setOutput).toHaveBeenCalledWith('latest_duration_seconds', '100.00');
    expect(core.setOutput).toHaveBeenCalledWith('average_duration_seconds', '100.00');
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('feeling steady'));
  });

  it('should report "sluggish" if the latest run is significantly slower', async () => {
    // Mock rationale: Simulate a scenario where the latest workflow run is significantly slower than its historical average.
    core.getInput
      .mockReturnValueOnce('my-workflow.yml')
      .mockReturnValueOnce('mock-token')
      .mockReturnValueOnce('15') // threshold_percent
      .mockReturnValueOnce('3'); // num_runs_for_average

    const now = Date.now();
    listWorkflowRunsForRepoMock.mockResolvedValue({
      data: {
        workflow_runs: [
          // Latest run: 130 seconds
          createMockRun(101, now - 130000, now),
          // Previous runs for average: 100, 110, 90 seconds (average ~100)
          createMockRun(100, now - 200000, now - 100000),
          createMockRun(99, now - 310000, now - 200000),
          createMockRun(98, now - 400000, now - 310000),
        ],
      },
    });

    await run();

    expect(core.setOutput).toHaveBeenCalledWith('status', 'sluggish');
    expect(core.setOutput).toHaveBeenCalledWith('duration_change_percent', '30.00'); // (130-100)/100 * 100 = 30
    expect(core.setOutput).toHaveBeenCalledWith('latest_duration_seconds', '130.00');
    expect(core.setOutput).toHaveBeenCalledWith('average_duration_seconds', '100.00');
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('feeling sluggish'));
  });

  it('should report "zippy" if the latest run is significantly faster', async () => {
    // Mock rationale: Simulate a scenario where the latest workflow run is significantly faster than its historical average.
    core.getInput
      .mockReturnValueOnce('my-workflow.yml')
      .mockReturnValueOnce('mock-token')
      .mockReturnValueOnce('15') // threshold_percent
      .mockReturnValueOnce('3'); // num_runs_for_average

    const now = Date.now();
    listWorkflowRunsForRepoMock.mockResolvedValue({
      data: {
        workflow_runs: [
          // Latest run: 70 seconds
          createMockRun(101, now - 70000, now),
          // Previous runs for average: 100, 110, 90 seconds (average ~100)
          createMockRun(100, now - 200000, now - 100000),
          createMockRun(99, now - 310000, now - 200000),
          createMockRun(98, now - 400000, now - 310000),
        ],
      },
    });

    await run();

    expect(core.setOutput).toHaveBeenCalledWith('status', 'zippy');
    expect(core.setOutput).toHaveBeenCalledWith('duration_change_percent', '-30.00'); // (70-100)/100 * 100 = -30
    expect(core.setOutput).toHaveBeenCalledWith('latest_duration_seconds', '70.00');
    expect(core.setOutput).toHaveBeenCalledWith('average_duration_seconds', '100.00');
    expect(core.info).toHaveBeenCalledWith(expect.stringContaining('feeling zippy'));
  });

  it('should handle no successful runs found', async () => {
    // Mock rationale: Simulate a scenario where the GitHub API returns no successful workflow runs for the given ID.
    core.getInput
      .mockReturnValueOnce('non-existent-workflow.yml')
      .mockReturnValueOnce('mock-token')
      .mockReturnValueOnce('15')
      .mockReturnValueOnce('3');

    listWorkflowRunsForRepoMock.mockResolvedValue({
      data: {
        workflow_runs: [],
      },
    });

    await run();

    expect(core.warning).toHaveBeenCalledWith(expect.stringContaining('No successful runs found'));
    expect(core.setOutput).toHaveBeenCalledWith('status', 'unknown');
    expect(core.setOutput).toHaveBeenCalledWith('duration_change_percent', '0.00');
    expect(core.setOutput).toHaveBeenCalledWith('latest_duration_seconds', '0.00');
    expect(core.setOutput).toHaveBeenCalledWith('average_duration_seconds', '0.00');
  });

  it('should handle not enough previous runs for average calculation', async () => {
    // Mock rationale: Simulate a scenario where there's a latest run, but insufficient historical runs to compute a meaningful average.
    core.getInput
      .mockReturnValueOnce('my-workflow.yml')
      .mockReturnValueOnce('mock-token')
      .mockReturnValueOnce('15')
      .mockReturnValueOnce('3'); // Requires 3 previous runs for average

    const now = Date.now();
    listWorkflowRunsForRepoMock.mockResolvedValue({
      data: {
        workflow_runs: [
          // Latest run: 100 seconds
          createMockRun(101, now - 100000, now),
          // Only one previous run, but 3 are required for average
          createMockRun(100, now - 200000, now - 100000),
        ],
      },
    });

    await run();

    expect(core.warning).toHaveBeenCalledWith(expect.stringContaining('Not enough previous successful runs'));
    expect(core.setOutput).toHaveBeenCalledWith('status', 'unknown');
    expect(core.setOutput).toHaveBeenCalledWith('duration_change_percent', '0.00');
    expect(core.setOutput).toHaveBeenCalledWith('latest_duration_seconds', '100.00');
    expect(core.setOutput).toHaveBeenCalledWith('average_duration_seconds', '0.00');
  });

  it('should call setFailed on API error', async () => {
    // Mock rationale: Simulate a failure in the GitHub API call, such as rate limiting or invalid token.
    core.getInput
      .mockReturnValueOnce('my-workflow.yml')
      .mockReturnValueOnce('mock-token')
      .mockReturnValueOnce('15')
      .mockReturnValueOnce('3');

    listWorkflowRunsForRepoMock.mockRejectedValue(new Error('API rate limit exceeded'));

    await run();

    expect(core.setFailed).toHaveBeenCalledWith('API rate limit exceeded');
  });

  it('should validate threshold_percent input', async () => {
    // Mock rationale: Test the action's input validation for an invalid (negative) threshold percentage.
    core.getInput
      .mockReturnValueOnce('my-workflow.yml')
      .mockReturnValueOnce('mock-token')
      .mockReturnValueOnce('-5') // Invalid threshold
      .mockReturnValueOnce('3');

    await run();

    expect(core.setFailed).toHaveBeenCalledWith('Input "threshold_percent" must be a non-negative number.');
    expect(listWorkflowRunsForRepoMock).not.toHaveBeenCalled(); // Ensure API call is not made with invalid input
  });

  it('should validate num_runs_for_average input', async () => {
    // Mock rationale: Test the action's input validation for an invalid (non-positive) number of runs for average.
    core.getInput
      .mockReturnValueOnce('my-workflow.yml')
      .mockReturnValueOnce('mock-token')
      .mockReturnValueOnce('15')
      .mockReturnValueOnce('0'); // Invalid num_runs

    await run();

    expect(core.setFailed).toHaveBeenCalledWith('Input "num_runs_for_average" must be a positive integer.');
    expect(listWorkflowRunsForRepoMock).not.toHaveBeenCalled(); // Ensure API call is not made with invalid input
  });
});
