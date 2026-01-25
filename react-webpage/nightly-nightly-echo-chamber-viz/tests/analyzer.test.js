import { analyzeEchoes, defaultStopwords } from '../src/utils/analyzer';

describe('analyzeEchoes', () => {
  // Mock rationale: Using predefined event data to ensure deterministic and offline testing.
  // This avoids reliance on external data sources or dynamic content generation.

  test('should correctly count words in simple messages', () => {
    const events = [
      { timestamp: '2024-07-20T10:00:00Z', message: 'The quick brown fox jumps over the lazy dog.' },
      { timestamp: '2024-07-20T10:05:00Z', message: 'A quick brown fox is quick.' }
    ];
    const expected = {
      quick: 3,
      brown: 2,
      fox: 2,
      jumps: 1,
      over: 1,
      lazy: 1,
      dog: 1
    };
    // Filter out default stopwords for comparison
    const result = analyzeEchoes(events, defaultStopwords);
    expect(result).toEqual(expected);
  });

  test('should handle empty messages and events array', () => {
    const events1 = [];
    expect(analyzeEchoes(events1)).toEqual({});

    const events2 = [
      { timestamp: '2024-07-20T10:00:00Z', message: '' },
      { timestamp: '2024-07-20T10:05:00Z', message: '   ' }
    ];
    expect(analyzeEchoes(events2)).toEqual({});
  });

  test('should ignore stopwords and short words', () => {
    const events = [
      { timestamp: '2024-07-20T11:00:00Z', message: 'This is a test message with many common words.' },
      { timestamp: '2024-07-20T11:01:00Z', message: 'Another test, but this one has fewer words.' }
    ];
    const expected = {
      test: 2,
      message: 1,
      many: 1,
      common: 1,
      another: 1,
      fewer: 1
    };
    const result = analyzeEchoes(events, defaultStopwords);
    expect(result).toEqual(expected);
  });

  test('should be case-insensitive', () => {
    const events = [
      { timestamp: '2024-07-20T12:00:00Z', message: 'Whispers in the Void' },
      { timestamp: '2024-07-20T12:01:00Z', message: 'whispers of the void' }
    ];
    const expected = {
      whispers: 2,
      void: 2
    };
    const result = analyzeEchoes(events, defaultStopwords);
    expect(result).toEqual(expected);
  });

  test('should handle custom stopwords', () => {
    const events = [
      { timestamp: '2024-07-20T13:00:00Z', message: 'The anomaly detected, anomaly confirmed.' }
    ];
    const customStopwords = [...defaultStopwords, 'anomaly'];
    const expected = {
      detected: 1,
      confirmed: 1
    };
    const result = analyzeEchoes(events, customStopwords);
    expect(result).toEqual(expected);
  });

  test('should handle messages with special characters', () => {
    const events = [
      { timestamp: '2024-07-20T14:00:00Z', message: 'Alert! System-critical failure (code: 404).' }
    ];
    const expected = {
      alert: 1,
      system: 1,
      critical: 1,
      failure: 1,
      code: 1,
      404: 1
    };
    const result = analyzeEchoes(events, defaultStopwords);
    expect(result).toEqual(expected);
  });
});
