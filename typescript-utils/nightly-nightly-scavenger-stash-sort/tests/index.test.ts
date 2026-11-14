import {
  Item,
  ApocalypticCategory,
  CategorizedItem,
  Scarcity
} from '../src/types';
import {
  DEFAULT_CATEGORIES,
  categorizeItem,
  sortStash,
  formatCategorizedItem,
  runCli
} from '../src/index';

describe('Scavenger Stash Sorter', () => {

  const testCategories: ApocalypticCategory[] = [
    { name: 'High Value', minScore: 70, maxScore: 100, priority: 1, description: 'High utility' },
    { name: 'Medium Value', minScore: 30, maxScore: 69, priority: 2, description: 'Medium utility' },
    { name: 'Low Value', minScore: 0, maxScore: 29, priority: 3, description: 'Low utility' },
  ];

  const item1: Item = { name: 'Water Filter', description: 'Filters dirty water', rawUtilityScore: 90, scarcity: 'Scarce' };
  const item2: Item = { name: 'Rusty Axe', description: 'Chopping wood, defense', rawUtilityScore: 75, scarcity: 'Common' };
  const item3: Item = { name: 'Old Map', description: 'Shows pre-apocalypse roads', rawUtilityScore: 45, scarcity: 'Rare' };
  const item4: Item = { name: 'Shiny Pebble', description: 'Looks nice', rawUtilityScore: 5, scarcity: 'Abundant' };
  const item5: Item = { name: 'First Aid Kit', description: 'Treats injuries', rawUtilityScore: 85, scarcity: 'Scarce' };
  const item6: Item = { name: 'Can of Beans', description: 'Edible food', rawUtilityScore: 65, scarcity: 'Common' };

  describe('categorizeItem', () => {
    test('should correctly categorize an item into High Value', () => {
      const categorized = categorizeItem(item1, testCategories);
      expect(categorized.category.name).toBe('High Value');
      expect(categorized.item).toEqual(item1);
    });

    test('should correctly categorize an item into Medium Value', () => {
      const categorized = categorizeItem(item3, testCategories);
      expect(categorized.category.name).toBe('Medium Value');
      expect(categorized.item).toEqual(item3);
    });

    test('should correctly categorize an item into Low Value', () => {
      const categorized = categorizeItem(item4, testCategories);
      expect(categorized.category.name).toBe('Low Value');
      expect(categorized.item).toEqual(item4);
    });

    test('should use DEFAULT_CATEGORIES if none are provided', () => {
      const categorized = categorizeItem(item1); // Using default categories
      expect(categorized.category.name).toBe('Survival Essentials');
    });

    test('should throw an error if no category matches the score', () => {
      const customCategories: ApocalypticCategory[] = [
        { name: 'Only 50', minScore: 50, maxScore: 50, priority: 1, description: '' }
      ];
      const item = { name: 'Odd Item', description: '', rawUtilityScore: 51, scarcity: 'Common' };
      expect(() => categorizeItem(item, customCategories)).toThrowError(/could not be assigned/);
    });
  });

  describe('sortStash', () => {
    test('should sort items by category priority then by utility score', () => {
      const itemsToSort = [item4, item3, item1, item2, item5, item6];
      const sorted = sortStash(itemsToSort, DEFAULT_CATEGORIES);

      // Expected order based on DEFAULT_CATEGORIES:
      // Survival Essentials (Prio 1): Water Filter (90), First Aid Kit (85)
      // Tactical Gear (Prio 2): Rusty Axe (75)
      // Resource & Crafting (Prio 3): Can of Beans (65), Old Map (45)
      // Barter & Trade (Prio 4): (none in this set)
      // Curiosities & Morale (Prio 5): Shiny Pebble (5)

      expect(sorted.length).toBe(6);
      expect(sorted[0].item.name).toBe('Water Filter'); // Prio 1, Score 90
      expect(sorted[1].item.name).toBe('First Aid Kit'); // Prio 1, Score 85
      expect(sorted[2].item.name).toBe('Rusty Axe'); // Prio 2, Score 75
      expect(sorted[3].item.name).toBe('Can of Beans'); // Prio 3, Score 65
      expect(sorted[4].item.name).toBe('Old Map'); // Prio 3, Score 45
      expect(sorted[5].item.name).toBe('Shiny Pebble'); // Prio 5, Score 5
    });

    test('should handle an empty list of items', () => {
      expect(sortStash([], DEFAULT_CATEGORIES)).toEqual([]);
    });
  });

  describe('formatCategorizedItem', () => {
    test('should format an item correctly', () => {
      const categorized = categorizeItem(item1, DEFAULT_CATEGORIES);
      const formatted = formatCategorizedItem(categorized);
      expect(formatted).toBe('[Survival Essentials (Prio: 1)] Water Filter (Score: 90, Scarcity: Scarce) - Filters dirty water');
    });
  });

  describe('runCli', () => {
    let consoleSpy: jest.SpyInstance;

    beforeEach(() => {
      consoleSpy = jest.spyOn(console, 'log').mockImplementation(() => {});
      jest.spyOn(console, 'error').mockImplementation(() => {}); // Mock error too
    });

    afterEach(() => {
      consoleSpy.mockRestore();
      (console.error as jest.Mock).mockRestore();
    });

    // Mock rationale: We are testing the CLI output, so we need to capture what `console.log` prints without actually printing to the console during tests.
    test('should print usage if no arguments are provided', () => {
      runCli([]);
      expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining("Usage: npm start"));
    });

    test('should process and print sorted items from CLI arguments', () => {
      const args = [
        "Water Purifier|Filters contaminated water|95|Scarce",
        "Rusty Spoon|Good for digging|10|Abundant",
        "Medkit|Heals wounds|88|Rare"
      ];
      runCli(args);

      expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining("--- Your Sorted Scavenger's Stash ---"));
      expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining("[Survival Essentials (Prio: 1)] Water Purifier (Score: 95, Scarcity: Scarce) - Filters contaminated water"));
      expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining("[Survival Essentials (Prio: 1)] Medkit (Score: 88, Scarcity: Rare) - Heals wounds"));
      expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining("[Curiosities & Morale (Prio: 5)] Rusty Spoon (Score: 10, Scarcity: Abundant) - Good for digging"));
      expect(consoleSpy).toHaveBeenCalledWith(expect.stringContaining("-------------------------------------"));

      // Ensure the order is correct
      const calls = consoleSpy.mock.calls.map(call => call[0]);
      const sortedOutput = calls.filter(line => line.startsWith('['));
      expect(sortedOutput[0]).toContain('Water Purifier');
      expect(sortedOutput[1]).toContain('Medkit');
      expect(sortedOutput[2]).toContain('Rusty Spoon');
    });

    test('should log an error for invalid item format', () => {
      runCli(["Invalid Item"]);
      expect(console.error).toHaveBeenCalledWith(expect.stringContaining("Error: Invalid item format"));
      expect(consoleSpy).not.toHaveBeenCalledWith(expect.stringContaining("--- Your Sorted Scavenger's Stash ---"));
    });

    test('should log an error for invalid utility score', () => {
      runCli(["Item|Desc|abc|Common"]);
      expect(console.error).toHaveBeenCalledWith(expect.stringContaining("Error: Invalid utility score"));
      expect(consoleSpy).not.toHaveBeenCalledWith(expect.stringContaining("--- Your Sorted Scavenger's Stash ---"));
    });

    test('should log an error for out-of-range utility score', () => {
      runCli(["Item|Desc|101|Common"]);
      expect(console.error).toHaveBeenCalledWith(expect.stringContaining("Error: Invalid utility score"));
      expect(consoleSpy).not.toHaveBeenCalledWith(expect.stringContaining("--- Your Sorted Scavenger's Stash ---"));
    });

    test('should log an error for invalid scarcity', () => {
        runCli(["Item|Desc|50|NonExistent"]);
        expect(console.error).toHaveBeenCalledWith(expect.stringContaining("Error: Invalid scarcity"));
        expect(consoleSpy).not.toHaveBeenCalledWith(expect.stringContaining("--- Your Sorted Scavenger's Stash ---"));
    });
  });
});
