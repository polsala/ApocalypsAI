import { analyzeSentiment } from '../src/SentimentAnalyzer';

describe('SentimentAnalyzer', () => {
  // Mock rationale: The SentimentAnalyzer operates on plain string arrays.
  // Mocking allows for deterministic testing without external dependencies or complex setup.

  test('should return "Neutral" for empty messages', () => {
    expect(analyzeSentiment([])).toBe('Neutral');
  });

  test('should return "Neutral" for messages with no specific keywords', () => {
    const messages = [
      "Just a general update.",
      "Checking in on the status."
    ];
    expect(analyzeSentiment(messages)).toBe('Neutral');
  });

  test('should return "Tense" for messages containing bug/error keywords', () => {
    const messages = [
      "Found a critical bug.",
      "An error occurred during compilation.",
      "The system failed to start."
    ];
    expect(analyzeSentiment(messages)).toBe('Tense');
  });

  test('should return "Active" for messages containing feature/new/add keywords', () => {
    const messages = [
      "Implementing a new feature.",
      "Adding support for more data types.",
      "Working on the next sprint tasks."
    ];
    expect(analyzeSentiment(messages)).toBe('Active');
  });

  test('should return "Calm" for messages containing fix/resolve/done keywords', () => {
    const messages = [
      "Fixed the minor issue.",
      "Resolved all pending tasks.",
      "Documentation update is done."
    ];
    expect(analyzeSentiment(messages)).toBe('Calm');
  });

  test('should return "Joyful" for messages containing positive keywords', () => {
    const messages = [
      "This is awesome work!",
      "Great progress on the project.",
      "Feeling happy with the results."
    ];
    expect(analyzeSentiment(messages)).toBe('Joyful');
  });

  test('should prioritize dominant mood (e.g., more tense than active)', () => {
    const messages = [
      "Found a critical bug.", // Tense
      "An error occurred.",     // Tense
      "Implementing a new feature.", // Active
      "This is awesome work!" // Joyful
    ];
    expect(analyzeSentiment(messages)).toBe('Tense'); // Tense: 2, Active: 1, Joyful: 1
  });

  test('should handle mixed sentiments with equal scores and apply tie-breaking', () => {
    const messages = [
      "Found a bug.", // Tense
      "Adding a feature.", // Active
      "Resolved an issue.", // Calm
      "Great work!" // Joyful
    ];
    // All non-neutral moods have a score of 1. The explicit iteration order in analyzeSentiment
    // (Tense, Active, Calm, Joyful) determines the tie-break. 'Tense' is first.
    expect(analyzeSentiment(messages)).toBe('Tense');
  });

  test('should handle messages with multiple keywords for different moods, counting only one per message', () => {
    const messages = [
      "Fixed a bug and added a new feature. Great job!"
    ];
    // The analyzer counts only one mood per message for simplicity.
    // 'bug' is found first for 'Tense'. So 'Tense' gets 1. Other keywords in the same message are ignored for other moods.
    expect(analyzeSentiment(messages)).toBe('Tense');
  });

  test('should handle messages with multiple keywords for the same mood, counting once per message', () => {
    const messages = [
      "Found a critical bug and an unexpected error."
    ];
    // Both 'critical bug' and 'unexpected error' contribute to 'Tense'.
    // The current logic increments score once per message if *any* keyword for that mood is found.
    // So, 'Tense' score will be 1.
    expect(analyzeSentiment(messages)).toBe('Tense');
  });
});
