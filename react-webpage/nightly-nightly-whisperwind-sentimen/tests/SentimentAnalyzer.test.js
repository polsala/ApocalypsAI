import SentimentAnalyzer from '../src/SentimentAnalyzer';

describe('SentimentAnalyzer', () => {
  // Mock rationale: The sentiment analysis is a simplified, keyword-based implementation.
  // For testing, we want to ensure our component correctly processes text based on its internal logic,
  // not necessarily test the accuracy of a complex NLP model. Mocking is not strictly needed here
  // as the logic is self-contained, but this comment serves to acknowledge the principle.

  test('should return "neutral" for empty or whitespace-only input', () => {
    expect(SentimentAnalyzer.analyze('')).toBe('neutral');
    expect(SentimentAnalyzer.analyze('   ')).toBe('neutral');
    expect(SentimentAnalyzer.analyze(null)).toBe('neutral');
    expect(SentimentAnalyzer.analyze(undefined)).toBe('neutral');
  });

  test('should return "hopeful" for strongly positive text', () => {
    expect(SentimentAnalyzer.analyze('We have hope for the future and will build together.')).toBe('hopeful');
    expect(SentimentAnalyzer.analyze('Joy and peace fill our hearts. We are strong.')).toBe('hopeful');
    expect(SentimentAnalyzer.analyze('Thrive and grow, good things are coming.')).toBe('hopeful');
  });

  test('should return "despair" for strongly negative text', () => {
    expect(SentimentAnalyzer.analyze('Fear and despair are overwhelming. Collapse is near.')).toBe('despair');
    expect(SentimentAnalyzer.analyze('The danger is immense, a real threat to our survival.')).toBe('despair');
    expect(SentimentAnalyzer.analyze('Sadness and crisis, we are weak and alone.')).toBe('despair');
  });

  test('should return "anxious" for mixed sentiment', () => {
    expect(SentimentAnalyzer.analyze('There is some hope, but also much fear.')).toBe('anxious');
    expect(SentimentAnalyzer.analyze('We are building, but the threat of collapse looms.')).toBe('anxious');
    expect(SentimentAnalyzer.analyze('A little joy, but also a lot of anxiety.')).toBe('anxious');
  });

  test('should return "anxious" for slightly positive or negative bias (not strong enough for hopeful/despair)', () => {
    expect(SentimentAnalyzer.analyze('We have hope.')).toBe('anxious'); // Only one positive keyword, not 1.5x negative
    expect(SentimentAnalyzer.analyze('There is danger.')).toBe('anxious'); // Only one negative keyword
    expect(SentimentAnalyzer.analyze('Good, but also bad.')).toBe('anxious'); // Equal positive/negative
  });

  test('should return "neutral" for text with no relevant keywords', () => {
    expect(SentimentAnalyzer.analyze('The quick brown fox jumps over the lazy dog.')).toBe('neutral');
    expect(SentimentAnalyzer.analyze('The sun rises in the east.')).toBe('neutral');
  });

  test('should be case-insensitive', () => {
    expect(SentimentAnalyzer.analyze('HOPE and JOY')).toBe('hopeful');
    expect(SentimentAnalyzer.analyze('FEAR and DESPAIR')).toBe('despair');
  });
});
