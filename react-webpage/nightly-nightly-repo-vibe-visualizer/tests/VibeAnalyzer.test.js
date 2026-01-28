import { analyzeVibe } from '../src/VibeAnalyzer';

describe('analyzeVibe', () => {
  // # Mock rationale: The VibeAnalyzer operates purely on string inputs and internal keyword lists.
  // # No external dependencies or side effects are involved, making it inherently deterministic and offline.
  // # The test cases provide various arrays of strings to simulate different sets of contributions.

  test('should return Optimistic for predominantly optimistic contributions', () => {
    const contributions = [
      'feat: add new user registration flow',
      'improve: performance of data fetching',
      'release: v1.0.0 to production',
      'docs: update README'
    ];
    expect(analyzeVibe(contributions)).toBe('Optimistic');
  });

  test('should return Chaotic for predominantly chaotic contributions', () => {
    const contributions = [
      'fix(bug): critical error in payment gateway',
      'urgent: hotfix for server crash',
      'refactor: clean up old code',
      'style: linting fixes'
    ];
    expect(analyzeVibe(contributions)).toBe('Chaotic');
  });

  test('should return Serene for predominantly serene contributions', () => {
    const contributions = [
      'refactor: consolidate utility functions',
      'chore: update npm packages',
      'test: add unit tests for new module',
      'feat: add new feature'
    ];
    expect(analyzeVibe(contributions)).toBe('Serene');
  });

  test('should return Mysterious for contributions with no strong vibe or mixed', () => {
    const contributions = [
      'update: dependencies',
      'adjust: UI spacing',
      'tweak: button color',
      'revert: accidental commit'
    ];
    expect(analyzeVibe(contributions)).toBe('Mysterious');
  });

  test('should handle empty contributions array', () => {
    const contributions = [];
    expect(analyzeVibe(contributions)).toBe('Mysterious'); // Default vibe
  });

  test('should handle contributions with mixed vibes, prioritizing based on count', () => {
    const contributions = [
      'feat: new dashboard widget', // Optimistic
      'fix: broken link',           // Chaotic
      'refactor: API client',       // Serene
      'add: user settings',         // Optimistic
      'bug: display issue',         // Chaotic
      'docs: usage guide'           // Serene
    ];
    // Optimistic: 2, Chaotic: 2, Serene: 2, Mysterious: 0
    // Due to tie-breaking order (Optimistic > Chaotic > Serene > Mysterious), Optimistic should win.
    expect(analyzeVibe(contributions)).toBe('Optimistic');
  });

  test('should handle contributions with mixed vibes, where one is clearly dominant', () => {
    const contributions = [
      'fix: critical bug in production',
      'fix: another bug',
      'urgent: hotfix',
      'feat: minor improvement',
      'docs: typo fix'
    ];
    // Chaotic: 3, Optimistic: 1, Serene: 1
    expect(analyzeVibe(contributions)).toBe('Chaotic');
  });

  test('should be case-insensitive', () => {
    const contributions = [
      'FEAT: big new thing',
      'Fix: small issue',
      'Chore: cleanup'
    ];
    // Optimistic: 1, Chaotic: 1, Serene: 1
    expect(analyzeVibe(contributions)).toBe('Optimistic'); // Due to tie-breaking
  });

  test('should count each contribution once for a vibe category, even with multiple keywords', () => {
    const contributions = [
      'fix(bug): resolve critical issue and hotfix it',
      'add new feature',
      'refactor and clean up'
    ];
    // Chaotic: 1 (fix, bug, hotfix are all in one string, but only increments Chaotic once)
    // Optimistic: 1
    // Serene: 1
    expect(analyzeVibe(contributions)).toBe('Optimistic'); // Due to tie-breaking
  });
});
