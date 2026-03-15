import { calculateAlignment } from '../src/cosmicAligner';
import { CosmicAlignment, CosmicEntity } from '../src/types';

describe('calculateAlignment', () => {
  const MOCK_NOW = new Date('2023-10-26T12:00:00Z'); // # Mock rationale: Ensures deterministic time for age calculations.

  it('should assign Galactic Harmony for a new, small, high-priority task', () => {
    const entity: CosmicEntity = {
      id: 't1',
      name: 'Urgent new feature',
      type: 'task',
      priority: 1, // High priority
      lastModified: new Date(MOCK_NOW.getTime() - 1000 * 60 * 5), // 5 minutes ago
      keywords: ['urgent', 'feature']
    };
    const result = calculateAlignment(entity, MOCK_NOW);
    expect(result.alignment).toBe(CosmicAlignment.GalacticHarmony);
    expect(result.score).toBeGreaterThanOrEqual(80);
    expect(result.recommendation).toContain('ideal moment to engage');
  });

  it('should assign Stellar Convergence for a recent, medium file', () => {
    const entity: CosmicEntity = {
      id: 'f1',
      name: 'project_report.md',
      type: 'file',
      lastModified: new Date(MOCK_NOW.getTime() - 3 * 24 * 60 * 60 * 1000), // 3 days ago
      sizeBytes: 5 * 1024 * 1024, // 5MB
    };
    const result = calculateAlignment(entity, MOCK_NOW);
    expect(result.alignment).toBe(CosmicAlignment.StellarConvergence);
    expect(result.score).toBeGreaterThanOrEqual(60);
    expect(result.recommendation).toContain('Focus your energy here');
  });

  it('should assign Temporal Flux for an older, larger file', () => {
    const entity: CosmicEntity = {
      id: 'f2',
      name: 'archive_data.zip',
      type: 'file',
      lastModified: new Date(MOCK_NOW.getTime() - 15 * 24 * 60 * 60 * 1000), // 15 days ago
      sizeBytes: 50 * 1024 * 1024, // 50MB
    };
    const result = calculateAlignment(entity, MOCK_NOW);
    expect(result.alignment).toBe(CosmicAlignment.TemporalFlux);
    expect(result.score).toBeGreaterThanOrEqual(40);
    expect(result.recommendation).toContain('window of opportunity exists');
  });

  it('should assign Nebula Drift for a very old, small file', () => {
    const entity: CosmicEntity = {
      id: 'f3',
      name: 'old_notes.txt',
      type: 'file',
      lastModified: new Date(MOCK_NOW.getTime() - 60 * 24 * 60 * 60 * 1000), // 60 days ago
      sizeBytes: 100 * 1024, // 100KB
    };
    const result = calculateAlignment(entity, MOCK_NOW);
    expect(result.alignment).toBe(CosmicAlignment.NebulaDrift);
    expect(result.score).toBeGreaterThanOrEqual(20);
    expect(result.recommendation).toContain('Consider its path');
  });

  it('should assign Void Resonance for an ancient, very large file', () => {
    const entity: CosmicEntity = {
      id: 'f4',
      name: 'legacy_backup.tar.gz',
      type: 'file',
      lastModified: new Date(MOCK_NOW.getTime() - 365 * 24 * 60 * 60 * 1000), // 1 year ago
      sizeBytes: 500 * 1024 * 1024, // 500MB
    };
    const result = calculateAlignment(entity, MOCK_NOW);
    expect(result.alignment).toBe(CosmicAlignment.VoidResonance);
    expect(result.score).toBeLessThan(20);
    expect(result.recommendation).toContain('demands attention or release');
  });

  it('should handle tasks without lastModified as relatively current', () => {
    const entity: CosmicEntity = {
      id: 't2',
      name: 'Brainstorm new ideas',
      type: 'task',
      priority: 3
    };
    const result = calculateAlignment(entity, MOCK_NOW);
    expect(result.alignment).not.toBe(CosmicAlignment.VoidResonance);
    expect(result.score).toBeGreaterThanOrEqual(40); // Should be at least Temporal Flux or higher
    expect(result.recommendation).toContain('Its origin is now');
  });

  it('should prioritize entities with urgent keywords', () => {
    const entity: CosmicEntity = {
      id: 't3',
      name: 'Critical bug fix',
      type: 'task',
      priority: 2,
      keywords: ['critical', 'bug'],
      lastModified: new Date(MOCK_NOW.getTime() - 2 * 24 * 60 * 60 * 1000) // 2 days ago
    };
    const result = calculateAlignment(entity, MOCK_NOW);
    expect(result.alignment).toBe(CosmicAlignment.GalacticHarmony); // Urgent keyword pushes it higher
    expect(result.score).toBeGreaterThanOrEqual(80);
  });

  it('should handle tab entities correctly', () => {
    const entity: CosmicEntity = {
      id: 'tab1',
      name: 'ApocalypsAI GitHub Issue',
      type: 'tab',
      keywords: ['github', 'issue']
    };
    const result = calculateAlignment(entity, MOCK_NOW);
    expect(result.alignment).not.toBe(CosmicAlignment.VoidResonance);
    expect(result.score).toBeGreaterThanOrEqual(60); // Tabs are generally current and light
    expect(result.recommendation).toContain('light as stardust');
  });
});
