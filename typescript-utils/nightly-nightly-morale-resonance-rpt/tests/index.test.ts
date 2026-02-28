import { handleAddEntry, generateEmotionalReport } from '../src/index';
import { getMoodEntries, clearMoodEntries } from '../src/data';
import { MoodEntry, EmotionalReport } from '../src/types';

// # Mock rationale: We're clearing the in-memory data store before each test
// to ensure tests are isolated and deterministic, without relying on file I/O.
beforeEach(() => {
  clearMoodEntries();
});

describe('handleAddEntry', () => {
  it('should add a new mood entry with valid data', () => {
    // # Mock rationale: Using a fixed timestamp for deterministic testing.
    const mockDateNow = jest.spyOn(Date, 'now').mockReturnValue(1678886400000); // March 15, 2023 00:00:00 GMT

    const entry = handleAddEntry(4, ['food', 'shelter'], 'Good day, found supplies.');
    const entries = getMoodEntries();

    expect(entries).toHaveLength(1);
    expect(entries[0]).toEqual({
      timestamp: 1678886400000,
      moodScore: 4,
      factors: ['food', 'shelter'],
      notes: 'Good day, found supplies.',
    });
    expect(entry).toEqual(entries[0]);

    mockDateNow.mockRestore();
  });

  it('should throw an error for invalid mood score', () => {
    expect(() => handleAddEntry(0, ['food'])).toThrow('Mood score must be an integer between 1 and 5.');
    expect(() => handleAddEntry(6, ['food'])).toThrow('Mood score must be an integer between 1 and 5.');
    expect(() => handleAddEntry(3.5, ['food'])).toThrow('Mood score must be an integer between 1 and 5.');
  });

  it('should filter out invalid factors', () => {
    // # Mock rationale: Using a fixed timestamp for deterministic testing.
    const mockDateNow = jest.spyOn(Date, 'now').mockReturnValue(1678886400000);

    const consoleWarnSpy = jest.spyOn(console, 'warn').mockImplementation(() => {});
    handleAddEntry(3, ['food', 'invalid_factor', 'social']);
    const entries = getMoodEntries();
    expect(entries[0].factors).toEqual(['food', 'social']);
    expect(consoleWarnSpy).toHaveBeenCalledWith('Warning: Some provided factors were invalid and ignored.');
    consoleWarnSpy.mockRestore();
    mockDateNow.mockRestore();
  });
});

