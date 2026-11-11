import { convertToCosmicDate, CosmicDate } from '../src/cosmicConverter';

describe('convertToCosmicDate', () => {
  it('should convert a valid date string to a cosmic date for 2023-01-15', () => {
    const dateString = '2023-01-15';
    const cosmicDate = convertToCosmicDate(dateString);

    expect(cosmicDate).not.toBeNull();
    expect(cosmicDate?.earthDate.toISOString().split('T')[0]).toBe('2023-01-15');
    // (2023 - 2000) % 12 = 23 % 12 = 11. Index 11 is "Celestial Alignment".
    expect(cosmicDate?.stellarCycle.name).toBe("Celestial Alignment");
    // Day 15 of year. (15 / 365) * 8 = 0.32... -> floor 0. Index 0 is "New Moon's Promise".
    expect(cosmicDate?.lunarPhase.name).toBe("New Moon's Promise");
    // (2023 - 2000) / 100 = 0.23 -> floor 0. Index 0 is "Era of the Great Silence".
    expect(cosmicDate?.galacticEra.name).toBe("Era of the Great Silence");
    expect(cosmicDate?.cosmicDay).toBe(15);
    expect(cosmicDate?.fullCosmicString).toContain("🔭 Celestial Alignment");
    expect(cosmicDate?.fullCosmicString).toContain("🌑 New Moon's Promise");
    expect(cosmicDate?.fullCosmicString).toContain("Cosmic Day 15 (Day 15 of the Celestial Alignment)");
    expect(cosmicDate?.fullCosmicString).toContain("within the Era of the Great Silence.");
  });

  it('should handle dates in a leap year (2024-07-20)', () => {
    const dateString = '2024-07-20';
    const cosmicDate = convertToCosmicDate(dateString);

    expect(cosmicDate).not.toBeNull();
    expect(cosmicDate?.earthDate.toISOString().split('T')[0]).toBe('2024-07-20');
    // (2024 - 2000) % 12 = 24 % 12 = 0. Index 0 is "Nebula's Embrace".
    expect(cosmicDate?.stellarCycle.name).toBe("Nebula's Embrace");
    // Day of year for 2024-07-20 (leap year): 31+29+31+30+31+30+20 = 202.
    expect(cosmicDate?.cosmicDay).toBe(202);
    // Lunar phase for day 202: (202 / 366) * 8 = 4.41... -> floor 4. Index 4 is "Full Moon's Radiance".
    expect(cosmicDate?.lunarPhase.name).toBe("Full Moon's Radiance");
    // (2024 - 2000) / 100 = 0.24 -> floor 0. Index 0 is "Era of the Great Silence".
    expect(cosmicDate?.galacticEra.name).toBe("Era of the Great Silence");
  });

  it('should return null for an invalid date string', () => {
    const dateString = 'not-a-date';
    const cosmicDate = convertToCosmicDate(dateString);
    expect(cosmicDate).toBeNull();
  });

  it('should return null for an empty date string', () => {
    const dateString = '';
    const cosmicDate = convertToCosmicDate(dateString);
    expect(cosmicDate).toBeNull();
  });

  it('should handle a future date for era calculation (2250-11-01)', () => {
    const dateString = '2250-11-01';
    const cosmicDate = convertToCosmicDate(dateString);

    expect(cosmicDate).not.toBeNull();
    // (2250 - 2000) / 100 = 2.5 -> floor 2. Index 2 is "Era of the Void's Awakening".
    expect(cosmicDate?.galacticEra.name).toBe("Era of the Void's Awakening");
  });

  it('should handle a date far in the future, capping era (2500-05-05)', () => {
    const dateString = '2500-05-05';
    const cosmicDate = convertToCosmicDate(dateString);

    expect(cosmicDate).not.toBeNull();
    // (2500 - 2000) / 100 = 5. Capped at GALACTIC_ERAS.length - 1 (index 3). Index 3 is "Era of the Whispering Galaxies".
    expect(cosmicDate?.galacticEra.name).toBe("Era of the Whispering Galaxies");
  });

  it('should handle a date before 2000, adjusting stellar cycle (1999-12-31)', () => {
    const dateString = '1999-12-31';
    const cosmicDate = convertToCosmicDate(dateString);

    expect(cosmicDate).not.toBeNull();
    // (1999 - 2000) % 12 = -1 % 12 = -1. Adjusted: -1 + 12 = 11. Index 11 is "Celestial Alignment".
    expect(cosmicDate?.stellarCycle.name).toBe("Celestial Alignment");
    // (1999 - 2000) / 100 = -0.01 -> floor -1. Capped at index 0. "Era of the Great Silence".
    expect(cosmicDate?.galacticEra.name).toBe("Era of the Great Silence");
  });
});
