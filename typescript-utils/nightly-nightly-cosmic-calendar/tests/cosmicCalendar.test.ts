import { earthToCosmic, cosmicToEarth } from '../src/index';

describe('Cosmic Calendar Converter', () => {
  // Mock rationale: Date objects are used internally for calculations,
  // but the core logic relies on `getDaysBetween` which is deterministic.
  // The epoch is fixed (Jan 1, 2000 UTC), so there is no reliance on the
  // current system date or time, making tests fully deterministic and offline.
  // All inputs are strings or numbers, ensuring consistent test results.

  // Test cases for earthToCosmic
  test('should convert the cosmic epoch start date correctly', () => {
    const cosmicDate = earthToCosmic('2000-01-01');
    expect(cosmicDate).toEqual({ cosmicYear: 1, phase: 'Nebula Bloom', cycle: 1 });
  });

  test('should convert a date within the first phase', () => {
    const cosmicDate = earthToCosmic('2000-01-15'); // 15th day
    expect(cosmicDate).toEqual({ cosmicYear: 1, phase: 'Nebula Bloom', cycle: 15 });
  });

  test('should convert a date at the end of the first phase', () => {
    const cosmicDate = earthToCosmic('2000-01-30'); // 30th day
    expect(cosmicDate).toEqual({ cosmicYear: 1, phase: 'Nebula Bloom', cycle: 30 });
  });

  test('should convert a date at the start of the second phase', () => {
    const cosmicDate = earthToCosmic('2000-01-31'); // 31st day
    expect(cosmicDate).toEqual({ cosmicYear: 1, phase: 'Void Gaze', cycle: 1 });
  });

  test('should convert a date in the middle of the year', () => {
    const cosmicDate = earthToCosmic('2000-07-01'); // Day 182 (30*6 + 2)
    expect(cosmicDate).toEqual({ cosmicYear: 1, phase: 'Quantum Ripple', cycle: 2 });
  });

  test('should convert a date at the end of the year (Interstellar Drift)', () => {
    const cosmicDate = earthToCosmic('2000-12-31'); // Day 365
    expect(cosmicDate).toEqual({ cosmicYear: 1, phase: 'Interstellar Drift', cycle: 5 });
  });

  test('should convert a date at the start of the next cosmic year', () => {
    const cosmicDate = earthToCosmic('2001-01-01'); // Day 366
    expect(cosmicDate).toEqual({ cosmicYear: 2, phase: 'Nebula Bloom', cycle: 1 });
  });

  test('should handle a date far in the future', () => {
    const cosmicDate = earthToCosmic('2050-06-15');
    // 2050-06-15 is 18412 days from 2000-01-01
    // 18412 / 365 = 50.44... -> cosmic year 51
    // 18412 % 365 = 162 days into cosmic year
    // 162 days: 5 phases * 30 days = 150 days. Remaining 12 days.
    // So, 6th phase (Galactic Whisper), cycle 12.
    expect(cosmicDate).toEqual({ cosmicYear: 51, phase: 'Galactic Whisper', cycle: 12 });
  });

  test('should throw error for invalid Earth date string', () => {
    expect(() => earthToCosmic('not-a-date')).toThrow("Invalid Earth date string provided.");
  });

  test('should throw error for date before cosmic epoch', () => {
    expect(() => earthToCosmic('1999-12-31')).toThrow("Date is before the Cosmic Epoch (Jan 1, 2000).");
  });

  // Test cases for cosmicToEarth
  test('should convert Cosmic Year 1, Nebula Bloom, Cycle 1 to Earth epoch', () => {
    const earthDate = cosmicToEarth(1, 'Nebula Bloom', 1);
    expect(earthDate).toBe('2000-01-01');
  });

  test('should convert Cosmic Year 1, Nebula Bloom, Cycle 15', () => {
    const earthDate = cosmicToEarth(1, 'Nebula Bloom', 15);
    expect(earthDate).toBe('2000-01-15');
  });

  test('should convert Cosmic Year 1, Void Gaze, Cycle 1', () => {
    const earthDate = cosmicToEarth(1, 'Void Gaze', 1);
    expect(earthDate).toBe('2000-01-31');
  });

  test('should convert Cosmic Year 1, Interstellar Drift, Cycle 5 (end of year)', () => {
    const earthDate = cosmicToEarth(1, 'Interstellar Drift', 5);
    expect(earthDate).toBe('2000-12-31');
  });

  test('should convert Cosmic Year 2, Nebula Bloom, Cycle 1 (start of next year)', () => {
    const earthDate = cosmicToEarth(2, 'Nebula Bloom', 1);
    expect(earthDate).toBe('2001-01-01');
  });

  test('should convert a future cosmic date back to Earth date', () => {
    const earthDate = cosmicToEarth(51, 'Galactic Whisper', 12);
    expect(earthDate).toBe('2050-06-15');
  });

  test('should throw error for invalid cosmic year', () => {
    expect(() => cosmicToEarth(0, 'Nebula Bloom', 1)).toThrow("Cosmic Year must be 1 or greater.");
  });

  test('should throw error for invalid phase name', () => {
    expect(() => cosmicToEarth(1, 'NonExistentPhase', 1)).toThrow("Invalid Cosmic Phase: NonExistentPhase");
  });

  test('should throw error for cycle out of range for phase', () => {
    expect(() => cosmicToEarth(1, 'Nebula Bloom', 31)).toThrow("Cycle 31 is out of range for Nebula Bloom (1-30).");
    expect(() => cosmicToEarth(1, 'Interstellar Drift', 6)).toThrow("Cycle 6 is out of range for Interstellar Drift (1-5).");
    expect(() => cosmicToEarth(1, 'Nebula Bloom', 0)).toThrow("Cycle 0 is out of range for Nebula Bloom (1-30).");
  });
});
