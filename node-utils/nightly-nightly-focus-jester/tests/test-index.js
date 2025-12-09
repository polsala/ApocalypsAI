const { focusSession, tellJoke } = require('../src/index');
const originalTimeout = global.setTimeout;

// Mock setTimeout for deterministic testing
beforeEach(() => {
  global.setTimeout = (fn) => fn();
});

afterEach(() => {
  global.setTimeout = originalTimeout;
});

// Test 1: Verify joke is told after session
it('should trigger joke callback', () => {
  const consoleSpy = jest.spyOn(console, 'log');
  focusSession(0.001);
  expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining('Break Time!'));
  consoleSpy.mockRestore();
});

// Test 2: Validate --help flag output
it('should show help when --help is provided', () => {
  const consoleSpy = jest.spyOn(console, 'log');
  require('../src/index'); // Force CLI execution
  expect(consoleSpy).toHaveBeenCalledWith('Usage: focusjester [minutes]');
  consoleSpy.mockRestore();
});
