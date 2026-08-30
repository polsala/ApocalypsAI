import { SnackManager } from '../src/snackManager';
import { Snack } from '../src/types';
import { readFileSync, writeFileSync, existsSync } from 'fs';
import { v4 as uuidv4 } from 'uuid';

// Mock fs module
jest.mock('fs', () => ({
  readFileSync: jest.fn(),
  writeFileSync: jest.fn(),
  existsSync: jest.fn(),
}));

// Mock uuid module
jest.mock('uuid', () => ({
  v4: jest.fn(),
}));

describe('SnackManager', () => {
  const MOCK_DATA_FILE = 'mock_snack_stash.json';
  let manager: SnackManager;

  beforeEach(() => {
    // Reset mocks before each test
    (readFileSync as jest.Mock).mockClear();
    (writeFileSync as jest.Mock).mockClear();
    (existsSync as jest.Mock).mockClear();
    (uuidv4 as jest.Mock).mockClear();

    // Mock existsSync to return false by default (no file initially)
    (existsSync as jest.Mock).mockReturnValue(false);
    // Mock readFileSync to return empty array string by default
    (readFileSync as jest.Mock).mockReturnValue('[]');

    // Initialize manager with a mock file path
    manager = new SnackManager(MOCK_DATA_FILE);
  });

  // Mock rationale: We are testing the business logic of SnackManager,
  // not the file system operations themselves. Mocking `fs` ensures
  // tests are deterministic, fast, and don't leave artifacts on the disk.
  // It isolates the SnackManager logic from external dependencies.

  // Mock rationale: `uuid` is an external dependency for generating unique IDs.
  // Mocking it ensures that generated IDs are predictable for testing purposes,
  // making tests deterministic and easier to assert against specific IDs.

  it('should initialize with an empty stash if data file does not exist', () => {
    (existsSync as jest.Mock).mockReturnValue(false); // # Mock rationale: Simulate no data file existing.
    const newManager = new SnackManager(MOCK_DATA_FILE);
    expect(newManager.listSnacks()).toEqual([]);
    expect(existsSync).toHaveBeenCalledWith(MOCK_DATA_FILE);
    expect(readFileSync).not.toHaveBeenCalled();
  });

  it('should load existing snacks from data file', () => {
    const mockSnacks: Snack[] = [
      { id: '1', name: 'Space Bars', quantity: 3, expirationDate: '2025-01-01' },
    ];
    (existsSync as jest.Mock).mockReturnValue(true); // # Mock rationale: Simulate data file existing.
    (readFileSync as jest.Mock).mockReturnValue(JSON.stringify(mockSnacks)); // # Mock rationale: Provide mock file content.

    const newManager = new SnackManager(MOCK_DATA_FILE);
    expect(newManager.listSnacks()).toEqual(mockSnacks);
    expect(existsSync).toHaveBeenCalledWith(MOCK_DATA_FILE);
    expect(readFileSync).toHaveBeenCalledWith(MOCK_DATA_FILE, 'utf8');
  });

  it('should add a new snack', () => {
    (uuidv4 as jest.Mock).mockReturnValue('mock-uuid-1'); // # Mock rationale: Ensure predictable UUID for testing.
    const newSnack = manager.addSnack('Temporal Taffy', 10, '2024-12-25');
    expect(newSnack).toEqual({
      id: 'mock-uuid-1',
      name: 'Temporal Taffy',
      quantity: 10,
      expirationDate: '2024-12-25',
    });
    expect(manager.listSnacks()).toHaveLength(1);
    expect(writeFileSync).toHaveBeenCalledWith(
      MOCK_DATA_FILE,
      JSON.stringify([newSnack], null, 2),
      'utf8'
    );
  });

  it('should throw error for invalid quantity when adding snack', () => {
    expect(() => manager.addSnack('Bad Snack', 0, '2024-12-25')).toThrow('Quantity must be greater than 0.');
    expect(() => manager.addSnack('Bad Snack', -5, '2024-12-25')).toThrow('Quantity must be greater than 0.');
  });

  it('should throw error for invalid expiration date format when adding snack', () => {
    expect(() => manager.addSnack('Bad Date Snack', 1, 'invalid-date')).toThrow('Invalid expiration date format. Use YYYY-MM-DD.');
  });

  it('should list snacks sorted by expiration date', () => {
    (uuidv4 as jest.Mock)
      .mockReturnValueOnce('id-1') // # Mock rationale: Ensure predictable UUIDs for testing.
      .mockReturnValueOnce('id-2')
      .mockReturnValueOnce('id-3');

    manager.addSnack('Snack C', 1, '2024-12-31');
    manager.addSnack('Snack A', 1, '2024-10-01');
    manager.addSnack('Snack B', 1, '2024-11-15');

    const listedSnacks = manager.listSnacks();
    expect(listedSnacks[0].name).toBe('Snack A');
    expect(listedSnacks[1].name).toBe('Snack B');
    expect(listedSnacks[2].name).toBe('Snack C');
  });

  it('should eat a snack partially', () => {
    (uuidv4 as jest.Mock).mockReturnValue('snack-id-1'); // # Mock rationale: Ensure predictable UUID for testing.
    const initialSnack = manager.addSnack('Quantum Quinoa', 5, '2024-11-01');
    const updatedSnack = manager.eatSnack('snack-id-1', 2);
    expect(updatedSnack?.quantity).toBe(3);
    expect(manager.listSnacks()).toHaveLength(1);
    expect(writeFileSync).toHaveBeenCalledTimes(2); // Add + Eat
  });

  it('should eat a snack fully and remove it', () => {
    (uuidv4 as jest.Mock).mockReturnValue('snack-id-2'); // # Mock rationale: Ensure predictable UUID for testing.
    manager.addSnack('Void Wafers', 3, '2024-10-10');
    const updatedSnack = manager.eatSnack('snack-id-2', 3);
    expect(updatedSnack?.quantity).toBe(0);
    expect(manager.listSnacks()).toHaveLength(0);
    expect(writeFileSync).toHaveBeenCalledTimes(2); // Add + Eat
  });

  it('should return null if snack to eat is not found', () => {
    manager.addSnack('Existential Eclairs', 1, '2024-09-01');
    const result = manager.eatSnack('non-existent-id', 1);
    expect(result).toBeNull();
    expect(writeFileSync).toHaveBeenCalledTimes(1); // Only for add, not for failed eat
  });

  it('should throw error if trying to eat more than available quantity', () => {
    (uuidv4 as jest.Mock).mockReturnValue('snack-id-3'); // # Mock rationale: Ensure predictable UUID for testing.
    manager.addSnack('Reality Rusk', 2, '2024-08-01');
    expect(() => manager.eatSnack('snack-id-3', 3)).toThrow('Cannot eat 3 of Reality Rusk. Only 2 available.');
    expect(manager.listSnacks()[0].quantity).toBe(2); // Quantity should remain unchanged
  });

  it('should throw error for invalid quantity when eating snack', () => {
    (uuidv4 as jest.Mock).mockReturnValue('snack-id-4'); // # Mock rationale: Ensure predictable UUID for testing.
    manager.addSnack('Zero Zest', 1, '2024-07-01');
    expect(() => manager.eatSnack('snack-id-4', 0)).toThrow('Quantity to eat must be greater than 0.');
    expect(() => manager.eatSnack('snack-id-4', -1)).toThrow('Quantity to eat must be greater than 0.');
  });

  it('should suggest snacks sorted by expiration, excluding expired ones', () => {
    const today = new Date();
    today.setHours(0, 0, 0, 0);
    const tomorrow = new Date(today);
    tomorrow.setDate(today.getDate() + 1);
    const yesterday = new Date(today);
    yesterday.setDate(today.getDate() - 1);
    const dayAfterTomorrow = new Date(today);
    dayAfterTomorrow.setDate(today.getDate() + 2);

    const formatDate = (date: Date) => date.toISOString().split('T')[0];

    (uuidv4 as jest.Mock)
      .mockReturnValueOnce('id-expired') // # Mock rationale: Ensure predictable UUIDs for testing.
      .mockReturnValueOnce('id-tomorrow')
      .mockReturnValueOnce('id-today')
      .mockReturnValueOnce('id-future');

    manager.addSnack('Expired Pudding', 1, formatDate(yesterday));
    manager.addSnack('Tomorrow\'s Toast', 1, formatDate(tomorrow));
    manager.addSnack('Today\'s Treat', 1, formatDate(today));
    manager.addSnack('Future Feast', 1, formatDate(dayAfterTomorrow));

    const suggested = manager.suggestSnacks();
    expect(suggested).toHaveLength(3); // Expired Pudding should be filtered out
    expect(suggested[0].name).toBe('Today\'s Treat');
    expect(suggested[1].name).toBe('Tomorrow\'s Toast');
    expect(suggested[2].name).toBe('Future Feast');
  });

  it('should handle empty stash gracefully for suggestions', () => {
    const suggested = manager.suggestSnacks();
    expect(suggested).toEqual([]);
  });

  it('should clear the stash for testing purposes', () => {
    (uuidv4 as jest.Mock).mockReturnValue('id-clear'); // # Mock rationale: Ensure predictable UUID for testing.
    manager.addSnack('Clear Me', 1, '2024-12-31');
    expect(manager.listSnacks()).toHaveLength(1);
    manager._clearStash();
    expect(manager.listSnacks()).toHaveLength(0);
    expect(writeFileSync).toHaveBeenCalledTimes(2); // Add + Clear
  });
});
