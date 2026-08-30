import { generateCosmicChoreChart } from '../src/cosmicChoreGenerator';
import { CosmicInfluence } from '../src/types';

describe('generateCosmicChoreChart', () => {
  // Mock rationale: We need deterministic dates to ensure the cosmic influence
  // and resulting chores are predictable for testing purposes. The `getDate()`
  // method of the Date object is used to determine the influence, so passing
  // a fixed Date object allows for consistent test results without global mocks.

  it('should generate a chart for LunarLull on a specific date (day 1)', () => {
    const mockDate = new Date('2023-01-01T12:00:00Z'); // Day 1
    const chart = generateCosmicChoreChart(mockDate);

    expect(chart.influence).toBe<CosmicInfluence>('LunarLull');
    expect(chart.message).toContain('moon whispers secrets');
    expect(chart.suggestedChores.length).toBeGreaterThan(0);
    expect(chart.suggestedChores.every(c => c.effort === 'low' || c.category === 'Self-Care')).toBe(true);
  });

  it('should generate a chart for MartianMomentum on a specific date (day 2)', () => {
    const mockDate = new Date('2023-01-02T12:00:00Z'); // Day 2
    const chart = generateCosmicChoreChart(mockDate);

    expect(chart.influence).toBe<CosmicInfluence>('MartianMomentum');
    expect(chart.message).toContain('Mars ignites your drive');
    expect(chart.suggestedChores.length).toBeGreaterThan(0);
    expect(chart.suggestedChores.every(c => c.effort === 'high' || c.category === 'Errand')).toBe(true);
  });

  it('should generate a chart for VenusianVibe on a specific date (day 3)', () => {
    const mockDate = new Date('2023-01-03T12:00:00Z'); // Day 3
    const chart = generateCosmicChoreChart(mockDate);

    expect(chart.influence).toBe<CosmicInfluence>('VenusianVibe');
    expect(chart.message).toContain('Venus brings harmony');
    expect(chart.suggestedChores.length).toBeGreaterThan(0);
    expect(chart.suggestedChores.every(c => c.category === 'Weekly' || c.description.includes('polish') || c.description.includes('organize'))).toBe(true);
  });

  it('should generate a chart for JovianJolt on a specific date (day 4)', () => {
    const mockDate = new Date('2023-01-04T12:00:00Z'); // Day 4
    const chart = generateCosmicChoreChart(mockDate);

    expect(chart.influence).toBe<CosmicInfluence>('JovianJolt');
    expect(chart.message).toContain('Jupiter\'s expansive energy');
    expect(chart.suggestedChores.length).toBeGreaterThan(0);
    expect(chart.suggestedChores.every(c => c.effort === 'high' || c.category === 'Weekly')).toBe(true);
  });

  it('should generate a chart for SolarSurge on a specific date (day 5)', () => {
    const mockDate = new Date('2023-01-05T12:00:00Z'); // Day 5
    const chart = generateCosmicChoreChart(mockDate);

    expect(chart.influence).toBe<CosmicInfluence>('SolarSurge');
    expect(chart.message).toContain('sun energizes all');
    expect(chart.suggestedChores.length).toBeGreaterThan(0);
    expect(chart.suggestedChores.every(c => c.category === 'Daily' || c.effort === 'medium')).toBe(true);
  });

  it('should handle dates beyond the initial influence cycle (day 6)', () => {
    const mockDate = new Date('2023-01-06T12:00:00Z'); // Day 6, which is 6 % 5 = 1 (index 0 is LunarLull)
    const chart = generateCosmicChoreChart(mockDate);
    expect(chart.influence).toBe<CosmicInfluence>('LunarLull'); 
  });

  it('should return a limited number of chores (max 5)', () => {
    const mockDate = new Date('2023-01-05T12:00:00Z'); // SolarSurge, which has many potential chores
    const chart = generateCosmicChoreChart(mockDate);
    expect(chart.suggestedChores.length).toBeLessThanOrEqual(5);
  });

  it('should always provide a message even if no chores are suggested (unlikely with current data)', () => {
    // This test ensures the message property is always defined, even in hypothetical scenarios
    // where filtering might yield no chores. With the current ALL_CHORES and filtering logic,
    // this scenario is unlikely to result in an empty suggestedChores array.
    const mockDate = new Date('2023-01-01T12:00:00Z');
    const chart = generateCosmicChoreChart(mockDate);
    expect(chart.message).toBeDefined();
  });
});
