import { analyze } from '../src/SentimentAnalyzer';

describe('SentimentAnalyzer', () => {
  // Mock rationale: The sentiment analysis is rule-based and self-contained.
  // No external dependencies or APIs are called, so direct testing of the logic is sufficient.
  // The tests cover various inputs to ensure the rules are applied correctly.

  test('should return neutral for empty or whitespace-only text', () => {
    expect(analyze('')).toEqual({ sentiment: 'neutral', score: 0, description: 'Awaiting input...' });
    expect(analyze('   ')).toEqual({ sentiment: 'neutral', score: 0, description: 'Awaiting input...' });
  });

  test('should return positive for clearly positive text', () => {
    const result = analyze('This is a great day! I feel happy and full of hope.');
    expect(result.sentiment).toBe('positive');
    expect(result.score).toBeGreaterThan(0);
    expect(result.description).toBe('Radiant with hope!');
  });

  test('should return negative for clearly negative text', () => {
    const result = analyze('I feel sad and despair. This is a terrible situation.');
    expect(result.sentiment).toBe('negative');
    expect(result.score).toBeLessThan(0);
    expect(result.description).toBe('Shadows of despair...');
  });

  test('should return neutral for mixed or ambiguous text', () => {
    const result = analyze('The weather is bad but I am strong.'); // bad (-1), strong (+1) -> score 0
    expect(result.sentiment).toBe('neutral');
    expect(result.score).toBe(0);
    expect(result.description).toBe('Feeling balanced.');
  });

  test('should return neutral for text with no sentiment words', () => {
    const result = analyze('The quick brown fox jumps over the lazy dog.');
    expect(result.sentiment).toBe('neutral');
    expect(result.score).toBe(0);
    expect(result.description).toBe('Feeling balanced.');
  });

  test('should handle case insensitivity', () => {
    const result = analyze('GREAT day, but also a little SAD.');
    expect(result.sentiment).toBe('neutral'); // GREAT (+1), SAD (-1) -> score 0
    expect(result.score).toBe(0);
    expect(result.description).toBe('Feeling balanced.');
  });

  test('should return positive for text with multiple positive words', () => {
    const result = analyze('We will thrive and survive! Hope is strong!');
    expect(result.sentiment).toBe('positive');
    expect(result.score).toBeGreaterThan(0);
    expect(result.description).toBe('Radiant with hope!');
  });

  test('should return negative for text with multiple negative words', () => {
    const result = analyze('Danger and despair lead to ruin and defeat.');
    expect(result.sentiment).toBe('negative');
    expect(result.score).toBeLessThan(0);
    expect(result.description).toBe('Shadows of despair...');
  });

  test('should differentiate between mild and strong positive/negative', () => {
    let result = analyze('This is good.');
    expect(result.sentiment).toBe('positive');
    expect(result.description).toBe('Optimistic vibrations.');

    result = analyze('This is good, great, and excellent!');
    expect(result.sentiment).toBe('positive');
    expect(result.description).toBe('Radiant with hope!');

    result = analyze('This is bad.');
    expect(result.sentiment).toBe('negative');
    expect(result.description).toBe('A touch of gloom.');

    result = analyze('This is bad, terrible, and awful!');
    expect(result.sentiment).toBe('negative');
    expect(result.description).toBe('Shadows of despair...');
  });
});
