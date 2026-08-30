import { analyzeSentiment, getMoodColor } from '../src/components/SentimentAnalyzer';

describe('SentimentAnalyzer', () => {
  // Mock rationale: The sentiment analysis relies on predefined word lists.
  // These lists are internal to the module and do not require external dependencies.
  // The tests directly call the functions with various string inputs,
  // ensuring deterministic results based on the fixed word lists.

  test('should return 0 for empty or neutral text', () => {
    expect(analyzeSentiment('')).toBe(0);
    expect(analyzeSentiment('The quick brown fox jumps over the lazy dog.')).toBe(0);
    expect(analyzeSentiment('This is a test sentence.')).toBe(0);
  });

  test('should return positive score for positive text', () => {
    expect(analyzeSentiment('We have hope and joy, together we will build.')).toBe(3);
    expect(analyzeSentiment('Love, peace, and progress are good.')).toBe(4);
    expect(analyzeSentiment('Strong community, safe haven, happy survivors.')).toBe(4);
    expect(analyzeSentiment('This is a very positive message full of love, hope, joy, peace, calm, safe, good, happy, strong, together, build, grow, thrive, survive, light, warm, friend, help, share, progress, bright, success, victory, comfort, secure, flourish, optimism, resilience, unity, trust.')).toBe(30); // Max positive score
  });

  test('should return negative score for negative text', () => {
    expect(analyzeSentiment('There is fear and despair, danger is a threat.')).toBe(-4);
    expect(analyzeSentiment('Sad, alone, broken, lost, cold, hungry.')).toBe(-6);
    expect(analyzeSentiment('Enemy attack will ruin us in the dark struggle.')).toBe(-6);
    expect(analyzeSentiment('This is a very negative message full of fear, despair, danger, threat, sad, alone, broken, lost, cold, hungry, enemy, fight, attack, ruin, dark, struggle, pain, worry, anxious, stress, crisis, collapse, desperate, hostile, gloom, desolation, famine, sickness, betrayal, doubt.')).toBe(-30); // Max negative score
  });

  test('should return mixed score for mixed text', () => {
    expect(analyzeSentiment('Despite the fear, we have hope.')).toBe(0); // -1 + 1
    expect(analyzeSentiment('Danger is real, but we are strong and together.')).toBe(1); // -1 + 2
    expect(analyzeSentiment('The struggle is hard, but we will survive and thrive.')).toBe(2); // -1 + 2 + 1
  });

  test('should be case-insensitive', () => {
    expect(analyzeSentiment('LOVE and hope.')).toBe(2);
    expect(analyzeSentiment('FEAR and despair.')).toBe(-2);
  });

  test('getMoodColor should return correct colors for scores', () => {
    expect(getMoodColor(10)).toBe("#4CAF50"); // Strong Positive
    expect(getMoodColor(5)).toBe("#4CAF50"); // Strong Positive boundary
    expect(getMoodColor(4)).toBe("#8BC34A"); // Moderate Positive
    expect(getMoodColor(2)).toBe("#8BC34A"); // Moderate Positive boundary
    expect(getMoodColor(1)).toBe("#CDDC39"); // Mild Positive
    expect(getMoodColor(0)).toBe("#9E9E9E"); // Neutral
    expect(getMoodColor(-1)).toBe("#FFC107"); // Mild Negative
    expect(getMoodColor(-2)).toBe("#FF9800"); // Moderate Negative boundary
    expect(getMoodColor(-4)).toBe("#FF9800"); // Moderate Negative
    expect(getMoodColor(-5)).toBe("#F44336"); // Strong Negative boundary
    expect(getMoodColor(-10)).toBe("#F44336"); // Strong Negative
  });
});
