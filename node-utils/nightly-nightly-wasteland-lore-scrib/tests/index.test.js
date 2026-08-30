const { generateLore, themes } = require('../src/index');

describe('generateLore', () => {
  const originalMathRandom = Math.random;

  beforeEach(() => {
    // Mock rationale: Ensure deterministic output for tests that rely on random selection.
    // We control Math.random to always return a predictable value.
    Math.random = jest.fn(() => 0.5); // Always pick the middle element for simplicity
  });

  afterEach(() => {
    Math.random = originalMathRandom;
  });

  test('should generate a single lore snippet with a specific theme', () => {
    const theme = 'ruins';
    const expectedLore = themes[theme][Math.floor(0.5 * themes[theme].length)]; // Expected based on mock
    const lore = generateLore(theme);
    expect(lore).toBe(expectedLore);
    expect(lore.split('\n\n').length).toBe(1);
  });

  test('should generate multiple lore snippets with a specific theme', () => {
    const theme = 'mutants';
    const count = 3;
    const expectedSnippet = themes[theme][Math.floor(0.5 * themes[theme].length)]; // Expected based on mock
    const lore = generateLore(theme, count);
    const snippets = lore.split('\n\n');
    expect(snippets.length).toBe(count);
    snippets.forEach(snippet => {
      expect(snippet).toBe(expectedSnippet);
    });
  });

  test('should generate a single lore snippet with a random theme when no theme is specified', () => {
    // Mock rationale: Control which 'random' theme is picked for deterministic testing.
    // We mock Object.keys and Math.random to ensure a specific theme is chosen.
    const mockThemes = ['hope', 'despair', 'technology'];
    jest.spyOn(Object, 'keys').mockReturnValue(mockThemes);
    Math.random.mockReturnValueOnce(0.5); // Picks 'despair' from mockThemes

    const expectedTheme = 'despair';
    const expectedLore = themes[expectedTheme][Math.floor(0.5 * themes[expectedTheme].length)];
    const lore = generateLore();
    expect(lore).toBe(expectedLore);
    expect(lore.split('\n\n').length).toBe(1);

    Object.keys.mockRestore(); // Clean up spy
  });

  test('should return "No lore themes available." if themes object is empty', () => {
    // Mock rationale: Temporarily empty the themes object to test edge case.
    const originalThemes = { ...themes };
    for (const key in themes) {
      delete themes[key];
    }
    const lore = generateLore('any');
    expect(lore).toBe('No lore themes available.');
    Object.assign(themes, originalThemes); // Restore themes
  });

  test('should handle invalid theme gracefully by picking a random one', () => {
    const invalidTheme = 'nonexistent';
    // Mock rationale: Control which 'random' theme is picked when an invalid one is provided.
    const mockThemes = ['ruins', 'nature'];
    jest.spyOn(Object, 'keys').mockReturnValue(mockThemes);
    Math.random.mockReturnValueOnce(0.0); // Picks 'ruins' from mockThemes

    const expectedTheme = 'ruins';
    const expectedLore = themes[expectedTheme][Math.floor(0.5 * themes[expectedTheme].length)];
    const lore = generateLore(invalidTheme);
    expect(lore).toBe(expectedLore);

    Object.keys.mockRestore();
  });

  test('should return "No lore themes available." if a valid theme has no lore snippets', () => {
    // Mock rationale: Temporarily modify a theme to have no snippets to test edge case.
    const originalRuins = [...themes.ruins];
    themes.ruins.length = 0; // Empty the array

    const lore = generateLore('ruins');
    expect(lore).toBe('No lore themes available.'); // Updated logic in src/index.js

    themes.ruins = originalRuins; // Restore original snippets
  });
});
