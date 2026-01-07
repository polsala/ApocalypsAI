import { weaveCosmicChoice } from '../src/weaver';
import { Choice, CosmicInfluence, WeaverConfig } from '../src/types';

describe('weaveCosmicChoice', () => {
  const sampleChoices: Choice[] = [
    { id: 'A', name: 'Option A', tags: ['tag1'], weight: 10 },
    { id: 'B', name: 'Option B', tags: ['tag2'], weight: 5 },
    { id: 'C', name: 'Option C', tags: ['tag1', 'tag2'], weight: 2 },
    { id: 'D', name: 'Option D', tags: [], weight: 1 }
  ];

  it('should return null if no choices are provided', () => {
    const config: WeaverConfig = { choices: [] };
    expect(weaveCosmicChoice(config)).toBeNull();
  });

  it('should return a choice from the provided list', () => {
    const config: WeaverConfig = { choices: sampleChoices, seed: 'test-seed-1' };
    const chosen = weaveCosmicChoice(config);
    expect(chosen).not.toBeNull();
    expect(sampleChoices.some(c => c.id === chosen!.id)).toBe(true);
  });

  it('should produce deterministic results with the same seed', () => {
    const config1: WeaverConfig = { choices: sampleChoices, seed: 'fixed-seed' };
    const config2: WeaverConfig = { choices: sampleChoices, seed: 'fixed-seed' };

    const chosen1 = weaveCosmicChoice(config1);
    const chosen2 = weaveCosmicChoice(config2);

    expect(chosen1!.id).toBe(chosen2!.id); // Should be the same choice
  });

  it('should apply influences correctly, favoring higher multipliers', () => {
    const choices: Choice[] = [
      { id: 'Relax', name: 'Relax', tags: ['calm'], weight: 1 },
      { id: 'Work', name: 'Work', tags: ['productive'], weight: 1 }
    ];
    const influences: CosmicInfluence[] = [
      { tag: 'productive', multiplier: 10 } // Should heavily favor 'Work'
    ];
    const config: WeaverConfig = { choices, influences, seed: 'influence-test-seed' };

    // With a strong influence, 'Work' should be chosen consistently for a given seed
    // We'll run it a few times to ensure it's not just random luck for this seed
    const results = Array(5).fill(0).map(() => weaveCosmicChoice(config)!.id);
    // # Mock rationale: The seeded random number generator ensures deterministic output.
    // We expect 'Work' to be chosen due to the high multiplier for 'productive' tag.
    // The specific seed 'influence-test-seed' is chosen to reliably hit the 'Work' option
    // given the weights and multiplier.
    expect(results.every(id => id === 'Work')).toBe(true);
  });

  it('should apply influences correctly, disfavoring lower multipliers', () => {
    const choices: Choice[] = [
      { id: 'Relax', name: 'Relax', tags: ['calm'], weight: 10 },
      { id: 'Work', name: 'Work', tags: ['productive'], weight: 10 }
    ];
    const influences: CosmicInfluence[] = [
      { tag: 'calm', multiplier: 0.1 } // Should heavily disfavor 'Relax'
    ];
    const config: WeaverConfig = { choices, influences, seed: 'disfavor-test-seed' };

    const results = Array(5).fill(0).map(() => weaveCosmicChoice(config)!.id);
    // # Mock rationale: The seeded random number generator ensures deterministic output.
    // We expect 'Work' to be chosen due to the low multiplier for 'calm' tag, making 'Relax' less likely.
    // The specific seed 'disfavor-test-seed' is chosen to reliably hit the 'Work' option.
    expect(results.every(id => id === 'Work')).toBe(true);
  });

  it('should handle choices with zero or negative effective scores by falling back to uniform random', () => {
    const choices: Choice[] = [
      { id: 'A', name: 'Option A', tags: ['bad'], weight: 1 },
      { id: 'B', name: 'Option B', tags: ['bad'], weight: 1 }
    ];
    const influences: CosmicInfluence[] = [
      { tag: 'bad', multiplier: 0 } // Makes all choices have 0 score
    ];
    const config: WeaverConfig = { choices, influences, seed: 'zero-score-seed' };

    const chosen = weaveCosmicChoice(config);
    expect(chosen).not.toBeNull();
    expect(['A', 'B']).toContain(chosen!.id);

    // Test with negative weights
    const choicesNegative: Choice[] = [
      { id: 'X', name: 'Option X', weight: -10 },
      { id: 'Y', name: 'Option Y', weight: -5 }
    ];
    const configNegative: WeaverConfig = { choices: choicesNegative, seed: 'negative-score-seed' };
    const chosenNegative = weaveCosmicChoice(configNegative);
    expect(chosenNegative).not.toBeNull();
    expect(['X', 'Y']).toContain(chosenNegative!.id);
  });

  it('should use base weights when no influences are present', () => {
    const choices: Choice[] = [
      { id: 'Low', name: 'Low Weight', weight: 1 },
      { id: 'High', name: 'High Weight', weight: 10 }
    ];
    const config: WeaverConfig = { choices, seed: 'weights-only-seed' };

    // # Mock rationale: The seeded random number generator ensures deterministic output.
    // With 'weights-only-seed', the random number generated should fall into the 'High' weight range.
    expect(weaveCosmicChoice(config)!.id).toBe('High');
  });

  it('should default to weight 1 if no weight is specified', () => {
    const choices: Choice[] = [
      { id: 'NoWeight1', name: 'No Weight 1' },
      { id: 'NoWeight2', name: 'No Weight 2' }
    ];
    const config: WeaverConfig = { choices, seed: 'default-weight-seed' };
    const chosen = weaveCosmicChoice(config);
    expect(chosen).not.toBeNull();
    expect(['NoWeight1', 'NoWeight2']).toContain(chosen!.id);
  });
});
