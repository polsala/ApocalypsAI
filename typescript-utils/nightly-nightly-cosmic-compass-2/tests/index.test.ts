import { generateCosmicGuidance } from '../src/index';
import { createSeededRandom, formatDate, generateSeedFromDate } from '../src/utils';

// Mock rationale: We need to ensure that `new Date()` always returns a predictable value
// for our tests to be deterministic. We also mock `console.log` to capture CLI output.
describe('Nightly Cosmic Compass', () => {
  const mockDate = new Date('2024-07-21T10:00:00Z'); // A fixed date for testing
  const mockDateString = '2024-07-21';

  beforeAll(() => {
    // Mock Date constructor to return a fixed date
    const mockDateConstructor = jest.fn(() => mockDate);
    // @ts-ignore: Mocking global Date is complex, but necessary for deterministic tests.
    global.Date = mockDateConstructor;
    global.Date.now = jest.fn(() => mockDate.getTime());
  });

  afterAll(() => {
    // Restore original Date constructor
    jest.restoreAllMocks();
  });

  it('should generate consistent guidance for a specific date', () => {
    const date1 = new Date('2024-01-01');
    const guidance1 = generateCosmicGuidance(date1);

    const date2 = new Date('2024-01-01'); // Same date
    const guidance2 = generateCosmicGuidance(date2);

    expect(guidance1).toEqual(guidance2);
    expect(guidance1.date).toBe('2024-01-01');
    expect(guidance1.focus).toBeDefined();
    expect(guidance1.message).toBeDefined();
    expect(guidance1.colorPalette).toBeInstanceOf(Array);
    expect(guidance1.colorPalette.length).toBeGreaterThan(0);
  });

  it('should generate different guidance for different dates', () => {
    const date1 = new Date('2024-01-01');
    const guidance1 = generateCosmicGuidance(date1);

    const date2 = new Date('2024-01-02'); // Different date
    const guidance2 = generateCosmicGuidance(date2);

    expect(guidance1).not.toEqual(guidance2);
  });

  it('should correctly format date', () => {
    const date = new Date('2023-03-05T12:34:56Z');
    expect(formatDate(date)).toBe('2023-03-05');
  });

  it('should generate a consistent seed from a date string', () => {
    const seed1 = generateSeedFromDate('2024-07-21');
    const seed2 = generateSeedFromDate('2024-07-21');
    const seed3 = generateSeedFromDate('2024-07-22');

    expect(seed1).toBe(seed2);
    expect(seed1).not.toBe(seed3);
    expect(typeof seed1).toBe('number');
  });

  it('createSeededRandom should produce deterministic sequence', () => {
    const seed = 12345;
    const random1 = createSeededRandom(seed);
    const random2 = createSeededRandom(seed);

    expect(random1()).toBe(random2());
    expect(random1()).toBe(random2()); // Check multiple calls
    expect(random1()).not.toBe(random2(seed)); // Should be different if re-seeded
  });

  it('should generate guidance for the mocked current date when no argument is provided', () => {
    // Mock rationale: Capture console output to verify the main function's behavior.
    const mockConsoleLog = jest.spyOn(console, 'log').mockImplementation(() => {});
    const originalArgv = process.argv;
    process.argv = ['node', 'index.js']; // No date argument

    // Directly test the core logic with the mocked date, as `main` is not exported.
    // A full CLI test would involve `child_process.exec` but that's outside the scope of 'offline' unit tests.
    const guidance = generateCosmicGuidance(mockDate);
    expect(guidance.date).toBe(mockDateString);
    expect(guidance.focus).toBeDefined();
    expect(guidance.message).toBeDefined();
    expect(guidance.colorPalette).toBeInstanceOf(Array);

    mockConsoleLog.mockRestore();
    process.argv = originalArgv;
  });

  // Test specific output for a known date to ensure determinism
  it('should produce specific guidance for 2024-07-21', () => {
    const specificDate = new Date('2024-07-21T00:00:00Z');
    const guidance = generateCosmicGuidance(specificDate);

    // These values are derived by running the utility with this date and observing output.
    // They are hardcoded to ensure determinism.
    expect(guidance.date).toBe('2024-07-21');
    expect(guidance.focus).toBe('Strategic Scavenge');
    expect(guidance.message).toBe("Prioritize your resources. Every scrap counts in the grand scheme of survival.");
    expect(guidance.colorPalette).toEqual(['#006400', '#228B22', '#3CB371', '#90EE90']);
  });

  it('should produce specific guidance for 2025-01-01', () => {
    const specificDate = new Date('2025-01-01T00:00:00Z');
    const guidance = generateCosmicGuidance(specificDate);

    expect(guidance.date).toBe('2025-01-01');
    expect(guidance.focus).toBe('Reflective Ripple');
    expect(guidance.message).toBe("The universe is vast and indifferent. Find your own meaning within its expanse.");
    expect(guidance.colorPalette).toEqual(['#8B0000', '#FF4500', '#FFD700', '#ADFF2F']);
  });
});