describe('generateEmotionalReport', () => {
  it('should return an empty report if no entries for the day', () => {
    // # Mock rationale: Using a fixed date for deterministic testing.
    const reportDate = new Date('2023-03-15T12:00:00Z');
    const report = generateEmotionalReport(reportDate);
    expect(report).toEqual({
      date: '2023-03-15',
      averageMood: 0,
      moodTrend: 'stable',
      dominantPositiveFactors: [],
      dominantNegativeFactors: [],
      recommendation: 'No mood data for this day. Encourage sharing!',
    });
  });

  it('should generate a report for a single entry', () => {
    // # Mock rationale: Using fixed timestamps for deterministic testing.
    const mockDateNow = jest.spyOn(Date, 'now');
    mockDateNow.mockReturnValueOnce(new Date('2023-03-15T10:00:00Z').getTime());
    handleAddEntry(5, ['resource_gain', 'social'], 'Found a new friend and some tech!');

    const reportDate = new Date('2023-03-15T12:00:00Z');
    const report = generateEmotionalReport(reportDate);

    expect(report.date).toBe('2023-03-15');
    expect(report.averageMood).toBe(5);
    expect(report.moodTrend).toBe('stable'); // No previous day data
    expect(report.dominantPositiveFactors).toEqual(['resource_gain', 'social']);
    expect(report.dominantNegativeFactors).toEqual([]);
    expect(report.recommendation).toContain('Morale is high!');

    mockDateNow.mockRestore();
  });

  it('should generate a report with multiple entries and calculate average mood', () => {
    // # Mock rationale: Using fixed timestamps for deterministic testing.
    const mockDateNow = jest.spyOn(Date, 'now');
    mockDateNow.mockReturnValueOnce(new Date('2023-03-15T08:00:00Z').getTime());
    handleAddEntry(4, ['food', 'shelter']);
    mockDateNow.mockReturnValueOnce(new Date('2023-03-15T12:00:00Z').getTime());
    handleAddEntry(2, ['weather', 'anomaly']);
    mockDateNow.mockReturnValueOnce(new Date('2023-03-15T16:00:00Z').getTime());
    handleAddEntry(3, ['social']);

    const reportDate = new Date('2023-03-15T20:00:00Z');
    const report = generateEmotionalReport(reportDate);

    expect(report.date).toBe('2023-03-15');
    expect(report.averageMood).toBeCloseTo(3); // (4+2+3)/3 = 3
    expect(report.moodTrend).toBe('stable');
    expect(report.dominantPositiveFactors).toEqual(['food', 'shelter', 'social']); // All had 1 positive count
    expect(report.dominantNegativeFactors).toEqual(['weather', 'anomaly']); // Both had 1 negative count
    expect(report.recommendation).toContain('Morale is stable.');

    mockDateNow.mockRestore();
  });

  it('should correctly identify dominant factors with varying scores', () => {
    // # Mock rationale: Using fixed timestamps for deterministic testing.
    const mockDateNow = jest.spyOn(Date, 'now');
    mockDateNow.mockReturnValueOnce(new Date('2023-03-15T08:00:00Z').getTime());
    handleAddEntry(5, ['food', 'social']); // +food, +social
    mockDateNow.mockReturnValueOnce(new Date('2023-03-15T10:00:00Z').getTime());
    handleAddEntry(1, ['weather', 'resource_loss']); // -weather, -resource_loss
    mockDateNow.mockReturnValueOnce(new Date('2023-03-15T12:00:00Z').getTime());
    handleAddEntry(4, ['food', 'shelter']); // +food, +shelter
    mockDateNow.mockReturnValueOnce(new Date('2023-03-15T14:00:00Z').getTime());
    handleAddEntry(2, ['weather', 'safety']); // -weather, -safety
    mockDateNow.mockReturnValueOnce(new Date('2023-03-15T16:00:00Z').getTime());
    handleAddEntry(3, ['social']); // +social

    const reportDate = new Date('2023-03-15T20:00:00Z');
    const report = generateEmotionalReport(reportDate);

    expect(report.date).toBe('2023-03-15');
    expect(report.averageMood).toBeCloseTo(3); // (5+1+4+2+3)/5 = 3
    expect(report.dominantPositiveFactors.sort()).toEqual(['food', 'social'].sort()); // food:2, social:2, shelter:1
    expect(report.dominantNegativeFactors.sort()).toEqual(['weather'].sort()); // weather:2, resource_loss:1, safety:1
    expect(report.recommendation).toContain('Morale is stable.');

    mockDateNow.mockRestore();
  });

  it('should determine mood trend (rising)', () => {
    // # Mock rationale: Using fixed timestamps for deterministic testing.
    const mockDateNow = jest.spyOn(Date, 'now');

    // Previous day (2023-03-14)
    mockDateNow.mockReturnValueOnce(new Date('2023-03-14T10:00:00Z').getTime());
    handleAddEntry(2, ['weather']); // Avg: 2
    mockDateNow.mockReturnValueOnce(new Date('2023-03-14T14:00:00Z').getTime());
    handleAddEntry(3, ['food']); // Avg: (2+3)/2 = 2.5

    // Current day (2023-03-15)
    mockDateNow.mockReturnValueOnce(new Date('2023-03-15T10:00:00Z').getTime());
    handleAddEntry(4, ['social']); // Avg: 4
    mockDateNow.mockReturnValueOnce(new Date('2023-03-15T14:00:00Z').getTime());
    handleAddEntry(5, ['resource_gain']); // Avg: (4+5)/2 = 4.5

    const reportDate = new Date('2023-03-15T20:00:00Z');
    const report = generateEmotionalReport(reportDate);

    expect(report.date).toBe('2023-03-15');
    expect(report.averageMood).toBe(4.5);
    expect(report.moodTrend).toBe('rising');
    expect(report.recommendation).toContain('Morale is high!');

    mockDateNow.mockRestore();
  });

  it('should determine mood trend (falling)', () => {
    // # Mock rationale: Using fixed timestamps for deterministic testing.
    const mockDateNow = jest.spyOn(Date, 'now');

    // Previous day (2023-03-14)
    mockDateNow.mockReturnValueOnce(new Date('2023-03-14T10:00:00Z').getTime());
    handleAddEntry(5, ['resource_gain']); // Avg: 5
    mockDateNow.mockReturnValueOnce(new Date('2023-03-14T14:00:00Z').getTime());
    handleAddEntry(4, ['social']); // Avg: (5+4)/2 = 4.5

    // Current day (2023-03-15)
    mockDateNow.mockReturnValueOnce(new Date('2023-03-15T10:00:00Z').getTime());
    handleAddEntry(2, ['weather']); // Avg: 2
    mockDateNow.mockReturnValueOnce(new Date('2023-03-15T14:00:00Z').getTime());
    handleAddEntry(1, ['anomaly']); // Avg: (2+1)/2 = 1.5

    const reportDate = new Date('2023-03-15T20:00:00Z');
    const report = generateEmotionalReport(reportDate);

    expect(report.date).toBe('2023-03-15');
    expect(report.averageMood).toBe(1.5);
    expect(report.moodTrend).toBe('falling');
    expect(report.recommendation).toContain('Morale is critical.');

    mockDateNow.mockRestore();
  });

  it('should determine mood trend (stable)', () => {
    // # Mock rationale: Using fixed timestamps for deterministic testing.
    const mockDateNow = jest.spyOn(Date, 'now');

    // Previous day (2023-03-14)
    mockDateNow.mockReturnValueOnce(new Date('2023-03-14T10:00:00Z').getTime());
    handleAddEntry(3, ['food']); // Avg: 3
    mockDateNow.mockReturnValueOnce(new Date('2023-03-14T14:00:00Z').getTime());
    handleAddEntry(3, ['shelter']); // Avg: (3+3)/2 = 3

    // Current day (2023-03-15)
    mockDateNow.mockReturnValueOnce(new Date('2023-03-15T10:00:00Z').getTime());
    handleAddEntry(3, ['social']); // Avg: 3
    mockDateNow.mockReturnValueOnce(new Date('2023-03-15T14:00:00Z').getTime());
    handleAddEntry(3, ['safety']); // Avg: (3+3)/2 = 3

    const reportDate = new Date('2023-03-15T20:00:00Z');
    const report = generateEmotionalReport(reportDate);

    expect(report.date).toBe('2023-03-15');
    expect(report.averageMood).toBe(3);
    expect(report.moodTrend).toBe('stable');
    expect(report.recommendation).toContain('Morale is stable.');

    mockDateNow.mockRestore();
  });
});
