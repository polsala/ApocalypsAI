const { generateActivity, generateMessage } = require('../src/detoxer');

describe('detoxer', () => {
  let randomSpy;

  beforeEach(() => {
    // Mock rationale: Ensure deterministic random selection for activities and messages.
    // We want to control which item is picked from the internal lists for consistent test results.
    randomSpy = jest.spyOn(Math, 'random');
  });

  afterEach(() => {
    randomSpy.mockRestore();
  });

  test('generateActivity should return a random activity from the full list if no preferences', () => {
    randomSpy.mockReturnValue(0.01); // Force selection of the first activity
    const activity = generateActivity();
    expect(activity).toContain('Gaze at the stars or clouds');
  });

  test('generateActivity should return an activity filtered by a single preference', () => {
    randomSpy.mockReturnValue(0.99); // Force selection of the last matching activity
    const activity = generateActivity(['practical']);
    expect(activity).toContain('Fix something broken around your dwelling');
  });

  test('generateActivity should return an activity filtered by multiple preferences', () => {
    randomSpy.mockReturnValue(0.01); // Force selection of the first matching activity
    const activity = generateActivity(['creative', 'physical']);
    expect(activity).toContain('Take a walk in the nearest green space'); // This is the first activity that matches either 'creative' or 'physical'
  });

  test('generateActivity should fallback to all activities if no preference match', () => {
    randomSpy.mockReturnValue(0.5); // Pick a middle activity from the full list
    const activity = generateActivity(['nonexistent']);
    expect(activity).toBeDefined(); // Should not be empty
    expect(typeof activity).toBe('string');
    // The specific activity depends on the full list and the mock value
    // With 0.5, it should pick the 6th activity (index 5) from the original list of 12
    expect(activity).toContain('Cook a complex meal from scratch');
  });

  test('generateMessage should return a formatted message with duration and reason', () => {
    randomSpy.mockReturnValue(0.01); // Force selection of the first message template
    const message = generateMessage('2 hours', 'deep thought');
    expect(message).toContain('2 hours');
    expect(message).toContain('deep thought');
    expect(message).toContain('Greetings, fellow travelers of the digital ether.');
  });

  test('generateMessage should handle missing duration gracefully', () => {
    randomSpy.mockReturnValue(0.01); // Force selection of the first message template
    const message = generateMessage(undefined, 'recharge');
    expect(message).toContain('an unspecified period');
    expect(message).toContain('recharge');
  });

  test('generateMessage should handle missing reason gracefully', () => {
    randomSpy.mockReturnValue(0.01); // Force selection of the first message template
    const message = generateMessage('1 day');
    expect(message).toContain('1 day');
    expect(message).toContain('recharge my essence');
  });

  test('generateMessage should handle both missing duration and reason gracefully', () => {
    randomSpy.mockReturnValue(0.01); // Force selection of the first message template
    const message = generateMessage();
    expect(message).toContain('an unspecified period');
    expect(message).toContain('recharge my essence');
  });
});
