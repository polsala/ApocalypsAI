const { getTemporalGuidance } = require('../src/index');

describe('getTemporalGuidance', () => {
  // Mock rationale: We need to control the current date and time to test
  // time-dependent logic deterministically without relying on the actual system clock.

  // Helper to create a mock Date object for a specific year, month, day, and hour.
  // Month is 0-indexed (e.g., January is 0).
  const mockDate = (year, month, day, hour) => {
    return new Date(year, month, day, hour);
  };

  // Weekday (Monday-Friday) scenarios
  test('should suggest "Plan for the Future" in weekday morning (Monday 8 AM)', () => {
    const date = mockDate(2023, 0, 2, 8); // Monday, Jan 2, 2023, 8 AM
    const guidance = getTemporalGuidance(date);
    expect(guidance.dayName).toBe('Monday');
    expect(guidance.hour).toBe(8);
    expect(guidance.direction).toBe('Plan for the Future');
    expect(guidance.activity).toBe("Sketch out tomorrow's survival route.");
  });

  test('should suggest "Live in the Present" in weekday afternoon (Wednesday 14 PM)', () => {
    const date = mockDate(2023, 0, 4, 14); // Wednesday, Jan 4, 2023, 2 PM
    const guidance = getTemporalGuidance(date);
    expect(guidance.dayName).toBe('Wednesday');
    expect(guidance.hour).toBe(14);
    expect(guidance.direction).toBe('Live in the Present');
    expect(guidance.activity).toBe("Tend to your immediate surroundings.");
  });

  test('should suggest "Reflect on the Past" in weekday evening (Friday 19 PM)', () => {
    const date = mockDate(2023, 0, 6, 19); // Friday, Jan 6, 2023, 7 PM
    const guidance = getTemporalGuidance(date);
    expect(guidance.dayName).toBe('Friday');
    expect(guidance.hour).toBe(19);
    expect(guidance.direction).toBe('Reflect on the Past');
    expect(guidance.activity).toBe("Journal about today's discoveries.");
  });

  test('should suggest "Embrace the Void" in weekday late night (Tuesday 23 PM)', () => {
    const date = mockDate(2023, 0, 3, 23); // Tuesday, Jan 3, 2023, 11 PM
    const guidance = getTemporalGuidance(date);
    expect(guidance.dayName).toBe('Tuesday');
    expect(guidance.hour).toBe(23);
    expect(guidance.direction).toBe('Embrace the Void');
    expect(guidance.activity).toBe("Contemplate the vastness of the cosmos.");
  });

  // Weekend (Saturday-Sunday) scenarios
  test('should suggest "Explore New Horizons" in weekend morning (Saturday 10 AM)', () => {
    const date = mockDate(2023, 0, 7, 10); // Saturday, Jan 7, 2023, 10 AM
    const guidance = getTemporalGuidance(date);
    expect(guidance.dayName).toBe('Saturday');
    expect(guidance.hour).toBe(10);
    expect(guidance.direction).toBe('Explore New Horizons');
    expect(guidance.activity).toBe("Scavenge for forgotten knowledge or resources.");
  });

  test('should suggest "Rejuvenate Your Spirit" in weekend afternoon (Sunday 16 PM)', () => {
    const date = mockDate(2023, 0, 8, 16); // Sunday, Jan 8, 2023, 4 PM
    const guidance = getTemporalGuidance(date);
    expect(guidance.dayName).toBe('Sunday');
    expect(guidance.hour).toBe(16);
    expect(guidance.direction).toBe('Rejuvenate Your Spirit');
    expect(guidance.activity).toBe("Engage in a calming, non-essential task.");
  });

  test('should suggest "Dream of What Was" in weekend late night (Saturday 2 AM)', () => {
    const date = mockDate(2023, 0, 7, 2); // Saturday, Jan 7, 2023, 2 AM
    const guidance = getTemporalGuidance(date);
    expect(guidance.dayName).toBe('Saturday');
    expect(guidance.hour).toBe(2);
    expect(guidance.direction).toBe('Dream of What Was');
    expect(guidance.activity).toBe("Recall a cherished memory from before.");
  });

  // Edge cases for hours
  test('should handle weekday morning edge case (Monday 6 AM)', () => {
    const date = mockDate(2023, 0, 2, 6); // Monday, Jan 2, 2023, 6 AM
    const guidance = getTemporalGuidance(date);
    expect(guidance.direction).toBe('Plan for the Future');
  });

  test('should handle weekday afternoon edge case (Monday 11 AM)', () => {
    const date = mockDate(2023, 0, 2, 11); // Monday, Jan 2, 2023, 11 AM
    const guidance = getTemporalGuidance(date);
    expect(guidance.direction).toBe('Live in the Present');
  });

  test('should handle weekday evening edge case (Monday 17 PM)', () => {
    const date = mockDate(2023, 0, 2, 17); // Monday, Jan 2, 2023, 5 PM
    const guidance = getTemporalGuidance(date);
    expect(guidance.direction).toBe('Reflect on the Past');
  });

  test('should handle weekday late night edge case (Monday 22 PM)', () => {
    const date = mockDate(2023, 0, 2, 22); // Monday, Jan 2, 2023, 10 PM
    const guidance = getTemporalGuidance(date);
    expect(guidance.direction).toBe('Embrace the Void');
  });

  test('should handle weekend morning edge case (Saturday 8 AM)', () => {
    const date = mockDate(2023, 0, 7, 8); // Saturday, Jan 7, 2023, 8 AM
    const guidance = getTemporalGuidance(date);
    expect(guidance.direction).toBe('Explore New Horizons');
  });

  test('should handle weekend afternoon edge case (Saturday 13 PM)', () => {
    const date = mockDate(2023, 0, 7, 13); // Saturday, Jan 7, 2023, 1 PM
    const guidance = getTemporalGuidance(date);
    expect(guidance.direction).toBe('Rejuvenate Your Spirit');
  });

  test('should handle weekend late night edge case (Saturday 19 PM)', () => {
    const date = mockDate(2023, 0, 7, 19); // Saturday, Jan 7, 2023, 7 PM
    const guidance = getTemporalGuidance(date);
    expect(guidance.direction).toBe('Dream of What Was');
  });
});
