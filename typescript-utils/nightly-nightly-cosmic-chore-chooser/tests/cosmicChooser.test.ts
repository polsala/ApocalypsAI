import { chooseCosmicChore } from '../src/cosmicChooser';
import { CosmicChoreConfig } from '../src/types';

describe('chooseCosmicChore', () => {
  it('should return a default contemplation when no tasks are provided', () => {
    const config: CosmicChoreConfig = { tasks: [] };
    const suggestion = chooseCosmicChore(config);

    expect(suggestion.chosenTask).toBe("Contemplate the infinite void.");
    expect(suggestion.rationale).toContain("cosmos offers no specific guidance");
    expect(suggestion.cosmicAlignmentScore).toBe(0);
  });

  it('should return a suggestion for a single task', () => {
    const tasks = ["Clean the temporal displacement unit"];
    const config: CosmicChoreConfig = { tasks, seed: 123 }; // # Mock rationale: Using a fixed seed for deterministic testing.
    const suggestion = chooseCosmicChore(config);

    expect(suggestion.chosenTask).toBe(tasks[0]);
    expect(typeof suggestion.rationale).toBe('string');
    expect(suggestion.cosmicAlignmentScore).toBeGreaterThanOrEqual(0);
    expect(suggestion.cosmicAlignmentScore).toBeLessThanOrEqual(1);
  });

  it('should return a deterministic suggestion with a fixed seed', () => {
    const tasks = ["Task A", "Task B", "Task C", "Task D"];
    const seed = 42; // # Mock rationale: Using a fixed seed for deterministic testing.

    const config1: CosmicChoreConfig = { tasks, seed };
    const suggestion1 = chooseCosmicChore(config1);

    const config2: CosmicChoreConfig = { tasks, seed };
    const suggestion2 = chooseCosmicChore(config2);

    expect(suggestion1.chosenTask).toBe(suggestion2.chosenTask);
    expect(suggestion1.rationale).toBe(suggestion2.rationale);
    expect(suggestion1.cosmicAlignmentScore).toBe(suggestion2.cosmicAlignmentScore);

    // Verify a specific outcome for a known seed (based on the LCG implementation)
    // Seed 42 -> first rng.next() result for task selection
    // (42 * 16807) % 2147483647 = 705894
    // (705894 - 1) / 2147483646 = ~0.0003287
    // Math.floor(0.0003287 * 4) = 0, so tasks[0] = "Task A"
    expect(suggestion1.chosenTask).toBe("Task A");

    // Seed 42 -> second rng.next() result for rationale selection
    // (705894 * 16807) % 2147483647 = 1125581765
    // (1125581765 - 1) / 2147483646 = ~0.5241
    // Math.floor(0.5241 * 13) = 6, so rationales[6] = "Observe the cosmic dance; this task is its next step for you."
    expect(suggestion1.rationale).toBe(`Observe the cosmic dance; this task is its next step for you.`);
  });

  it('should return different suggestions for different seeds', () => {
    const tasks = ["Task X", "Task Y", "Task Z"];
    const config1: CosmicChoreConfig = { tasks, seed: 1 }; // # Mock rationale: Using different fixed seeds to ensure non-determinism across seeds.
    const suggestion1 = chooseCosmicChore(config1);

    const config2: CosmicChoreConfig = { tasks, seed: 2 }; // # Mock rationale: Using different fixed seeds to ensure non-determinism across seeds.
    const suggestion2 = chooseCosmicChore(config2);

    // It's highly probable they will be different, but not guaranteed for small task lists.
    // We'll check if at least one aspect is different.
    const areDifferent = suggestion1.chosenTask !== suggestion2.chosenTask ||
                         suggestion1.rationale !== suggestion2.rationale ||
                         suggestion1.cosmicAlignmentScore !== suggestion2.cosmicAlignmentScore;
    expect(areDifferent).toBe(true);
  });

  it('should handle a large number of tasks', () => {
    const largeTasks = Array.from({ length: 1000 }, (_, i) => `Task ${i + 1}`);
    const config: CosmicChoreConfig = { tasks: largeTasks, seed: 999 }; // # Mock rationale: Using a fixed seed for deterministic testing with a large input.
    const suggestion = chooseCosmicChore(config);

    expect(largeTasks).toContain(suggestion.chosenTask);
    expect(typeof suggestion.rationale).toBe('string');
    expect(suggestion.cosmicAlignmentScore).toBeGreaterThanOrEqual(0);
    expect(suggestion.cosmicAlignmentScore).toBeLessThanOrEqual(1);
  });
});
