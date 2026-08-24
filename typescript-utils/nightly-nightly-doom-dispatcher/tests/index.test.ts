import { assignDoomAndWhimsy, dispatchTasks } from '../src/index';

// Mock rationale: Math.random() is mocked to ensure deterministic results for testing
// the random assignment logic. This allows us to predict the output of assignDoomAndWhimsy
// and dispatchTasks, making tests reliable and repeatable.
describe('Nightly Doom Dispatcher', () => {
  let consoleSpy: jest.SpyInstance;

  beforeEach(() => {
    consoleSpy = jest.spyOn(console, 'log').mockImplementation(() => {});
  });

  afterEach(() => {
    consoleSpy.mockRestore();
  });

  describe('assignDoomAndWhimsy', () => {
    it('should assign deterministic DoomLevel and WhimsyBonus when Math.random is mocked', () => {
      // Mock Math.random to return specific values for deterministic testing
      const mockRandom = jest.spyOn(Math, 'random');

      // Test case 1: MinorGlitch (index 0) + FaintSparkle (index 0)
      mockRandom.mockReturnValueOnce(0.01); // For DoomLevel (MinorGlitch)
      mockRandom.mockReturnValueOnce(0.01); // For WhimsyBonus (FaintSparkle)
      const task1 = assignDoomAndWhimsy("Test Task 1");
      expect(task1.task).toBe("Test Task 1");
      expect(task1.doomLevel).toBe(1); // MinorGlitch
      expect(task1.whimsyBonus).toBe(1); // FaintSparkle
      expect(task1.score).toBe(11); // 1*10 + 1

      // Test case 2: ExistentialThreat (index 2) + CosmicJoke (index 2)
      mockRandom.mockReturnValueOnce(0.99); // For DoomLevel (ExistentialThreat)
      mockRandom.mockReturnValueOnce(0.99); // For WhimsyBonus (CosmicJoke)
      const task2 = assignDoomAndWhimsy("Test Task 2");
      expect(task2.task).toBe("Test Task 2");
      expect(task2.doomLevel).toBe(3); // ExistentialThreat
      expect(task2.whimsyBonus).toBe(3); // CosmicJoke
      expect(task2.score).toBe(33); // 3*10 + 3

      // Test case 3: ImpendingCatastrophe (index 1) + GentleGiggle (index 1)
      mockRandom.mockReturnValueOnce(0.4); // For DoomLevel (ImpendingCatastrophe)
      mockRandom.mockReturnValueOnce(0.4); // For WhimsyBonus (GentleGiggle)
      const task3 = assignDoomAndWhimsy("Test Task 3");
      expect(task3.task).toBe("Test Task 3");
      expect(task3.doomLevel).toBe(2); // ImpendingCatastrophe
      expect(task3.whimsyBonus).toBe(2); // GentleGiggle
      expect(task3.score).toBe(22); // 2*10 + 2

      mockRandom.mockRestore();
    });
  });

  describe('dispatchTasks', () => {
    it('should handle an empty list of tasks', () => {
      dispatchTasks([]);
      expect(consoleSpy).toHaveBeenCalledWith("No tasks provided. The apocalypse awaits your input!");
    });

    it('should sort tasks correctly based on doom level and whimsy bonus', () => {
      // Mock Math.random to ensure a specific order for sorting tests
      const mockRandom = jest.spyOn(Math, 'random');

      // Task 1: "Fix the temporal anomaly" -> Impending Catastrophe (2) + Gentle Giggle (2) -> Score 22
      mockRandom.mockReturnValueOnce(0.4); // DoomLevel: ImpendingCatastrophe (index 1)
      mockRandom.mockReturnValueOnce(0.4); // WhimsyBonus: GentleGiggle (index 1)

      // Task 2: "Feed the void-cat" -> Minor Glitch (1) + Cosmic Joke (3) -> Score 13
      mockRandom.mockReturnValueOnce(0.01); // DoomLevel: MinorGlitch (index 0)
      mockRandom.mockReturnValueOnce(0.99); // WhimsyBonus: CosmicJoke (index 2)

      // Task 3: "Debug the reality distortion field" -> Existential Threat (3) + Faint Sparkle (1) -> Score 31
      mockRandom.mockReturnValueOnce(0.99); // DoomLevel: ExistentialThreat (index 2)
      mockRandom.mockReturnValueOnce(0.01); // WhimsyBonus: FaintSparkle (index 0)

      // Task 4: "Water the mutant cacti" -> Minor Glitch (1) + Faint Sparkle (1) -> Score 11
      mockRandom.mockReturnValueOnce(0.01); // DoomLevel: MinorGlitch (index 0)
      mockRandom.mockReturnValueOnce(0.01); // WhimsyBonus: FaintSparkle (index 0)

      const tasks = [
        "Fix the temporal anomaly",
        "Feed the void-cat",
        "Debug the reality distortion field",
        "Water the mutant cacti"
      ];

      dispatchTasks(tasks);

      // Expected order:
      // 1. Debug the reality distortion field (Score 31)
      // 2. Fix the temporal anomaly (Score 22)
      // 3. Feed the void-cat (Score 13)
      // 4. Water the mutant cacti (Score 11)

      expect(consoleSpy).toHaveBeenCalledTimes(tasks.length + 2); // Header, tasks, footer
      expect(consoleSpy).toHaveBeenCalledWith("\n--- Daily Doom Dispatch ---\n");
      expect(consoleSpy).toHaveBeenCalledWith("1. [Existential Threat + Faint Sparkle] Debug the reality distortion field");
      expect(consoleSpy).toHaveBeenCalledWith("2. [Impending Catastrophe + Gentle Giggle] Fix the temporal anomaly");
      expect(consoleSpy).toHaveBeenCalledWith("3. [Minor Glitch + Cosmic Joke] Feed the void-cat");
      expect(consoleSpy).toHaveBeenCalledWith("4. [Minor Glitch + Faint Sparkle] Water the mutant cacti");
      expect(consoleSpy).toHaveBeenCalledWith("\nMay your efforts avert total annihilation... or at least make it amusing.\n");

      mockRandom.mockRestore();
    });

    it('should sort tasks with same doom level by whimsy bonus (higher whimsy first)', () => {
      const mockRandom = jest.spyOn(Math, 'random');

      // Task A: Impending Catastrophe (2) + Cosmic Joke (3) -> Score 23
      mockRandom.mockReturnValueOnce(0.4); // DoomLevel: ImpendingCatastrophe
      mockRandom.mockReturnValueOnce(0.99); // WhimsyBonus: CosmicJoke

      // Task B: Impending Catastrophe (2) + Faint Sparkle (1) -> Score 21
      mockRandom.mockReturnValueOnce(0.4); // DoomLevel: ImpendingCatastrophe
      mockRandom.mockReturnValueOnce(0.01); // WhimsyBonus: FaintSparkle

      const tasks = ["Task A", "Task B"];
      dispatchTasks(tasks);

      // Expected order: Task A (score 23), Task B (score 21)
      expect(consoleSpy).toHaveBeenCalledWith("1. [Impending Catastrophe + Cosmic Joke] Task A");
      expect(consoleSpy).toHaveBeenCalledWith("2. [Impending Catastrophe + Faint Sparkle] Task B");

      mockRandom.mockRestore();
    });
  });
});
