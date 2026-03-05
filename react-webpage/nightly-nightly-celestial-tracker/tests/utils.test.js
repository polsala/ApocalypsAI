import { calculateCelestialPositions, determineAlignmentInfluence } from '../src/utils';

describe('utils', () => {
  // Mock rationale: These functions are pure and deterministic. No external mocks needed.
  // We test their output directly based on known inputs.

  describe('calculateCelestialPositions', () => {
    test('should return a deterministic set of positions for a given date', () => {
      const date1 = new Date('2023-01-15T12:00:00Z');
      const positions1 = calculateCelestialPositions(date1);

      expect(positions1).toHaveLength(5);
      expect(positions1[0].name).toBe('Solara');
      expect(positions1[0].angle).toBeCloseTo(240.5);
      expect(positions1[1].name).toBe('Lunaris');
      expect(positions1[1].angle).toBeCloseTo(104.4);

      const date2 = new Date('2023-01-15T12:00:00Z'); // Same date
      const positions2 = calculateCelestialPositions(date2);
      expect(positions1).toEqual(positions2); // Should be identical for same date

      const date3 = new Date('2023-01-16T12:00:00Z'); // Different date
      const positions3 = calculateCelestialPositions(date3);
      expect(positions1).not.toEqual(positions3); // Should be different for different date
    });

    test('angles should be between 0 and 360', () => {
      const date = new Date('2025-07-20T00:00:00Z');
      const positions = calculateCelestialPositions(date);
      positions.forEach(body => {
        expect(body.angle).toBeGreaterThanOrEqual(0);
        expect(body.angle).toBeLessThan(360);
      });
    });
  });

  describe('determineAlignmentInfluence', () => {
    test('should detect a conjunction when two bodies are very close', () => {
      const positions = [
        { name: 'A', angle: 10, color: 'red' },
        { name: 'B', angle: 15, color: 'blue' },
        { name: 'C', angle: 100, color: 'green' }
      ];
      const influences = determineAlignmentInfluence(positions);
      expect(influences).toContain('A-B Conjunction: A day of heightened emotional resonance and potential resource discovery!');
      expect(influences).toHaveLength(1); // Only one specific alignment
    });

    test('should detect an opposition when two bodies are ~180 degrees apart', () => {
      const positions = [
        { name: 'A', angle: 10, color: 'red' },
        { name: 'B', angle: 190, color: 'blue' },
        { name: 'C', angle: 50, color: 'green' }
      ];
      const influences = determineAlignmentInfluence(positions);
      expect(influences).toContain('A-B Opposition: Expect challenges in communication, but breakthroughs in innovation!');
      expect(influences).toHaveLength(1);
    });

    test('should detect a square when two bodies are ~90 degrees apart', () => {
      const positions = [
        { name: 'A', angle: 10, color: 'red' },
        { name: 'B', angle: 100, color: 'blue' },
        { name: 'C', angle: 200, color: 'green' }
      ];
      const influences = determineAlignmentInfluence(positions);
      expect(influences).toContain('A-B Square: A period of introspection, perhaps revealing hidden truths or forgotten caches.');
      expect(influences).toHaveLength(1);
    });

    test('should detect a grand trine when three bodies are ~120 degrees apart', () => {
      const positions = [
        { name: 'A', angle: 0, color: 'red' },
        { name: 'B', angle: 120, color: 'blue' },
        { name: 'C', angle: 240, color: 'green' },
        { name: 'D', angle: 30, color: 'yellow' }
      ];
      const influences = determineAlignmentInfluence(positions);
      expect(influences).toContain('Grand Trine (A, B, C): Harmonious energies abound, perfect for collaborative efforts!');
      expect(influences).toHaveLength(1);
    });

    test('should return default message if no alignments are found', () => {
      const positions = [
        { name: 'A', angle: 0, color: 'red' },
        { name: 'B', angle: 45, color: 'blue' },
        { name: 'C', angle: 90, color: 'green' }
      ];
      const influences = determineAlignmentInfluence(positions);
      expect(influences).toContain('The cosmos hums a neutral tune. Proceed with cautious optimism.');
      expect(influences).toHaveLength(1);
    });

    test('should return multiple influences if multiple alignments occur', () => {
      const positions = [
        { name: 'A', angle: 5, color: 'red' },
        { name: 'B', angle: 10, color: 'blue' }, // A-B Conjunction
        { name: 'C', angle: 190, color: 'green' } // A-C Opposition
      ];
      const influences = determineAlignmentInfluence(positions);
      expect(influences).toContain('A-B Conjunction: A day of heightened emotional resonance and potential resource discovery!');
      expect(influences).toContain('A-C Opposition: Expect challenges in communication, but breakthroughs in innovation!');
      expect(influences).toHaveLength(2);
    });
  });
});
