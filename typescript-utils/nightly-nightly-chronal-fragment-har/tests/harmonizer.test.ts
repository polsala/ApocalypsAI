import { ChronalFragmentHarmonizer } from '../src/harmonizer';
import { DataFragment, HarmonizationReport } from '../src/types';

describe('ChronalFragmentHarmonizer', () => {
  const mockFragments: DataFragment[] = [
    {
      id: 'frag-001',
      content: 'Old world news snippet about AI ethics.',
      timestamp: '2042-03-15T10:30:00Z',
      temporalDistortion: 15,
      origin: 'Pre-Collapse Archive',
    },
    {
      id: 'frag-002',
      content: "Scavenged log entry: 'Power fluctuations detected near Sector 7.'",
      timestamp: '2077-11-20T08:00:00Z',
      temporalDistortion: 80,
      origin: 'Wasteland Scavenge',
    },
    {
      id: 'frag-003',
      content: 'A faint echo of a forgotten lullaby.',
      timestamp: '2030-01-01T00:00:00Z',
      temporalDistortion: 5,
      origin: 'Void Echo',
    },
    {
      id: 'frag-004',
      content: 'Partial schematic for a temporal capacitor.',
      timestamp: '2050-07-22T14:15:00Z',
      temporalDistortion: 45,
      origin: 'Pre-Collapse Archive',
    },
    {
      id: 'frag-005',
      content: 'A very stable fragment from the past.',
      timestamp: '2020-01-01T00:00:00Z',
      temporalDistortion: 10,
      origin: 'Ancient Cache',
    },
    {
      id: 'frag-006',
      content: 'A moderately distorted future prediction.',
      timestamp: '2090-01-01T00:00:00Z',
      temporalDistortion: 55,
      origin: 'Oracle Vision',
    },
  ];

  it('should correctly validate and sort fragments upon instantiation', () => {
    const harmonizer = new ChronalFragmentHarmonizer(mockFragments);
    const sortedFragments = (harmonizer as any).fragments; // Access private property for testing

    // Expected order: frag-003 (5), frag-005 (10), frag-001 (15), frag-004 (45), frag-006 (55), frag-002 (80)
    expect(sortedFragments[0].id).toBe('frag-003');
    expect(sortedFragments[1].id).toBe('frag-005');
    expect(sortedFragments[2].id).toBe('frag-001');
    expect(sortedFragments[3].id).toBe('frag-004');
    expect(sortedFragments[4].id).toBe('frag-006');
    expect(sortedFragments[5].id).toBe('frag-002');
  });

  it('should throw an error for invalid fragment structure', () => {
    const invalidFragments = [
      { id: 'bad-frag', content: 'test', timestamp: '2023-01-01T00:00:00Z', temporalDistortion: 10, origin: 'test' },
      { id: '', content: 'test', timestamp: '2023-01-01T00:00:00Z', temporalDistortion: 10, origin: 'test' }, // Empty ID
    ];
    expect(() => new ChronalFragmentHarmonizer(invalidFragments as any)).toThrow("Invalid fragment: 'id' must be a non-empty string.");

    const invalidTimestamp = [
      { id: 'bad-frag', content: 'test', timestamp: 'not-a-date', temporalDistortion: 10, origin: 'test' },
    ];
    expect(() => new ChronalFragmentHarmonizer(invalidTimestamp as any)).toThrow("Invalid fragment: 'timestamp' must be an ISO 8601 string");

    const invalidDistortion = [
      { id: 'bad-frag', content: 'test', timestamp: '2023-01-01T00:00:00Z', temporalDistortion: 101, origin: 'test' },
    ];
    expect(() => new ChronalFragmentHarmonizer(invalidDistortion as any)).toThrow("Invalid fragment: 'temporalDistortion' must be a number between 0 and 100.");
  });

  it('should correctly categorize fragments', () => {
    const harmonizer = new ChronalFragmentHarmonizer([]); // Empty for categorization test
    expect(harmonizer.categorizeFragment(mockFragments[0])).toBe('Stable'); // 15
    expect(harmonizer.categorizeFragment(mockFragments[1])).toBe('Highly Distorted'); // 80
    expect(harmonizer.categorizeFragment(mockFragments[3])).toBe('Unstable'); // 45
  });

  it('should generate a correct harmonization report', () => {
    const harmonizer = new ChronalFragmentHarmonizer(mockFragments);
    const report = harmonizer.generateReport();

    expect(report.totalFragments).toBe(6);
    expect(report.stableFragments.length).toBe(3); // frag-003, frag-005, frag-001
    expect(report.unstableFragments.length).toBe(2); // frag-004, frag-006
    expect(report.highlyDistortedFragments.length).toBe(1); // frag-002

    expect(report.stableFragments[0].id).toBe('frag-003');
    expect(report.stableFragments[1].id).toBe('frag-005');
    expect(report.stableFragments[2].id).toBe('frag-001');

    expect(report.unstableFragments[0].id).toBe('frag-004');
    expect(report.unstableFragments[1].id).toBe('frag-006');

    expect(report.highlyDistortedFragments[0].id).toBe('frag-002');

    expect(report.recommendations.length).toBeGreaterThan(0);
  });

  it('should format the report correctly', () => {
    const harmonizer = new ChronalFragmentHarmonizer(mockFragments);
    const report = harmonizer.generateReport();
    const formattedReport = harmonizer.formatReport(report);

    expect(formattedReport).toContain('Chronal Fragment Harmonization Report');
    expect(formattedReport).toContain('Total Fragments Processed: 6');
    expect(formattedReport).toContain('Stable Fragments (Distortion < 20): 3');
    expect(formattedReport).toContain('Unstable Fragments (Distortion 20-60): 2');
    expect(formattedReport).toContain('Highly Distorted Fragments (Distortion > 60): 1');
    expect(formattedReport).toContain('--- Stable Fragments ---');
    expect(formattedReport).toContain('[frag-003] (Void Echo) 2030-01-01T00:00:00Z - Distortion: 5');
    expect(formattedReport).toContain('--- Harmonization Recommendations ---');
    expect(formattedReport).toContain('- Prioritize integration of \'Stable Fragments\' first');
  });

  it('should handle empty fragment list gracefully', () => {
    const harmonizer = new ChronalFragmentHarmonizer([]);
    const report = harmonizer.generateReport();
    expect(report.totalFragments).toBe(0);
    expect(report.stableFragments.length).toBe(0);
    expect(report.unstableFragments.length).toBe(0);
    expect(report.highlyDistortedFragments.length).toBe(0);
    const formattedReport = harmonizer.formatReport(report);
    expect(formattedReport).toContain('Total Fragments Processed: 0');
  });
});

// # Mock rationale:
// The tests for ChronalFragmentHarmonizer are entirely deterministic and offline.
// They operate on in-memory mock `DataFragment` arrays.
// The `fs` module for file reading in `cli.ts` is not directly tested here,
// as the core logic is isolated in `harmonizer.ts`. For a full E2E test of the CLI,
// a separate integration test would typically mock `fs.readFileSync` and `process.argv`,
// but for unit testing the core logic, this approach is sufficient and adheres to the
// "deterministic and offline" rule.
