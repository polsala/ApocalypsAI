const core = require('@actions/core');
const github = require('@actions/github');
const { when } = require('jest-when'); // For more flexible mocking

// Mock the GitHub Actions toolkit
jest.mock('@actions/core');
jest.mock('@actions/github');

// Mock the main action file
const run = require('../src/main'); // Assuming main.js exports the run function or calls it directly

describe('Nightly Workflow Wellness Oracle', () => {
  let listWorkflowRunsForRepoMock;

  beforeEach(() => {
    jest.clearAllMocks();

    // Mock github.context
    github.context = {
      repo: {
        owner: 'test-owner',
        repo: 'test-repo',
      },
    };

    // Mock octokit.rest.actions.listWorkflowRunsForRepo
    listWorkflowRunsForRepoMock = jest.fn();
    github.getOctokit.mockReturnValue({
      rest: {
        actions: {
          listWorkflowRunsForRepo: listWorkflowRunsForRepoMock,
        },
      },
    });

    // Mock core.getInput
    when(core.getInput)
      .calledWith('github-token', expect.any(Object))
      .mockReturnValue('mock-token');
    when(core.getInput)
      .calledWith('days-to-check')
      .mockReturnValue('7'); // Default value
  });

  // Mock rationale: The GitHub API calls are external and non-deterministic.
  // We mock `listWorkflowRunsForRepo` to control the data returned, ensuring
  // tests are deterministic and can cover various scenarios (success, failure, no runs).
  // `core.getInput` and `core.setOutput` are mocked to control action inputs and
  // capture outputs without actual interaction with the GitHub Actions runner environment.

  test('should report flourishing forest when all runs succeed', async () => {
    const now = new Date();
    const sevenDaysAgo = new Date();
    sevenDaysAgo.setDate(now.getDate() - 7);

    listWorkflowRunsForRepoMock.mockResolvedValueOnce({
      data: {
        workflow_runs: [
          { created_at: sevenDaysAgo.toISOString(), updated_at: now.toISOString(), conclusion: 'success', status: 'completed' },
          { created_at: sevenDaysAgo.toISOString(), updated_at: now.toISOString(), conclusion: 'success', status: 'completed' },
          { created_at: sevenDaysAgo.toISOString(), updated_at: now.toISOString(), conclusion: 'success', status: 'completed' },
        ],
      },
    });

    await run();

    expect(core.setOutput).toHaveBeenCalledWith(
      'wellness-report',
      expect.stringContaining('The Workflow Forest is flourishing! 🌳 All 3 recent runs (last 7 days) completed successfully.')
    );
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should report a storm when all runs fail', async () => {
    const now = new Date();
    const sevenDaysAgo = new Date();
    sevenDaysAgo.setDate(now.getDate() - 7);

    listWorkflowRunsForRepoMock.mockResolvedValueOnce({
      data: {
        workflow_runs: [
          { created_at: sevenDaysAgo.toISOString(), updated_at: now.toISOString(), conclusion: 'failure', status: 'completed' },
          { created_at: sevenDaysAgo.toISOString(), updated_at: now.toISOString(), conclusion: 'failure', status: 'completed' },
        ],
      },
    });

    await run();

    expect(core.setOutput).toHaveBeenCalledWith(
      'wellness-report',
      expect.stringContaining('A storm brews in the Workflow Peaks! ⛈️ All 2 recent runs (last 7 days) have failed.')
    );
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should report a river with rapids when some runs fail', async () => {
    const now = new Date();
    const sevenDaysAgo = new Date();
    sevenDaysAgo.setDate(now.getDate() - 7);

    listWorkflowRunsForRepoMock.mockResolvedValueOnce({
      data: {
        workflow_runs: [
          { created_at: sevenDaysAgo.toISOString(), updated_at: now.toISOString(), conclusion: 'success', status: 'completed' },
          { created_at: sevenDaysAgo.toISOString(), updated_at: now.toISOString(), conclusion: 'failure', status: 'completed' },
          { created_at: sevenDaysAgo.toISOString(), updated_at: now.toISOString(), conclusion: 'success', status: 'completed' },
          { created_at: sevenDaysAgo.toISOString(), updated_at: now.toISOString(), conclusion: 'failure', status: 'completed' },
          { created_at: sevenDaysAgo.toISOString(), updated_at: now.toISOString(), conclusion: 'success', status: 'completed' },
        ],
      },
    });

    await run();

    expect(core.setOutput).toHaveBeenCalledWith(
      'wellness-report',
      expect.stringContaining('The Workflow River flows, but with some rapids! 🌊 Out of 5 recent runs (last 7 days), 3 succeeded and 2 encountered obstacles. Success rate: 60.0%.')
    );
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should report no runs found', async () => {
    listWorkflowRunsForRepoMock.mockResolvedValueOnce({
      data: {
        workflow_runs: [],
      },
    });

    await run();

    expect(core.setOutput).toHaveBeenCalledWith(
      'wellness-report',
      expect.stringContaining('The Workflow Oracle finds no recent runs in the last 7 days. The digital winds are calm, or perhaps too calm... 💨')
    );
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should handle pending runs', async () => {
    const now = new Date();
    const sevenDaysAgo = new Date();
    sevenDaysAgo.setDate(now.getDate() - 7);

    listWorkflowRunsForRepoMock.mockResolvedValueOnce({
      data: {
        workflow_runs: [
          { created_at: sevenDaysAgo.toISOString(), updated_at: now.toISOString(), conclusion: null, status: 'in_progress' },
          { created_at: sevenDaysAgo.toISOString(), updated_at: now.toISOString(), conclusion: null, status: 'queued' },
        ],
      },
    });

    await run();

    expect(core.setOutput).toHaveBeenCalledWith(
      'wellness-report',
      expect.stringContaining('The Workflow Loom is busy weaving! 🧵 2 runs are currently in progress or queued.')
    );
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should handle cancelled runs', async () => {
    const now = new Date();
    const sevenDaysAgo = new Date();
    sevenDaysAgo.setDate(now.getDate() - 7);

    listWorkflowRunsForRepoMock.mockResolvedValueOnce({
      data: {
        workflow_runs: [
          { created_at: sevenDaysAgo.toISOString(), updated_at: now.toISOString(), conclusion: 'cancelled', status: 'completed' },
          { created_at: sevenDaysAgo.toISOString(), updated_at: now.toISOString(), conclusion: 'cancelled', status: 'completed' },
        ],
      },
    });

    await run();

    expect(core.setOutput).toHaveBeenCalledWith(
      'wellness-report',
      expect.stringContaining('The Workflow Compass points to new directions! 🧭 2 runs were cancelled.')
    );
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should handle mixed runs with pending and failures', async () => {
    const now = new Date();
    const sevenDaysAgo = new Date();
    sevenDaysAgo.setDate(now.getDate() - 7);

    listWorkflowRunsForRepoMock.mockResolvedValueOnce({
      data: {
        workflow_runs: [
          { created_at: sevenDaysAgo.toISOString(), updated_at: now.toISOString(), conclusion: 'success', status: 'completed' },
          { created_at: sevenDaysAgo.toISOString(), updated_at: now.toISOString(), conclusion: 'failure', status: 'completed' },
          { created_at: sevenDaysAgo.toISOString(), updated_at: now.toISOString(), conclusion: null, status: 'in_progress' },
        ],
      },
    });

    await run();

    // When there are failures, the failure report takes precedence
    expect(core.setOutput).toHaveBeenCalledWith(
      'wellness-report',
      expect.stringContaining('The Workflow River flows, but with some rapids! 🌊 Out of 3 recent runs (last 7 days), 1 succeeded and 1 encountered obstacles. Success rate: 33.3%.')
    );
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should handle invalid days-to-check input', async () => {
    when(core.getInput)
      .calledWith('days-to-check')
      .mockReturnValue('0');

    await run();

    expect(core.setFailed).toHaveBeenCalledWith('days-to-check must be a positive number.');
    expect(core.setOutput).not.toHaveBeenCalled();
  });

  test('should handle API errors gracefully', async () => {
    listWorkflowRunsForRepoMock.mockRejectedValueOnce(new Error('API rate limit exceeded'));

    await run();

    expect(core.setFailed).toHaveBeenCalledWith('API rate limit exceeded');
    expect(core.setOutput).not.toHaveBeenCalled();
  });

  test('should handle pagination correctly', async () => {
    const now = new Date();
    const sevenDaysAgo = new Date();
    sevenDaysAgo.setDate(now.getDate() - 7);

    const runsPage1 = Array(100).fill(null).map((_, i) => ({
      created_at: sevenDaysAgo.toISOString(),
      updated_at: now.toISOString(),
      conclusion: 'success',
      status: 'completed',
      id: i,
    }));
    const runsPage2 = Array(50).fill(null).map((_, i) => ({
      created_at: sevenDaysAgo.toISOString(),
      updated_at: now.toISOString(),
      conclusion: 'failure',
      status: 'completed',
      id: i + 100,
    }));

    listWorkflowRunsForRepoMock
      .mockResolvedValueOnce({ data: { workflow_runs: runsPage1 } })
      .mockResolvedValueOnce({ data: { workflow_runs: runsPage2 } });

    await run();

    expect(listWorkflowRunsForRepoMock).toHaveBeenCalledTimes(2);
    expect(core.setOutput).toHaveBeenCalledWith(
      'wellness-report',
      expect.stringContaining('The Workflow River flows, but with some rapids! 🌊 Out of 150 recent runs (last 7 days), 100 succeeded and 50 encountered obstacles. Success rate: 66.7%.')
    );
    expect(core.setFailed).not.toHaveBeenCalled();
  });

  test('should calculate average duration correctly', async () => {
    const now = new Date();
    const run1Start = new Date(now.getTime() - 60 * 1000); // 1 minute ago
    const run2Start = new Date(now.getTime() - 120 * 1000); // 2 minutes ago

    listWorkflowRunsForRepoMock.mockResolvedValueOnce({
      data: {
        workflow_runs: [
          { created_at: run1Start.toISOString(), updated_at: now.toISOString(), conclusion: 'success', status: 'completed' }, // 60s duration
          { created_at: run2Start.toISOString(), updated_at: now.toISOString(), conclusion: 'success', status: 'completed' }, // 120s duration
        ],
      },
    });

    await run();

    // Average duration should be (60 + 120) / 2 = 90 seconds
    expect(core.setOutput).toHaveBeenCalledWith(
      'wellness-report',
      expect.stringContaining('The average run took 90 seconds.')
    );
    expect(core.setFailed).not.toHaveBeenCalled();
  });
});
