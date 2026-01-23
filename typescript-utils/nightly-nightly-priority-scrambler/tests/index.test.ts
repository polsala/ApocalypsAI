import { readFileSync } from 'fs';
import { Item, Config } from '../src/types';
import { calculateScore, loadJson } from '../src/index';

// Mock fs.readFileSync to prevent actual file system access during tests.
// # Mock rationale: We need to simulate reading configuration and item files without
// # actually touching the filesystem during tests to ensure determinism and speed.
// # This mock allows us to provide predefined JSON content for `mock-items.json`
// # and `mock-config.json` paths.
jest.mock('fs', () => ({
  readFileSync: jest.fn((path: string, encoding: string) => {
    if (path.includes('mock-items.json')) {
      return JSON.stringify([
        { id: '1', name: 'Canned Beans', tags: ['food', 'survival'], basePriority: 70 },
        { id: '2', name: 'First Aid Kit', tags: ['medical', 'survival'], basePriority: 90 },
        { id: '3', name: 'Broken Radio', description: 'Needs repair, might get news', tags: ['communication'], basePriority: 30 },
        { id: '4', name: 'Shiny Rock', description: 'Looks pretty, no practical use', tags: ['trinket'], basePriority: 10 },
        { id: '5', name: 'Water Purifier', tags: ['water', 'survival'], basePriority: 95 },
        { id: '6', name: 'Old Map', description: 'Map of the local area, potentially outdated', tags: ['navigation'], basePriority: 60 }
      ]);
    }
    if (path.includes('mock-config.json')) {
      return JSON.stringify({
        factors: [
          { name: 'Survival Essential', weight: 20, keywords: ['survival', 'food', 'water', 'medical'], type: 'positive' },
          { name: 'Communication Need', weight: 15, keywords: ['radio', 'communication'], type: 'positive' },
          { name: 'Repair Required', weight: 10, keywords: ['broken', 'needs repair'], type: 'negative' },
          { name: 'Morale Boost', weight: 5, keywords: ['pretty', 'shiny', 'trinket'], type: 'positive' },
          { name: 'Outdated Info', weight: 8, keywords: ['old', 'outdated'], type: 'negative' }
        ],
        defaultBasePriority: 50
      });
    }
    throw new Error(`File not found: ${path}`);
  }),
}));

