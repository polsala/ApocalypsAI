import { fetchWorkflows } from '../src/api';

describe('fetchWorkflows', () => {
  // # Mock rationale: Simulates network latency and potential API failures
  // to ensure tests are deterministic and do not rely on actual network calls.
  beforeEach(() => {
    jest.spyOn(global, 'setTimeout').mockImplementation(cb => cb());
    jest.spyOn(Math, 'random').mockReturnValue(0.5); // Ensure no error for basic tests
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  test('should return a successful response with workflow data', async () => {
    const response = await fetchWorkflows();
    expect(response.success).toBe(true);
    expect(response.data).toBeInstanceOf(Array);
    expect(response.data.length).toBeGreaterThan(0);
    expect(response.data[0]).toHaveProperty('id');
    expect(response.data[0]).toHaveProperty('name');
    expect(response.data[0]).toHaveProperty('status');
    expect(response.data[0]).toHaveProperty('lastRun');
    expect(response.data[0]).toHaveProperty('mood');
    expect(response.data[0].mood).toHaveProperty('emoji');
    expect(response.data[0].mood).toHaveProperty('description');
  });

  test('should return a failure response if random condition met', async () => {
    jest.spyOn(Math, 'random').mockReturnValue(0.05); // Force success
    let response = await fetchWorkflows();
    expect(response.success).toBe(true);

    jest.spyOn(Math, 'random').mockReturnValue(0.15); // Force failure
    response = await fetchWorkflows();
    expect(response.success).toBe(false);
    expect(response.error).toBe('Failed to fetch cosmic threads.');
  });
});
