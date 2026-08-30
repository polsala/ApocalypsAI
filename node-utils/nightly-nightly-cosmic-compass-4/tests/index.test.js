const { getLunarPhase, getZodiacSign, getPlanetaryInfluence, getCosmicGuidance } = require('../src/cosmicData');
const { runCosmicCompass } = require('../src/index');

// Mock console.log to capture output
const mockConsoleLog = jest.spyOn(console, 'log').mockImplementation(() => {});

// Mock rationale: Jest's `spyOn` is used to capture console output without affecting the actual console.
// This allows for deterministic testing of what the CLI prints.

describe('Cosmic Data Functions', () => {
  // Mock rationale: Mocking the Date object ensures deterministic test results for date-dependent functions.
  // This prevents tests from failing due to changes in the current date.
  const mockDate = (year, month, day) => {
    const mock = new Date(year, month - 1, day); // month is 0-indexed in Date constructor
    jest.spyOn(global, 'Date').mockImplementation(() => mock);
  };

  afterEach(() => {
    jest.restoreAllMocks(); // Restore Date and console.log mocks after each test
  });

  test('getLunarPhase returns correct phase for various dates', () => {
    mockDate(2023, 1, 1); // Jan 1st
    expect(getLunarPhase(new Date())).toBe('New Moon');
    mockDate(2023, 1, 5); // Jan 5th
    expect(getLunarPhase(new Date())).toBe('Waxing Crescent');
    mockDate(2023, 1, 17); // Jan 17th
    expect(getLunarPhase(new Date())).toBe('Full Moon');
    mockDate(2023, 1, 29); // Jan 29th
    expect(getLunarPhase(new Date())).toBe('Waning Crescent');
  });

  test('getZodiacSign returns correct sign for various dates', () => {
    mockDate(2023, 1, 15); // Jan 15th
    expect(getZodiacSign(new Date())).toBe('Capricorn');
    mockDate(2023, 3, 25); // Mar 25th
    expect(getZodiacSign(new Date())).toBe('Aries');
    mockDate(2023, 10, 30); // Oct 30th
    expect(getZodiacSign(new Date())).toBe('Scorpio');
    mockDate(2023, 12, 25); // Dec 25th
    expect(getZodiacSign(new Date())).toBe('Capricorn');
  });

  test('getPlanetaryInfluence returns correct influence for each day of the week', () => {
    mockDate(2023, 1, 1); // Sunday
    expect(getPlanetaryInfluence(new Date())).toEqual({ planet: 'Sun', influence: 'Vitality & Leadership' });
    mockDate(2023, 1, 2); // Monday
    expect(getPlanetaryInfluence(new Date())).toEqual({ planet: 'Moon', influence: 'Emotion & Intuition' });
    mockDate(2023, 1, 3); // Tuesday
    expect(getPlanetaryInfluence(new Date())).toEqual({ planet: 'Mars', influence: 'Action & Drive' });
    mockDate(2023, 1, 4); // Wednesday
    expect(getPlanetaryInfluence(new Date())).toEqual({ planet: 'Mercury', influence: 'Communication & Intellect' });
    mockDate(2023, 1, 5); // Thursday
    expect(getPlanetaryInfluence(new Date())).toEqual({ planet: 'Jupiter', influence: 'Growth & Expansion' });
    mockDate(2023, 1, 6); // Friday
    expect(getPlanetaryInfluence(new Date())).toEqual({ planet: 'Venus', influence: 'Harmony & Connection' });
    mockDate(2023, 1, 7); // Saturday
    expect(getPlanetaryInfluence(new Date())).toEqual({ planet: 'Saturn', influence: 'Discipline & Structure' });
  });

  test('getCosmicGuidance provides specific guidance for known combinations', () => {
    // Test New Moon + Aries combo
    const guidance1 = getCosmicGuidance('New Moon', 'Aries', { planet: 'Mars', influence: 'Action & Drive' });
    expect(guidance1.direction).toBe('Bold Beginnings & Energetic Action');
    expect(guidance1.activity).toContain('Initiate new projects with courage');

    // Test Full Moon + Libra combo
    const guidance2 = getCosmicGuidance('Full Moon', 'Libra', { planet: 'Venus', influence: 'Harmony & Connection' });
    expect(guidance2.direction).toBe('Relationship Harmony & Balance');
    expect(guidance2.activity).toContain('Seek balance in partnerships');

    // Test Scorpio + Mars combo (general case)
    const guidance3 = getCosmicGuidance('Waxing Gibbous', 'Scorpio', { planet: 'Mars', influence: 'Action & Drive' });
    expect(guidance3.direction).toBe('Introspection & Transformation');
    expect(guidance3.activity).toContain('Reflect on your inner landscape');

    // Test Taurus + Venus combo (general case)
    const guidance4 = getCosmicGuidance('Full Moon', 'Taurus', { planet: 'Venus', influence: 'Harmony & Connection' });
    expect(guidance4.direction).toBe('Stability & Comfort');
    expect(guidance4.activity).toContain('securing resources');

    // Test Gemini + Mercury combo (general case)
    const guidance5 = getCosmicGuidance('New Moon', 'Gemini', { planet: 'Mercury', influence: 'Communication & Intellect' });
    expect(guidance5.direction).toBe('Communication & Adaptability');
    expect(guidance5.activity).toContain('information gathering');

    // Test general guidance for unmatched combo
    const guidance6 = getCosmicGuidance('Waning Crescent', 'Leo', { planet: 'Jupiter', influence: 'Growth & Expansion' });
    expect(guidance6.direction).toContain('General Guidance');
    expect(guidance6.activity).toContain('Growth & Expansion');
  });
});

describe('runCosmicCompass CLI output', () => {
  afterEach(() => {
    jest.restoreAllMocks();
    mockConsoleLog.mockClear();
  });

  test('should print correct output for a specific date (e.g., Jan 1, 2023 - Sunday)', () => {
    // Mock rationale: Mocking Date to ensure consistent output for the CLI test.
    const mockDate = new Date(2023, 0, 1); // Jan 1, 2023 is a Sunday
    jest.spyOn(global, 'Date').mockImplementation(() => mockDate);

    runCosmicCompass();

    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('🌌 Nightly Cosmic Compass 🌌'));
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Lunar Phase: New Moon'));
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Zodiac Sign: Capricorn'));
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Planetary Influence: Sun (Vitality & Leadership)'));
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Cosmic Direction: New Beginnings & Intention Setting'));
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Activity Suggestion: Plant seeds for future projects and set clear intentions. Clear out old clutter.'));
  });

  test('should print correct output for another specific date (e.g., Oct 25, 2023 - Wednesday)', () => {
    // Mock rationale: Mocking Date to ensure consistent output for the CLI test.
    const mockDate = new Date(2023, 9, 25); // Oct 25, 2023 is a Wednesday
    jest.spyOn(global, 'Date').mockImplementation(() => mockDate);

    runCosmicCompass();

    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('🌌 Nightly Cosmic Compass 🌌'));
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Lunar Phase: Waning Gibbous'));
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Zodiac Sign: Scorpio'));
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Planetary Influence: Mercury (Communication & Intellect)'));
    // This specific combination (Waning Gibbous + Scorpio + Mercury) falls into the general guidance for now
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Cosmic Direction: General Guidance: Communication & Intellect & Waning Gibbous energies.'));
    expect(mockConsoleLog).toHaveBeenCalledWith(expect.stringContaining('Activity Suggestion: Consider activities related to communication & intellect and the current waning gibbous phase.'));
  });
});
