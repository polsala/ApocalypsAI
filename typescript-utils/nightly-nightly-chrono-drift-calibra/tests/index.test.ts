import { calculateDrift, getRecalibrationMantra, run } from '../src/index';

// Mock rationale: We mock console.error and console.log to prevent actual console output during tests
// and to capture what would be printed, allowing us to assert on it.
const mockConsoleError = jest.spyOn(console, 'error').mockImplementation(() => {});
const mockConsoleLog = jest.spyOn(console, 'log').mockImplementation(() => {});

describe('calculateDrift', () => {
  it('should return 0 for identical times', () => {
    const actual = new Date('2023-10-27T10:00:00.000Z');
    const perceived = new Date('2023-10-27T10:00:00.000Z');
    expect(calculateDrift(actual, perceived)).toBe(0);
  });

  it('should return positive drift if perceived time is ahead', () => {
    const actual = new Date('2023-10-27T10:00:00.000Z');
    const perceived = new Date('2023-10-27T10:00:10.000Z'); // 10 seconds ahead
    expect(calculateDrift(actual, perceived)).toBe(10 * 1000);
  });

  it('should return negative drift if perceived time is behind', () => {
    const actual = new Date('2023-10-27T10:00:00.000Z');
    const perceived = new Date('2023-10-27T09:59:50.000Z'); // 10 seconds behind
    expect(calculateDrift(actual, perceived)).toBe(-10 * 1000);
  });
});

describe('getRecalibrationMantra', () => {
  it('should return perfect alignment mantra for 0 drift', () => {
    expect(getRecalibrationMantra(0)).toBe('Your internal chronometer is perfectly aligned with the cosmic flow. Serenity.');
  });

  it('should return gentle nudge mantra for small positive drift (30 seconds)', () => {
    expect(getRecalibrationMantra(30 * 1000)).toBe('A gentle nudge for your temporal compass. Breathe and realign.');
  });

  it('should return gentle nudge mantra for small negative drift (30 seconds)', () => {
    expect(getRecalibrationMantra(-30 * 1000)).toBe('A gentle nudge for your temporal compass. Breathe and realign.');
  });

  it('should return fabric ripples mantra for medium drift (30 minutes)', () => {
    expect(getRecalibrationMantra(30 * 60 * 1000)).toBe('The fabric of time ripples slightly. Re-anchor your awareness.');
  });

  it('should return significant resonance mantra for large drift (12 hours)', () => {
    expect(getRecalibrationMantra(12 * 60 * 60 * 1000)).toBe('Significant temporal resonance detected. Seek a stable temporal anchor.');
  });

  it('should return reality wavers mantra for very large drift (2 days)', () => {
    expect(getRecalibrationMantra(2 * 24 * 60 * 60 * 1000)).toBe('Reality itself seems to waver. Embrace the present, for it is all you truly have.');
  });
});

describe('run', () => {
  afterEach(() => {
    jest.clearAllMocks();
  });

  it('should return null and log error for insufficient arguments', () => {
    const result = run(['2023-10-27T10:00:00.000Z']);
    expect(result).toBeNull();
    expect(mockConsoleError).toHaveBeenCalledWith('Usage: node dist/index.js <actual_time_iso> <perceived_time_iso>');
  });

  it('should return null and log error for invalid date format', () => {
    const result = run(['invalid-date', '2023-10-27T10:00:00.000Z']);
    expect(result).toBeNull();
    expect(mockConsoleError).toHaveBeenCalledWith('Error: Invalid date format. Please use ISO 8601 strings.');
  });

  it('should calculate drift and log mantra for valid input', () => {
    const actualTime = '2023-10-27T10:00:00.000Z';
    const perceivedTime = '2023-10-27T10:00:30.000Z';
    const expectedDrift = 30 * 1000;
    const expectedMantra = 'A gentle nudge for your temporal compass. Breathe and realign.';

    const result = run([actualTime, perceivedTime]);

    expect(result).toEqual({
      driftMs: expectedDrift,
      mantra: expectedMantra,
    });
    expect(mockConsoleLog).toHaveBeenCalledWith(`Temporal Drift: ${expectedDrift}ms`);
    expect(mockConsoleLog).toHaveBeenCalledWith(`Recalibration Mantra: ${expectedMantra}`);
  });

  it('should handle negative drift correctly', () => {
    const actualTime = '2023-10-27T10:00:30.000Z';
    const perceivedTime = '2023-10-27T10:00:00.000Z';
    const expectedDrift = -30 * 1000;
    const expectedMantra = 'A gentle nudge for your temporal compass. Breathe and realign.';

    const result = run([actualTime, perceivedTime]);

    expect(result).toEqual({
      driftMs: expectedDrift,
      mantra: expectedMantra,
    });
    expect(mockConsoleLog).toHaveBeenCalledWith(`Temporal Drift: ${expectedDrift}ms`);
    expect(mockConsoleLog).toHaveBeenCalledWith(`Recalibration Mantra: ${expectedMantra}`);
  });
});
