import { checkCosmicAlignment } from '../src/index';
import { CosmicFactor, AlignmentResult, AlignmentStatus } from '../src/types';

// Mock rationale: We need to control Math.random to ensure deterministic test results.
// This allows us to predict the outcome of the random factor generation and overall alignment status.
describe('checkCosmicAlignment', () => {
  let mockMathRandom: jest.SpyInstance;

  beforeEach(() => {
    mockMathRandom = jest.spyOn(Math, 'random');
  });

  afterEach(() => {
    mockMathRandom.mockRestore();
  });

  it('should return a Favorable alignment when random values lean positive', () => {
    // Mock Math.random to always return values that lead to 'Favorable' outcomes
    // for both factor selection and status determination.
    mockMathRandom
      .mockReturnValueOnce(0.1) // Selects Lunar Phase
      .mockReturnValueOnce(0.1) // Lunar Phase: Favorable
      .mockReturnValueOnce(0.2) // Selects Stellar Drift
      .mockReturnValueOnce(0.1) // Stellar Drift: Favorable
      .mockReturnValueOnce(0.3) // Selects Nebula Bloom
      .mockReturnValueOnce(0.1) // Nebula Bloom: Favorable
      .mockReturnValueOnce(0.4) // Selects Quantum Entanglement
      .mockReturnValueOnce(0.1); // Quantum Entanglement: Favorable

    const result: AlignmentResult = checkCosmicAlignment();

    expect(result.overallStatus).toBe('Favorable');
    expect(result.factors.length).toBe(4);
    expect(result.factors.filter(f => f.status === 'Favorable').length).toBe(4);
    expect(result.message).toContain('cosmos smiles upon your endeavors');
  });

  it('should return an Unfavorable alignment when random values lean negative', () => {
    // Mock Math.random to always return values that lead to 'Unfavorable' outcomes
    mockMathRandom
      .mockReturnValueOnce(0.1) // Selects Lunar Phase
      .mockReturnValueOnce(0.9) // Lunar Phase: Unfavorable
      .mockReturnValueOnce(0.2) // Selects Stellar Drift
      .mockReturnValueOnce(0.9) // Stellar Drift: Unfavorable
      .mockReturnValueOnce(0.3) // Selects Nebula Bloom
      .mockReturnValueOnce(0.9) // Nebula Bloom: Unfavorable
      .mockReturnValueOnce(0.4) // Selects Quantum Entanglement
      .mockReturnValueOnce(0.9); // Quantum Entanglement: Unfavorable

    const result: AlignmentResult = checkCosmicAlignment();

    expect(result.overallStatus).toBe('Unfavorable');
    expect(result.factors.length).toBe(4);
    expect(result.factors.filter(f => f.status === 'Unfavorable').length).toBe(4);
    expect(result.message).toContain('cosmic currents are turbulent');
  });

  it('should return a Neutral alignment when favorable and unfavorable counts are equal', () => {
    // Mock Math.random to alternate between favorable and unfavorable, resulting in equal counts.
    mockMathRandom
      .mockReturnValueOnce(0.1) // Selects Lunar Phase
      .mockReturnValueOnce(0.1) // Lunar Phase: Favorable
      .mockReturnValueOnce(0.2) // Selects Stellar Drift
      .mockReturnValueOnce(0.9) // Stellar Drift: Unfavorable
      .mockReturnValueOnce(0.3) // Selects Nebula Bloom
      .mockReturnValueOnce(0.1) // Nebula Bloom: Favorable
      .mockReturnValueOnce(0.4); // Selects Quantum Entanglement
      // .mockReturnValueOnce(0.9); // Quantum Entanglement: Unfavorable (This makes 2 Favorable, 2 Unfavorable)

    const result: AlignmentResult = checkCosmicAlignment();

    expect(result.overallStatus).toBe('Neutral');
    expect(result.factors.length).toBe(4);
    expect(result.factors.filter(f => f.status === 'Favorable').length).toBe(2);
    expect(result.factors.filter(f => f.status === 'Unfavorable').length).toBe(2);
    expect(result.message).toContain('cosmos is undecided');
  });

  it('should have factors with correct structure and types', () => {
    mockMathRandom
      .mockReturnValueOnce(0.1) // Selects Lunar Phase
      .mockReturnValueOnce(0.1) // Lunar Phase: Favorable
      .mockReturnValueOnce(0.2) // Selects Stellar Drift
      .mockReturnValueOnce(0.9) // Stellar Drift: Unfavorable
      .mockReturnValueOnce(0.3) // Selects Nebula Bloom
      .mockReturnValueOnce(0.1) // Nebula Bloom: Favorable
      .mockReturnValueOnce(0.4); // Selects Quantum Entanglement
      // .mockReturnValueOnce(0.9); // Quantum Entanglement: Unfavorable

    const result: AlignmentResult = checkCosmicAlignment();
    const firstFactor = result.factors[0];

    expect(firstFactor).toHaveProperty('name');
    expect(typeof firstFactor.name).toBe('string');
    expect(firstFactor).toHaveProperty('status');
    expect(['Favorable', 'Unfavorable', 'Neutral'] as AlignmentStatus[]).toContain(firstFactor.status);
    expect(firstFactor).toHaveProperty('description');
    expect(typeof firstFactor.description).toBe('string');
  });
});