describe('Nightly Priority Scrambler', () => {
  let mockItems: Item[];
  let mockConfig: Config;

  beforeAll(() => {
    // Load mock data using the mocked readFileSync
    mockItems = loadJson<Item[]>('mock-items.json');
    mockConfig = loadJson<Config>('mock-config.json');
  });

  it('should correctly load items and config from mock files', () => {
    expect(mockItems).toHaveLength(6);
    expect(mockConfig.factors).toHaveLength(5);
    expect(mockConfig.defaultBasePriority).toBe(50);
  });

  it('should calculate score for "Canned Beans" correctly', () => {
    const item = mockItems.find(i => i.id === '1')!; // Canned Beans
    const result = calculateScore(item, mockConfig);
    // Base: 70
    // Survival Essential (food, survival): +20 (food) +20 (survival) = +40
    // Total: 70 + 40 = 110
    expect(result.item.name).toBe('Canned Beans');
    expect(result.score).toBe(110);
    expect(result.rationale).toEqual([
      'Base priority: 70',
      '+40.00 from "Survival Essential" (keywords: food, survival)'
    ]);
  });

  it('should calculate score for "First Aid Kit" correctly', () => {
    const item = mockItems.find(i => i.id === '2')!; // First Aid Kit
    const result = calculateScore(item, mockConfig);
    // Base: 90
    // Survival Essential (medical, survival): +20 (medical) +20 (survival) = +40
    // Total: 90 + 40 = 130
    expect(result.item.name).toBe('First Aid Kit');
    expect(result.score).toBe(130);
    expect(result.rationale).toEqual([
      'Base priority: 90',
      '+40.00 from "Survival Essential" (keywords: medical, survival)'
    ]);
  });

  it('should calculate score for "Broken Radio" correctly', () => {
    const item = mockItems.find(i => i.id === '3')!; // Broken Radio
    const result = calculateScore(item, mockConfig);
    // Base: 30
    // Communication Need (radio, communication): +15 (radio) +15 (communication) = +30
    // Repair Required (broken): -10 (broken) = -10
    // Total: 30 + 30 - 10 = 50
    expect(result.item.name).toBe('Broken Radio');
    expect(result.score).toBe(50);
    expect(result.rationale).toEqual([
      'Base priority: 30',
      '+30.00 from "Communication Need" (keywords: radio, communication)',
      '-10.00 from "Repair Required" (keywords: broken)'
    ]);
  });

  it('should calculate score for "Shiny Rock" correctly', () => {
    const item = mockItems.find(i => i.id === '4')!; // Shiny Rock
    const result = calculateScore(item, mockConfig);
    // Base: 10
    // Morale Boost (shiny, pretty, trinket): +5 (shiny) +5 (trinket) = +10
    // Total: 10 + 10 = 20
    expect(result.item.name).toBe('Shiny Rock');
    expect(result.score).toBe(20);
    expect(result.rationale).toEqual([
      'Base priority: 10',
      '+10.00 from "Morale Boost" (keywords: shiny, trinket)'
    ]);
  });

  it('should use defaultBasePriority if item has none', () => {
    const itemWithoutBasePriority: Item = { id: '7', name: 'Mystery Box', tags: ['unknown'] };
    const result = calculateScore(itemWithoutBasePriority, mockConfig);
    // Base: 50 (default)
    // No matching factors
    expect(result.score).toBe(50);
    expect(result.rationale).toEqual([
      'Base priority: 50'
    ]);
  });

  it('should handle items with multiple matching factors and keywords', () => {
    const item = mockItems.find(i => i.id === '5')!; // Water Purifier
    const result = calculateScore(item, mockConfig);
    // Base: 95
    // Survival Essential (water, survival): +20 (water) +20 (survival) = +40
    // Total: 95 + 40 = 135
    expect(result.item.name).toBe('Water Purifier');
    expect(result.score).toBe(135);
    expect(result.rationale).toEqual([
      'Base priority: 95',
      '+40.00 from "Survival Essential" (keywords: water, survival)'
    ]);
  });

  it('should handle items with negative factors', () => {
    const item = mockItems.find(i => i.id === '6')!; // Old Map
    const result = calculateScore(item, mockConfig);
    // Base: 60
    // Outdated Info (old): -8 (old) = -8
    // Total: 60 - 8 = 52
    expect(result.item.name).toBe('Old Map');
    expect(result.score).toBe(52);
    expect(result.rationale).toEqual([
      'Base priority: 60',
      '-8.00 from "Outdated Info" (keywords: old)'
    ]);
  });

  it('should sort prioritized items correctly by score (descending)', () => {
    const itemsToPrioritize = mockItems.map(item => calculateScore(item, mockConfig));
    itemsToPrioritize.sort((a, b) => b.score - a.score);

    // Expected order based on calculated scores:
    // Water Purifier (135)
    // First Aid Kit (130)
    // Canned Beans (110)
    // Old Map (52)
    // Broken Radio (50)
    // Shiny Rock (20)

    expect(itemsToPrioritize[0].item.name).toBe('Water Purifier');
    expect(itemsToPrioritize[1].item.name).toBe('First Aid Kit');
    expect(itemsToPrioritize[2].item.name).toBe('Canned Beans');
    expect(itemsToPrioritize[3].item.name).toBe('Old Map');
    expect(itemsToPrioritize[4].item.name).toBe('Broken Radio');
    expect(itemsToPrioritize[5].item.name).toBe('Shiny Rock');
  });
});
