import { RegretManager } from '../src/regretManager';
import { RegretData } from '../src/types';
import { readFileSync, writeFileSync, existsSync } from 'fs';
import path from 'path';

// Mock fs module
jest.mock('fs', () => ({
  // # Mock rationale: We mock fs functions to prevent actual file system
  // # interactions during tests, ensuring determinism and isolation.
  // # This allows tests to control the initial state and verify the
  // # output without side effects or requiring a real file.
  readFileSync: jest.fn(),
  writeFileSync: jest.fn(),
  existsSync: jest.fn(),
}));

const mockReadFileSync = readFileSync as jest.Mock;
const mockWriteFileSync = writeFileSync as jest.Mock;
const mockExistsSync = existsSync as jest.Mock;

const TEST_FILE_PATH = path.join(__dirname, 'test_temporal_echoes.json');

describe('RegretManager', () => {
  let manager: RegretManager;

  beforeEach(() => {
    // Reset mocks before each test
    mockReadFileSync.mockClear();
    mockWriteFileSync.mockClear();
    mockExistsSync.mockClear();

    // Default mock behavior: file does not exist initially
    mockExistsSync.mockReturnValue(false);
    mockReadFileSync.mockReturnValue(JSON.stringify({ active: [], resolved: [] }));

    manager = new RegretManager(TEST_FILE_PATH);
  });

  it('should initialize with empty data if file does not exist', () => {
    expect(manager.listActiveRegrets()).toEqual([]);
    expect(manager.listResolvedRegrets()).toEqual([]);
    expect(mockExistsSync).toHaveBeenCalledWith(TEST_FILE_PATH);
    expect(mockReadFileSync).not.toHaveBeenCalled(); // Because existsSync returned false
  });

  it('should load existing data from file', () => {
    const initialData: RegretData = {
      active: [{ id: '1', description: 'Active regret', timestamp: '2023-01-01T00:00:00Z' }],
      resolved: [{ id: '2', description: 'Resolved regret', timestamp: '2023-01-02T00:00:00Z', resolvedAt: '2023-01-03T00:00:00Z' }],
    };
    mockExistsSync.mockReturnValue(true);
    mockReadFileSync.mockReturnValue(JSON.stringify(initialData));

    manager = new RegretManager(TEST_FILE_PATH); // Re-initialize to load mocked data

    expect(manager.listActiveRegrets()).toEqual(initialData.active);
    expect(manager.listResolvedRegrets()).toEqual(initialData.resolved);
    expect(mockExistsSync).toHaveBeenCalledWith(TEST_FILE_PATH);
    expect(mockReadFileSync).toHaveBeenCalledWith(TEST_FILE_PATH, 'utf8');
  });

  it('should add a new regret and save data', () => {
    const description = 'Forgot to water the digital plants.';
    const newRegret = manager.addRegret(description);

    expect(newRegret).toHaveProperty('id');
    expect(newRegret.description).toBe(description);
    expect(newRegret).toHaveProperty('timestamp');
    expect(manager.listActiveRegrets()).toContainEqual(newRegret);
    expect(mockWriteFileSync).toHaveBeenCalledTimes(1);
    const savedData = JSON.parse(mockWriteFileSync.mock.calls[0][1]);
    expect(savedData.active).toContainEqual(newRegret);
  });

  it('should list active regrets correctly', () => {
    manager.addRegret('Active 1');
    manager.addRegret('Active 2');
    const active = manager.listActiveRegrets();
    expect(active.length).toBe(2);
    expect(active[0].description).toBe('Active 1');
    expect(active[1].description).toBe('Active 2');
  });

  it('should resolve a regret and move it to resolved list', () => {
    const regret1 = manager.addRegret('Missed the temporal bus.');
    const regret2 = manager.addRegret('Accidentally time-traveled to Tuesday.');

    const resolvedRegret = manager.resolveRegret(regret1.id);

    expect(resolvedRegret).toBeDefined();
    expect(resolvedRegret?.id).toBe(regret1.id);
    expect(resolvedRegret).toHaveProperty('resolvedAt');
    expect(manager.listActiveRegrets()).not.toContainEqual(regret1);
    expect(manager.listActiveRegrets()).toContainEqual(regret2);
    expect(manager.listResolvedRegrets()).toContainEqual(resolvedRegret);
    expect(mockWriteFileSync).toHaveBeenCalledTimes(2); // Add then Resolve
    const savedData = JSON.parse(mockWriteFileSync.mock.calls[1][1]);
    expect(savedData.active).not.toContainEqual(regret1);
    expect(savedData.resolved).toContainEqual(resolvedRegret);
  });

  it('should return undefined if resolving a non-existent regret', () => {
    manager.addRegret('Existing regret');
    const resolved = manager.resolveRegret('non-existent-id');
    expect(resolved).toBeUndefined();
    expect(manager.listActiveRegrets().length).toBe(1); // No change
    expect(manager.listResolvedRegrets().length).toBe(0); // No change
    expect(mockWriteFileSync).toHaveBeenCalledTimes(1); // Only for the add operation
  });

  it('should list resolved regrets correctly', () => {
    const regret1 = manager.addRegret('Regret A');
    const regret2 = manager.addRegret('Regret B');
    manager.resolveRegret(regret1.id);
    manager.resolveRegret(regret2.id);

    const resolved = manager.listResolvedRegrets();
    expect(resolved.length).toBe(2);
    expect(resolved[0].description).toBe('Regret A');
    expect(resolved[1].description).toBe('Regret B');
  });

  it('should handle empty file content gracefully', () => {
    mockExistsSync.mockReturnValue(true);
    mockReadFileSync.mockReturnValue(''); // Empty file content
    console.error = jest.fn(); // Mock console.error to prevent noise

    manager = new RegretManager(TEST_FILE_PATH);
    expect(manager.listActiveRegrets()).toEqual([]);
    expect(manager.listResolvedRegrets()).toEqual([]);
    expect(console.error).toHaveBeenCalled(); // Expect an error message
  });

  it('should handle invalid JSON content gracefully', () => {
    mockExistsSync.mockReturnValue(true);
    mockReadFileSync.mockReturnValue('{"active": ['); // Invalid JSON
    console.error = jest.fn(); // Mock console.error to prevent noise

    manager = new RegretManager(TEST_FILE_PATH);
    expect(manager.listActiveRegrets()).toEqual([]);
    expect(manager.listResolvedRegrets()).toEqual([]);
    expect(console.error).toHaveBeenCalled(); // Expect an error message
  });

  it('should clear data for testing purposes', () => {
    manager.addRegret('Temp regret');
    expect(manager.listActiveRegrets().length).toBe(1);
    (manager as any)._clearData(); // Access private method for testing
    expect(manager.listActiveRegrets()).toEqual([]);
    expect(manager.listResolvedRegrets()).toEqual([]);
    expect(mockWriteFileSync).toHaveBeenCalledTimes(2); // Add then Clear
    const savedData = JSON.parse(mockWriteFileSync.mock.calls[1][1]);
    expect(savedData.active).toEqual([]);
    expect(savedData.resolved).toEqual([]);
  });
});
