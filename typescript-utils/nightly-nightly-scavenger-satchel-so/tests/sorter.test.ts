import { sortSatchel } from '../src/sorter';
import { Item, SatchelConfig } from '../src/types';

describe('sortSatchel', () => {
  const items: Item[] = [
    { name: 'Water Bottle', weight: 1.1, volume: 1.0, survival_score: 100 },
    { name: 'Canned Beans', weight: 0.4, volume: 0.3, survival_score: 50 },
    { name: 'First Aid Kit', weight: 0.8, volume: 0.5, survival_score: 120 },
    { name: 'Machete', weight: 1.5, volume: 0.2, survival_score: 80 },
    { name: 'Radio', weight: 0.6, volume: 0.4, survival_score: 70 },
    { name: 'Tent', weight: 3.0, volume: 5.0, survival_score: 200 },
    { name: 'Rope (10m)', weight: 0.5, volume: 0.1, survival_score: 60 },
    { name: 'Matches', weight: 0.1, volume: 0.05, survival_score: 30 },
  ];

  it('should select items within weight and volume limits, prioritizing survival score and density', () => {
    const config: SatchelConfig = { maxWeight: 3.0, maxVolume: 2.0 };
    const selected = sortSatchel(items, config);

    // Expected items based on greedy sort (survival_score (desc), then density (desc), then total resource (asc))
    // 1. Tent (S:200, W:3.0, V:5.0) - too large for 3.0kg, 2.0L
    // 2. First Aid Kit (S:120, W:0.8, V:0.5) - Fits. Current: W:0.8, V:0.5
    // 3. Water Bottle (S:100, W:1.1, V:1.0) - Fits. Current: W:1.9, V:1.5
    // 4. Machete (S:80, W:1.5, V:0.2) - Too heavy (1.9 + 1.5 = 3.4 > 3.0)
    // 5. Radio (S:70, W:0.6, V:0.4) - Fits. Current: W:1.9 + 0.6 = 2.5, V:1.5 + 0.4 = 1.9
    // 6. Rope (10m) (S:60, W:0.5, V:0.1) - Fits. Current: W:2.5 + 0.5 = 3.0, V:1.9 + 0.1 = 2.0
    // 7. Canned Beans (S:50, W:0.4, V:0.3) - Too heavy (3.0 + 0.4 > 3.0)
    // 8. Matches (S:30, W:0.1, V:0.05) - Too heavy (3.0 + 0.1 > 3.0)

    const expectedNames = ['First Aid Kit', 'Water Bottle', 'Radio', 'Rope (10m)'];
    expect(selected.map(item => item.name)).toEqual(expectedNames);
    expect(selected.length).toBe(expectedNames.length);

    const totalWeight = selected.reduce((sum, item) => sum + item.weight, 0);
    const totalVolume = selected.reduce((sum, item) => sum + item.volume, 0);
    expect(totalWeight).toBeCloseTo(3.0);
    expect(totalVolume).toBeCloseTo(2.0);
  });

  it('should handle empty item list', () => {
    const config: SatchelConfig = { maxWeight: 10, maxVolume: 10 };
    const selected = sortSatchel([], config);
    expect(selected).toEqual([]);
  });

  it('should handle items that are all too large', () => {
    const config: SatchelConfig = { maxWeight: 0.05, maxVolume: 0.01 }; // Too small for even matches
    const selected = sortSatchel(items, config);
    expect(selected).toEqual([]);
  });

  it('should select items when only one fits', () => {
    const config: SatchelConfig = { maxWeight: 0.15, maxVolume: 0.06 }; // Just enough for matches
    const selected = sortSatchel(items, config);
    expect(selected.map(item => item.name)).toEqual(['Matches']);
  });

  it('should prioritize higher survival score when density is similar', () => {
    const customItems: Item[] = [
      { name: 'Rare Artifact A', weight: 1, volume: 1, survival_score: 200 }, // Density 100
      { name: 'Rare Artifact B', weight: 1, volume: 1, survival_score: 150 }, // Density 75
      { name: 'Common Tool C', weight: 0.5, volume: 0.5, survival_score: 100 }, // Density 100
    ];
    const config: SatchelConfig = { maxWeight: 1.5, maxVolume: 1.5 };
    const selected = sortSatchel(customItems, config);

    // Sorted order based on strategy:
    // 1. Rare Artifact A (S:200, D:100)
    // 2. Common Tool C (S:100, D:100) - same density as A, lower score, but picked next due to lower total resource if A is taken
    // 3. Rare Artifact B (S:150, D:75)

    // A fits (W:1, V:1). Remaining: W:0.5, V:0.5
    // C fits (W:0.5, V:0.5). Remaining: W:0, V:0
    // B does not fit.
    expect(selected.map(item => item.name)).toEqual(['Rare Artifact A', 'Common Tool C']);
  });
});

// # Mock rationale: The `src/index.ts` file performs file I/O and CLI argument parsing. 
// # However, the core logic for sorting items is encapsulated in `src/sorter.ts`, which is a pure function. 
// # For deterministic and offline testing, it is sufficient to test this pure sorting logic directly. 
// # Mocking `fs.readFileSync` and `process.argv` would be necessary if `src/index.ts` itself were being unit tested, 
// # but for this utility, testing the core algorithm is the primary goal and is achieved without mocks.
