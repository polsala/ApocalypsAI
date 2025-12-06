import { alignEchoStreams, detectDiscrepancies, harmonizeEchoes } from '../src/index';
import { TemporalEcho, AlignedEchoGroup, Discrepancy } from '../src/types';

describe('Timeline Harmonizer', () => {
  // Mock rationale: All data is in-memory and deterministic. No external calls or side effects.
  const streamA: TemporalEcho[] = [
    { timestamp: 1000, value: 10, source: 'Alpha' },
    { timestamp: 2000, value: 20, source: 'Alpha' },
    { timestamp: 3000, value: 30, source: 'Alpha' },
  ];

  const streamB: TemporalEcho[] = [
    { timestamp: 1000, value: 11, source: 'Beta' },
    { timestamp: 2000, value: 21, source: 'Beta' },
    { timestamp: 4000, value: 40, source: 'Beta' }, // Missing 3000
  ];

  const streamC: TemporalEcho[] = [
    { timestamp: 1000, value: 10, source: 'Gamma' },
    { timestamp: 3000, value: 32, source: 'Gamma' }, // Missing 2000
    { timestamp: 4000, value: 41, source: 'Gamma' },
  ];

  describe('alignEchoStreams', () => {
    test('should align streams with perfect overlap', () => {
      const aligned = alignEchoStreams([streamA, streamB]);
      expect(aligned.length).toBe(4);
      expect(aligned[0].timestamp).toBe(1000);
      expect(aligned[0].echoes.length).toBe(2);
      expect(aligned[0].echoes.map(e => e.source)).toEqual(expect.arrayContaining(['Alpha', 'Beta']));
      expect(aligned[1].timestamp).toBe(2000);
      expect(aligned[1].echoes.length).toBe(2);
      expect(aligned[2].timestamp).toBe(3000);
      expect(aligned[2].echoes.length).toBe(1); // Stream B is missing
      expect(aligned[2].echoes[0].source).toBe('Alpha');
      expect(aligned[3].timestamp).toBe(4000);
      expect(aligned[3].echoes.length).toBe(1); // Stream A is missing
      expect(aligned[3].echoes[0].source).toBe('Beta');
    });

    test('should align multiple streams with various missing points', () => {
      const aligned = alignEchoStreams([streamA, streamB, streamC]);
      expect(aligned.length).toBe(4);

      expect(aligned[0].timestamp).toBe(1000);
      expect(aligned[0].echoes.length).toBe(3);
      expect(aligned[0].echoes.map(e => e.value)).toEqual(expect.arrayContaining([10, 11, 10]));

      expect(aligned[1].timestamp).toBe(2000);
      expect(aligned[1].echoes.length).toBe(2);
      expect(aligned[1].echoes.map(e => e.value)).toEqual(expect.arrayContaining([20, 21]));

      expect(aligned[2].timestamp).toBe(3000);
      expect(aligned[2].echoes.length).toBe(2);
      expect(aligned[2].echoes.map(e => e.value)).toEqual(expect.arrayContaining([30, 32]));

      expect(aligned[3].timestamp).toBe(4000);
      expect(aligned[3].echoes.length).toBe(2);
      expect(aligned[3].echoes.map(e => e.value)).toEqual(expect.arrayContaining([40, 41]));
    });

    test('should handle empty streams', () => {
      const aligned = alignEchoStreams([streamA, []]);
      expect(aligned.length).toBe(3);
      expect(aligned[0].echoes.length).toBe(1);
      expect(aligned[0].echoes[0].source).toBe('Alpha');
    });

    test('should return empty array for all empty streams', () => {
      const aligned = alignEchoStreams([[], []]);
      expect(aligned.length).toBe(0);
    });
  });

  describe('detectDiscrepancies', () => {
    const alignedGroups: AlignedEchoGroup[] = [
      { timestamp: 1000, echoes: [{ timestamp: 1000, value: 10, source: 'A' }, { timestamp: 1000, value: 10.5, source: 'B' }] }, // Low deviation
      { timestamp: 2000, echoes: [{ timestamp: 2000, value: 20, source: 'A' }, { timestamp: 2000, value: 25, source: 'B' }] }, // High deviation
      { timestamp: 3000, echoes: [{ timestamp: 3000, value: 30, source: 'A' }] }, // Single echo, no discrepancy
      { timestamp: 4000, echoes: [{ timestamp: 4000, value: 0, source: 'A' }, { timestamp: 4000, value: 0, source: 'B' }] }, // All zeros, no discrepancy
      { timestamp: 5000, echoes: [{ timestamp: 5000, value: 0, source: 'A' }, { timestamp: 5000, value: 10, source: 'B' }] }, // Zero and non-zero
    ];

    test('should detect discrepancies above threshold', () => {
      const discrepancies = detectDiscrepancies(alignedGroups, 0.15); // 15% threshold
      expect(discrepancies.length).toBe(2);
      expect(discrepancies[0].timestamp).toBe(2000);
      expect(discrepancies[0].deviation).toBeCloseTo(0.111); // (25-22.5)/22.5 = 2.5/22.5 = 0.111...
      expect(discrepancies[1].timestamp).toBe(5000);
      expect(discrepancies[1].deviation).toBe(Infinity);
    });

    test('should not detect discrepancies below threshold', () => {
      const discrepancies = detectDiscrepancies(alignedGroups, 0.2); // 20% threshold
      expect(discrepancies.length).toBe(1); // Still detects 5000, 2000 is now below threshold
      expect(discrepancies[0].timestamp).toBe(5000);
    });

    test('should handle groups with single echoes', () => {
      const discrepancies = detectDiscrepancies([alignedGroups[2]], 0.1);
      expect(discrepancies.length).toBe(0);
    });

    test('should handle all zero values without error or discrepancy', () => {
      const discrepancies = detectDiscrepancies([alignedGroups[3]], 0.1);
      expect(discrepancies.length).toBe(0);
    });

    test('should detect discrepancy when one value is zero and another is not', () => {
      const discrepancies = detectDiscrepancies([alignedGroups[4]], 0.1);
      expect(discrepancies.length).toBe(1);
      expect(discrepancies[0].timestamp).toBe(5000);
      expect(discrepancies[0].deviation).toBe(Infinity);
    });
  });

  describe('harmonizeEchoes', () => {
    const alignedGroups: AlignedEchoGroup[] = [
      { timestamp: 1000, echoes: [{ timestamp: 1000, value: 10, source: 'A' }, { timestamp: 1000, value: 12, source: 'B' }] },
      { timestamp: 2000, echoes: [{ timestamp: 2000, value: 20, source: 'A' }, { timestamp: 2000, value: 22, source: 'B' }, { timestamp: 2000, value: 24, source: 'C' }] },
      { timestamp: 3000, echoes: [{ timestamp: 3000, value: 30, source: 'A' }] },
      { timestamp: 4000, echoes: [] }, // Empty group
    ];

    test('should harmonize using average strategy', () => {
      const harmonized = harmonizeEchoes(alignedGroups, 'average');
      expect(harmonized.length).toBe(3);
      expect(harmonized[0].value).toBe(11); // (10+12)/2
      expect(harmonized[1].value).toBe(22); // (20+22+24)/3
      expect(harmonized[2].value).toBe(30); // Single value
      expect(harmonized[0].source).toBe('Harmonized');
    });

    test('should harmonize using median strategy', () => {
      const harmonized = harmonizeEchoes(alignedGroups, 'median');
      expect(harmonized.length).toBe(3);
      expect(harmonized[0].value).toBe(11); // Median of [10, 12]
      expect(harmonized[1].value).toBe(22); // Median of [20, 22, 24]
      expect(harmonized[2].value).toBe(30);
    });

    test('should harmonize using first strategy', () => {
      const harmonized = harmonizeEchoes(alignedGroups, 'first');
      expect(harmonized.length).toBe(3);
      expect(harmonized[0].value).toBe(10);
      expect(harmonized[1].value).toBe(20);
      expect(harmonized[2].value).toBe(30);
    });

    test('should harmonize using last strategy', () => {
      const harmonized = harmonizeEchoes(alignedGroups, 'last');
      expect(harmonized.length).toBe(3);
      expect(harmonized[0].value).toBe(12);
      expect(harmonized[1].value).toBe(24);
      expect(harmonized[2].value).toBe(30);
    });

    test('should handle empty aligned groups gracefully', () => {
      const harmonized = harmonizeEchoes([alignedGroups[3]], 'average');
      expect(harmonized.length).toBe(0);
    });
  });
});
