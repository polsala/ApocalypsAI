import { ScavengerManifest } from '../src/manifest';
import { ScavengedItem, ManifestData } from '../src/types';
import { promises as fs } from 'node:fs';

// Mock rationale: We need to control file system interactions to ensure tests are deterministic
// and do not rely on actual file creation/deletion, which could lead to race conditions or
// leave artifacts. Mocking 'node:fs/promises' allows us to simulate file operations in memory.
jest.mock('node:fs/promises', () => ({
  readFile: jest.fn(),
  writeFile: jest.fn(),
}));

const mockReadFile = fs.readFile as jest.MockedFunction<typeof fs.readFile>;
const mockWriteFile = fs.writeFile as jest.MockedFunction<typeof fs.writeFile>;

// Mock uuid to ensure consistent IDs for testing
jest.mock('uuid', () => ({
  v4: jest.fn(() => 'mock-uuid-123'),
}));

describe('ScavengerManifest', () => {
  let manifest: ScavengerManifest;
  const initialManifestData: ManifestData = { items: [] };

  beforeEach(() => {
    // Reset mocks before each test
    mockReadFile.mockReset();
    mockWriteFile.mockReset();
    // Ensure manifest starts clean for each test
    mockReadFile.mockResolvedValue(JSON.stringify(initialManifestData));
    manifest = new ScavengerManifest();
  });

  it('should initialize with an empty manifest if file does not exist', async () => {
    mockReadFile.mockRejectedValueOnce({ code: 'ENOENT' }); // Simulate file not found
    const newManifest = new ScavengerManifest();
    // Wait for constructor's async loadManifest to complete
    await (newManifest as any).loadManifest(); 
    expect(await newManifest.listItems()).toEqual([]);
    expect(mockWriteFile).toHaveBeenCalledTimes(1); // Should create an empty file
  });

  it('should add an item to the manifest', async () => {
    const item = await manifest.addItem('Rusty Knife', 'Weapon', 'Worn', 1, 'Good for opening cans.');
    expect(item).toHaveProperty('id', 'mock-uuid-123');
    expect(item.name).toBe('Rusty Knife');
    expect(item.condition).toBe('Worn');
    expect(item.quantity).toBe(1);
    expect(item.notes).toBe('Good for opening cans.');
    expect(mockWriteFile).toHaveBeenCalledTimes(1);

    const expectedData = {
      items: [
        expect.objectContaining({
          id: 'mock-uuid-123',
          name: 'Rusty Knife',
          category: 'Weapon',
          condition: 'Worn',
          quantity: 1,
          notes: 'Good for opening cans.',
        }),
      ],
    };
    expect(mockWriteFile).toHaveBeenCalledWith('manifest.json', JSON.stringify(expectedData, null, 2), 'utf-8');
  });

  it('should list all items in the manifest', async () => {
    const existingItem: ScavengedItem = {
      id: 'existing-id-1',
      name: 'Water Purifier',
      category: 'Survival',
      condition: 'Good',
      quantity: 1,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };
    mockReadFile.mockResolvedValueOnce(JSON.stringify({ items: [existingItem] }));
    const newManifest = new ScavengerManifest();
    await (newManifest as any).loadManifest(); // Ensure data is loaded

    const items = await newManifest.listItems();
    expect(items).toEqual([existingItem]);
    expect(mockReadFile).toHaveBeenCalledTimes(2); // Once in constructor, once in listItems
  });

  it('should update an existing item', async () => {
    const itemToUpdate: ScavengedItem = {
      id: 'update-id-1',
      name: 'Old Radio',
      category: 'Electronics',
      condition: 'Broken',
      quantity: 1,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };
    mockReadFile.mockResolvedValueOnce(JSON.stringify({ items: [itemToUpdate] }));
    const newManifest = new ScavengerManifest();
    await (newManifest as any).loadManifest();

    const updatedItem = await newManifest.updateItem('update-id-1', { condition: 'Worn', notes: 'Static on most channels.' });

    expect(updatedItem).not.toBeNull();
    expect(updatedItem?.condition).toBe('Worn');
    expect(updatedItem?.notes).toBe('Static on most channels.');
    expect(updatedItem?.updatedAt).not.toBe(itemToUpdate.updatedAt);
    expect(mockWriteFile).toHaveBeenCalledTimes(1);
  });

  it('should return null if item to update is not found', async () => {
    mockReadFile.mockResolvedValueOnce(JSON.stringify(initialManifestData));
    const newManifest = new ScavengerManifest();
    await (newManifest as any).loadManifest();

    const updatedItem = await newManifest.updateItem('non-existent-id', { name: 'New Name' });
    expect(updatedItem).toBeNull();
    expect(mockWriteFile).not.toHaveBeenCalled(); // No save should happen
  });

  it('should remove an item from the manifest', async () => {
    const itemToRemove: ScavengedItem = {
      id: 'remove-id-1',
      name: 'Empty Bottle',
      category: 'Junk',
      condition: 'Pristine',
      quantity: 5,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };
    mockReadFile.mockResolvedValueOnce(JSON.stringify({ items: [itemToRemove] }));
    const newManifest = new ScavengerManifest();
    await (newManifest as any).loadManifest();

    const removed = await newManifest.removeItem('remove-id-1');
    expect(removed).toBe(true);
    expect(mockWriteFile).toHaveBeenCalledTimes(1);
    expect(await newManifest.listItems()).toEqual([]);
  });

  it('should return false if item to remove is not found', async () => {
    mockReadFile.mockResolvedValueOnce(JSON.stringify(initialManifestData));
    const newManifest = new ScavengerManifest();
    await (newManifest as any).loadManifest();

    const removed = await newManifest.removeItem('non-existent-id');
    expect(removed).toBe(false);
    expect(mockWriteFile).not.toHaveBeenCalled();
  });

  it('should search items by name', async () => {
    const item1: ScavengedItem = {
      id: 's1',
      name: 'Scrap Metal',
      category: 'Material',
      condition: 'Worn',
      quantity: 10,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };
    const item2: ScavengedItem = {
      id: 's2',
      name: 'Rusty Pipe',
      category: 'Material',
      condition: 'Damaged',
      quantity: 3,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };
    const item3: ScavengedItem = {
      id: 's3',
      name: 'Medical Kit',
      category: 'Medical',
      condition: 'Good',
      quantity: 1,
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };
    mockReadFile.mockResolvedValueOnce(JSON.stringify({ items: [item1, item2, item3] }));
    const newManifest = new ScavengerManifest();
    await (newManifest as any).loadManifest();

    const results = await newManifest.searchItems('scrap', 'name');
    expect(results).toEqual([item1]);
  });

  it('should search items across multiple fields if no field is specified', async () => {
    const item1: ScavengedItem = {
      id: 's1',
      name: 'Scrap Metal',
      category: 'Material',
      condition: 'Worn',
      quantity: 10,
      notes: 'Useful for repairs',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };
    const item2: ScavengedItem = {
      id: 's2',
      name: 'Rusty Pipe',
      category: 'Tool',
      condition: 'Damaged',
      quantity: 3,
      notes: 'Can be used as a weapon',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };
    const item3: ScavengedItem = {
      id: 's3',
      name: 'Medical Kit',
      category: 'Medical',
      condition: 'Good',
      quantity: 1,
      notes: 'Contains bandages',
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };
    mockReadFile.mockResolvedValueOnce(JSON.stringify({ items: [item1, item2, item3] }));
    const newManifest = new ScavengerManifest();
    await (newManifest as any).loadManifest();

    const results = await newManifest.searchItems('tool');
    expect(results).toEqual([item2]); // Matches category 'Tool'

    const results2 = await newManifest.searchItems('repairs');
    expect(results2).toEqual([item1]); // Matches notes 'Useful for repairs'

    const results3 = await newManifest.searchItems('damaged');
    expect(results3).toEqual([item2]); // Matches condition 'Damaged'
  });

  it('should handle errors during manifest loading', async () => {
    mockReadFile.mockRejectedValueOnce(new Error('Permission denied'));
    const newManifest = new ScavengerManifest();
    // Wait for constructor's async loadManifest to complete
    await (newManifest as any).loadManifest();
    expect(await newManifest.listItems()).toEqual([]); // Should still be empty
    expect(console.error).toHaveBeenCalledWith(expect.stringContaining('Error loading manifest: Permission denied'));
  });

  it('should handle errors during manifest saving', async () => {
    mockWriteFile.mockRejectedValueOnce(new Error('Disk full'));
    // Mock console.error to prevent test output pollution
    const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});

    await manifest.addItem('Broken Watch', 'Junk', 'Broken', 1);
    expect(consoleErrorSpy).toHaveBeenCalledWith(expect.stringContaining('Error saving manifest: Disk full'));
    consoleErrorSpy.mockRestore();
  });
});
