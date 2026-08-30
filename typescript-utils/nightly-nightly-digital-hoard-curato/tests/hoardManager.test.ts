import { HoardManager } from '../src/hoardManager';
import { DigitalItem, Scarcity, Utility } from '../src/types';
import * as fs from 'fs';
import * as path from 'path';

// Mock rationale: We mock the 'fs' module to ensure tests are deterministic and do not
// rely on actual file system operations. This prevents side effects and makes tests
// run faster and more reliably in an isolated environment.
jest.mock('fs', () => ({
  existsSync: jest.fn(),
  mkdirSync: jest.fn(),
  readFileSync: jest.fn(),
  writeFileSync: jest.fn(),
}));

// Mock uuidv4 to ensure deterministic IDs for testing
jest.mock('uuid', () => ({
  v4: jest.fn(() => 'test-uuid-123-abc'),
}));

const mockFs = fs as jest.Mocked<typeof fs>;

describe('HoardManager', () => {
  const testDataDir = path.join(process.cwd(), '.test_hoard_data');
  const testDataFilePath = path.join(testDataDir, 'hoard.json');

  beforeEach(() => {
    jest.clearAllMocks();
    // Default mock for existsSync to return false (no file exists initially)
    mockFs.existsSync.mockReturnValue(false);
    // Ensure mkdirSync doesn't throw errors
    mockFs.mkdirSync.mockReturnValue(undefined);
    // Ensure writeFileSync doesn't throw errors
    mockFs.writeFileSync.mockReturnValue(undefined);
  });

  it('should initialize with an empty hoard if no data file exists', () => {
    const manager = new HoardManager(testDataDir);
    expect(manager.listItems()).toEqual([]);
    expect(mockFs.existsSync).toHaveBeenCalledWith(testDataFilePath);
    expect(mockFs.mkdirSync).toHaveBeenCalledWith(testDataDir, { recursive: true });
  });

  it('should load hoard from an existing data file', () => {
    const mockHoard: DigitalItem[] = [
      {
        id: 'existing-id-1',
        name: 'Old Map',
        type: 'file',
        pathOrContent: '/maps/old.jpg',
        scarcity: 'rare',
        utility: 'useful',
        addedAt: '2023-01-01T00:00:00.000Z',
      },
    ];
    mockFs.existsSync.mockImplementation((p) => p === testDataFilePath);
    mockFs.readFileSync.mockReturnValue(JSON.stringify(mockHoard));

    const manager = new HoardManager(testDataDir);
    expect(manager.listItems()).toEqual(mockHoard);
    expect(mockFs.readFileSync).toHaveBeenCalledWith(testDataFilePath, 'utf8');
  });

  it('should add a new item to the hoard and save it', () => {
    const manager = new HoardManager(testDataDir);
    const newItem = manager.addItem(
      'New Discovery',
      'text',
      'A strange glowing rock.',
      'legendary',
      'essential'
    );

    expect(newItem.name).toBe('New Discovery');
    expect(newItem.id).toBe('test-uuid-123-abc'); // From mocked uuidv4
    expect(manager.listItems()).toHaveLength(1);
    expect(mockFs.writeFileSync).toHaveBeenCalledTimes(1);
    expect(JSON.parse(mockFs.writeFileSync.mock.calls[0][1])).toEqual([
      expect.objectContaining({
        name: 'New Discovery',
        scarcity: 'legendary',
        utility: 'essential',
      }),
    ]);
  });

  it('should delete an item from the hoard and save it', () => {
    const manager = new HoardManager(testDataDir);
    const item1 = manager.addItem('Item One', 'text', 'content1', 'common', 'ephemeral');
    const item2 = manager.addItem('Item Two', 'text', 'content2', 'rare', 'useful');

    expect(manager.listItems()).toHaveLength(2);
    const deleted = manager.deleteItem(item1.id);
    expect(deleted).toBe(true);
    expect(manager.listItems()).toHaveLength(1);
    expect(manager.listItems()[0].name).toBe('Item Two');
    expect(mockFs.writeFileSync).toHaveBeenCalledTimes(3); // Initial save + 2 adds + 1 delete
  });

  it('should return false if item to delete is not found', () => {
    const manager = new HoardManager(testDataDir);
    manager.addItem('Item One', 'text', 'content1', 'common', 'ephemeral');
    const deleted = manager.deleteItem('non-existent-id');
    expect(deleted).toBe(false);
    expect(manager.listItems()).toHaveLength(1);
    expect(mockFs.writeFileSync).toHaveBeenCalledTimes(2); // Only for add, not for failed delete
  });

  it('should generate a curation report', () => {
    const manager = new HoardManager(testDataDir);
    manager.addItem('Old World Map', 'file', '/maps/old.jpg', 'legendary', 'essential');
    manager.addItem('Broken Radio', 'text', 'static noise', 'common', 'ephemeral');
    manager.addItem('Water Purification Manual', 'url', 'http://wiki.com/water', 'rare', 'useful');
    manager.addItem('Family Photo', 'file', '/pics/family.png', 'legendary', 'archive');

    const report = manager.generateCurationReport();
    expect(report).toContain('--- Digital Hoard Curation Report ---');
    expect(report).toContain('Legendary & Essential Items (PRIORITY BACKUP!):');
    expect(report).toContain('  - [test-uuid-] Old World Map (file)');
    expect(report).toContain('Rare & Useful Items (Consider Backup):');
    expect(report).toContain('  - [test-uuid-] Water Purification Manual (url)');
    expect(report).toContain('Ephemeral Items (Review for Deletion):');
    expect(report).toContain('  - [test-uuid-] Broken Radio (text)');
    expect(report).toContain('Archive Items (Verify Redundancy):');
    expect(report).toContain('  - [test-uuid-] Family Photo (file)');
    expect(report).toContain('--- End Report ---');
  });

  it('should handle empty hoard in report', () => {
    const manager = new HoardManager(testDataDir);
    const report = manager.generateCurationReport();
    expect(report).toContain('Your hoard is empty. Time to scavenge!');
  });

  it('should handle corrupted data file gracefully', () => {
    mockFs.existsSync.mockImplementation((p) => p === testDataFilePath);
    mockFs.readFileSync.mockReturnValue('invalid json');
    const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {}); // Mock console.error

    const manager = new HoardManager(testDataDir);
    expect(manager.listItems()).toEqual([]); // Should be empty after error
    expect(consoleErrorSpy).toHaveBeenCalledWith(expect.stringContaining('Failed to load hoard data:'), expect.any(Error));
    consoleErrorSpy.mockRestore();
  });
});
