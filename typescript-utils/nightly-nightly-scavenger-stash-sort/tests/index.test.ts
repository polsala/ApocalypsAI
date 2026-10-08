import { sortItemsIntoStashes } from '../src/sorter';
import { Item, StashCategory } from '../src/types';
import { defaultCategories } from '../src/categories';
import { readFileSync } from 'fs'; // # Mock rationale: Used for testing file reading logic, but actual file system access is mocked.
import * as path from 'path'; // # Mock rationale: Used for resolving file paths, but actual file system access is mocked.

// Mock fs.readFileSync to prevent actual file system access during tests
jest.mock('fs', () => ({
  readFileSync: jest.fn(),
}));

describe('Stash Sorter', () => {
  const mockItems: Item[] = [
    { name: 'Rusty Can Opener', type: 'Tool', weight: 0.5, volume: 0.1, value: 5 },
    { name: 'Purified Water Bottle', type: 'Water', weight: 1.0, volume: 1.0, value: 20 },
    { name: 'Moldy Bread', type: 'Food', weight: 0.2, volume: 0.2, value: 2 },
    { name: 'Pre-War Comic Book', type: 'Relic', weight: 0.1, volume: 0.05, value: 150 },
    { name: 'Scrap Metal (x10)', type: 'Component', weight: 2.0, volume: 0.5, value: 10 },
    { name: 'Broken Goggles', type: 'Junk', weight: 0.1, volume: 0.1, value: 1 },
    { name: 'Medical Kit', type: 'Medicine', weight: 0.8, volume: 0.3, value: 75 },
    { name: 'Ancient Map', type: 'Relic', weight: 0.1, volume: 0.05, value: 40 }, // Lower value relic
    { name: 'Heavy Pipe Wrench', type: 'Tool', weight: 3.0, volume: 0.5, value: 12 }, // High value tool
    { name: 'Broken Toy Car', type: 'Toy', weight: 0.1, volume: 0.1, value: 3 },
    { name: 'Rare Book', type: 'Book', weight: 0.3, volume: 0.2, value: 60 }
  ];

  it('should correctly sort items into default categories', () => {
    const sorted = sortItemsIntoStashes(mockItems, defaultCategories);

    expect(sorted['Survival Essentials']).toEqual(expect.arrayContaining([
      { name: 'Purified Water Bottle', type: 'Water', weight: 1.0, volume: 1.0, value: 20 },
      { name: 'Moldy Bread', type: 'Food', weight: 0.2, volume: 0.2, value: 2 },
      { name: 'Medical Kit', type: 'Medicine', weight: 0.8, volume: 0.3, value: 75 },
      { name: 'Heavy Pipe Wrench', type: 'Tool', weight: 3.0, volume: 0.5, value: 12 } // Tool with value > 10
    ]));
    expect(sorted['Survival Essentials']).not.toEqual(expect.arrayContaining([
      { name: 'Rusty Can Opener', type: 'Tool', weight: 0.5, volume: 0.1, value: 5 } // Tool with value <= 10
    ]));

    expect(sorted['Tradeable Trinkets']).toEqual(expect.arrayContaining([
      { name: 'Pre-War Comic Book', type: 'Relic', weight: 0.1, volume: 0.05, value: 150 } // Relic with value > 50
    ]));
    expect(sorted['Tradeable Trinkets']).not.toEqual(expect.arrayContaining([
      { name: 'Ancient Map', type: 'Relic', weight: 0.1, volume: 0.05, value: 40 } // Relic with value <= 50
    ]));

    expect(sorted['Curious Collectibles']).toEqual(expect.arrayContaining([
      { name: 'Ancient Map', type: 'Relic', weight: 0.1, volume: 0.05, value: 40 }, // Relic not caught by Tradeable Trinkets
      { name: 'Broken Toy Car', type: 'Toy', weight: 0.1, volume: 0.1, value: 3 },
      { name: 'Rare Book', type: 'Book', weight: 0.3, volume: 0.2, value: 60 }
    ]));
    expect(sorted['Curious Collectibles']).not.toEqual(expect.arrayContaining([
      { name: 'Pre-War Comic Book', type: 'Relic', weight: 0.1, volume: 0.05, value: 150 } // Should be in Tradeable Trinkets due to priority
    ]));

    expect(sorted['Scrap & Salvage']).toEqual(expect.arrayContaining([
      { name: 'Scrap Metal (x10)', type: 'Component', weight: 2.0, volume: 0.5, value: 10 }, // Component, weight > 1.5, value < 15
      { name: 'Broken Goggles', type: 'Junk', weight: 0.1, volume: 0.1, value: 1 },
      { name: 'Rusty Can Opener', type: 'Tool', weight: 0.5, volume: 0.1, value: 5 } // Tool not caught by Survival Essentials
    ]));

    // Ensure no item is duplicated across categories (due to priority)
    const allSortedItems = Object.values(sorted).flat();
    expect(allSortedItems.length).toBe(mockItems.length);
    expect(new Set(allSortedItems.map(item => item.name)).size).toBe(mockItems.length);
  });

  it('should handle empty items array', () => {
    const sorted = sortItemsIntoStashes([], defaultCategories);
    expect(Object.keys(sorted).length).toBe(defaultCategories.length);
    defaultCategories.forEach(cat => {
      expect(sorted[cat.name]).toEqual([]);
    });
  });

  it('should handle items that do not match any category', () => {
    const customCategories: StashCategory[] = [
      { name: 'Only Food', priority: 100, rules: [(item) => item.type === 'Food'] }
    ];
    const items: Item[] = [
      { name: 'Water', type: 'Water', weight: 1, volume: 1, value: 10 },
      { name: 'Apple', type: 'Food', weight: 0.1, volume: 0.1, value: 5 }
    ];

    const sorted = sortItemsIntoStashes(items, customCategories);
    expect(sorted['Only Food']).toEqual([{ name: 'Apple', type: 'Food', weight: 0.1, volume: 0.1, value: 5 }]);
    expect(sorted['Only Food'].length).toBe(1);
    // Water should not be in any category as it doesn't match
    expect(Object.values(sorted).flat().length).toBe(1);
  });

  it('should prioritize categories correctly', () => {
    const customCategories: StashCategory[] = [
      { name: 'High Priority Tools', priority: 200, rules: [(item) => item.type === 'Tool'] },
      { name: 'Low Priority Tools', priority: 100, rules: [(item) => item.type === 'Tool'] }
    ];
    const items: Item[] = [
      { name: 'Hammer', type: 'Tool', weight: 1, volume: 0.5, value: 20 }
    ];

    const sorted = sortItemsIntoStashes(items, customCategories);
    expect(sorted['High Priority Tools']).toEqual([{ name: 'Hammer', type: 'Tool', weight: 1, volume: 0.5, value: 20 }]);
    expect(sorted['Low Priority Tools']).toEqual([]); // Should not be assigned here due to higher priority match
  });

  it('should integrate with main CLI logic for file reading', async () => {
    // Mock the readFileSync implementation for this specific test
    const mockReadFileSync = readFileSync as jest.Mock;
    mockReadFileSync.mockReturnValueOnce(JSON.stringify([
      { name: 'Test Food', type: 'Food', weight: 0.1, volume: 0.1, value: 5 }
    ]));

    // Mock process.argv for CLI arguments
    const originalArgv = process.argv;
    process.argv = ['node', 'index.js', 'mock-items.json']; // # Mock rationale: Simulates command line arguments for the CLI entry point.

    // Mock console.log to capture output
    const consoleSpy = jest.spyOn(console, 'log').mockImplementation(() => {});
    const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
    const processExitSpy = jest.spyOn(process, 'exit').mockImplementation((code?: number) => { throw new Error(`process.exit: ${code}`); }); // # Mock rationale: Prevents actual process exit during tests.

    // Dynamically import index.ts to run its main function
    // This is a common pattern for testing CLI entry points
    await import('../src/index');

    expect(mockReadFileSync).toHaveBeenCalledWith('mock-items.json', 'utf8');
    expect(consoleSpy).toHaveBeenCalledWith(JSON.stringify({
      'Survival Essentials': [{ name: 'Test Food', type: 'Food', weight: 0.1, volume: 0.1, value: 5 }],
      'Tradeable Trinkets': [],
      'Curious Collectibles': [],
      'Scrap & Salvage': []
    }, null, 2));
    expect(consoleErrorSpy).not.toHaveBeenCalled();
    expect(processExitSpy).not.toHaveBeenCalled();

    // Restore mocks
    consoleSpy.mockRestore();
    consoleErrorSpy.mockRestore();
    processExitSpy.mockRestore();
    process.argv = originalArgv;

    // Clear module cache for index.ts to allow re-import in subsequent tests
    jest.resetModules();
  });

  it('should handle file not found error in main CLI logic', async () => {
    const mockReadFileSync = readFileSync as jest.Mock;
    mockReadFileSync.mockImplementationOnce(() => {
      throw new Error('ENOENT: no such file or directory');
    });

    const originalArgv = process.argv;
    process.argv = ['node', 'index.js', 'non-existent.json']; // # Mock rationale: Simulates command line arguments for the CLI entry point.

    const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
    const processExitSpy = jest.spyOn(process, 'exit').mockImplementation((code?: number) => { throw new Error(`process.exit: ${code}`); }); // # Mock rationale: Prevents actual process exit during tests.

    let errorThrown = false;
    try {
      await import('../src/index');
    } catch (e: any) {
      if (e.message.startsWith('process.exit')) {
        errorThrown = true;
      }
    }

    expect(mockReadFileSync).toHaveBeenCalledWith('non-existent.json', 'utf8');
    expect(consoleErrorSpy).toHaveBeenCalledWith(expect.stringContaining('Error processing items file: ENOENT: no such file or directory'));
    expect(processExitSpy).toHaveBeenCalledWith(1);
    expect(errorThrown).toBe(true);

    consoleErrorSpy.mockRestore();
    processExitSpy.mockRestore();
    process.argv = originalArgv;

    // Clear module cache for index.ts to allow re-import in subsequent tests
    jest.resetModules();
  });

  it('should handle invalid JSON file error in main CLI logic', async () => {
    const mockReadFileSync = readFileSync as jest.Mock;
    mockReadFileSync.mockReturnValueOnce('{"items": [invalid json]}');

    const originalArgv = process.argv;
    process.argv = ['node', 'index.js', 'invalid.json']; // # Mock rationale: Simulates command line arguments for the CLI entry point.

    const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
    const processExitSpy = jest.spyOn(process, 'exit').mockImplementation((code?: number) => { throw new Error(`process.exit: ${code}`); }); // # Mock rationale: Prevents actual process exit during tests.

    let errorThrown = false;
    try {
      await import('../src/index');
    } catch (e: any) {
      if (e.message.startsWith('process.exit')) {
        errorThrown = true;
      }
    }

    expect(mockReadFileSync).toHaveBeenCalledWith('invalid.json', 'utf8');
    expect(consoleErrorSpy).toHaveBeenCalledWith(expect.stringContaining('Error processing items file: Unexpected token'));
    expect(processExitSpy).toHaveBeenCalledWith(1);
    expect(errorThrown).toBe(true);

    consoleErrorSpy.mockRestore();
    processExitSpy.mockRestore();
    process.argv = originalArgv;

    // Clear module cache for index.ts to allow re-import in subsequent tests
    jest.resetModules();
  });
});
