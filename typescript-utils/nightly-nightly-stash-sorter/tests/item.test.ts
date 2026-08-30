import { ScavengedItem, SurvivalPriority, sortAndFilterItems, ItemCondition } from '../src/item';

describe('sortAndFilterItems', () => {
  const mockItems: ScavengedItem[] = [
    { id: '1', name: 'Canned Beans', category: 'food', rarity: 'common', condition: 'good', weight_kg: 0.5, value_units: 10, perishable: false },
    { id: '2', name: 'Rusty Axe', category: 'weapon', rarity: 'uncommon', condition: 'damaged', weight_kg: 2.0, value_units: 25, perishable: false },
    { id: '3', name: 'Water Bottle', category: 'water', rarity: 'common', condition: 'pristine', weight_kg: 1.0, value_units: 15, perishable: true },
    { id: '4', name: 'First Aid Kit', category: 'medical', rarity: 'rare', condition: 'good', weight_kg: 0.8, value_units: 40, perishable: false },
    { id: '5', name: 'Broken Radio', category: 'misc', rarity: 'uncommon', condition: 'broken', weight_kg: 1.2, value_units: 5, perishable: false },
    { id: '6', name: 'Pistol', category: 'weapon', rarity: 'rare', condition: 'worn', weight_kg: 1.5, value_units: 50, perishable: false },
    { id: '7', name: 'MRE', category: 'food', rarity: 'uncommon', condition: 'pristine', weight_kg: 0.7, value_units: 20, perishable: true }
  ];

  // Mock rationale: Using a static array of ScavengedItem objects allows for deterministic testing
  // without relying on file I/O or external data sources. This ensures tests are fast,
  // isolated, and predictable.

  it('should return all items if no priority is given', () => {
    const result = sortAndFilterItems(mockItems, {});
    expect(result).toEqual(mockItems);
  });

  it('should filter by a single category', () => {
    const priority: SurvivalPriority = { filterCategory: ['food'] };
    const result = sortAndFilterItems(mockItems, priority);
    expect(result.length).toBe(2);
    expect(result.every(item => item.category === 'food')).toBe(true);
  });

  it('should filter by multiple categories', () => {
    const priority: SurvivalPriority = { filterCategory: ['food', 'weapon'] };
    const result = sortAndFilterItems(mockItems, priority);
    expect(result.length).toBe(4);
    expect(result.every(item => item.category === 'food' || item.category === 'weapon')).toBe(true);
  });

  it('should filter by a single rarity', () => {
    const priority: SurvivalPriority = { filterRarity: ['rare'] };
    const result = sortAndFilterItems(mockItems, priority);
    expect(result.length).toBe(2);
    expect(result.every(item => item.rarity === 'rare')).toBe(true);
  });

  it('should filter by minimum condition', () => {
    const priority: SurvivalPriority = { filterConditionMin: 'good' };
    const result = sortAndFilterItems(mockItems, priority);
    expect(result.length).toBe(4); // Canned Beans (good), Water Bottle (pristine), First Aid Kit (good), MRE (pristine)
    expect(result.some(item => item.id === '2')).toBe(false); // Rusty Axe (damaged)
    expect(result.some(item => item.id === '5')).toBe(false); // Broken Radio (broken)
    expect(result.some(item => item.id === '6')).toBe(false); // Pistol (worn)
  });

  it('should sort by value_units in descending order', () => {
    const priority: SurvivalPriority = { sortBy: 'value_units', sortOrder: 'desc' };
    const result = sortAndFilterItems(mockItems, priority);
    expect(result[0].name).toBe('Pistol'); // 50
    expect(result[1].name).toBe('First Aid Kit'); // 40
    expect(result[result.length - 1].name).toBe('Broken Radio'); // 5
  });

  it('should sort by name in ascending order', () => {
    const priority: SurvivalPriority = { sortBy: 'name', sortOrder: 'asc' };
    const result = sortAndFilterItems(mockItems, priority);
    expect(result[0].name).toBe('Broken Radio');
    expect(result[result.length - 1].name).toBe('Water Bottle');
  });

  it('should sort by condition in ascending order', () => {
    const priority: SurvivalPriority = { sortBy: 'condition', sortOrder: 'asc' };
    const result = sortAndFilterItems(mockItems, priority);
    const expectedOrder: ItemCondition[] = ['broken', 'damaged', 'worn', 'good', 'good', 'pristine', 'pristine'];
    expect(result.map(item => item.condition)).toEqual(expectedOrder);
  });

  it('should sort by condition in descending order', () => {
    const priority: SurvivalPriority = { sortBy: 'condition', sortOrder: 'desc' };
    const result = sortAndFilterItems(mockItems, priority);
    const expectedOrder: ItemCondition[] = ['pristine', 'pristine', 'good', 'good', 'worn', 'damaged', 'broken'];
    expect(result.map(item => item.condition)).toEqual(expectedOrder);
  });

  it('should limit the number of results', () => {
    const priority: SurvivalPriority = { limit: 3 };
    const result = sortAndFilterItems(mockItems, priority);
    expect(result.length).toBe(3);
  });

  it('should combine filtering and sorting', () => {
    const priority: SurvivalPriority = {
      filterCategory: ['food', 'medical'],
      filterConditionMin: 'good',
      sortBy: 'value_units',
      sortOrder: 'desc',
      limit: 2
    };
    const result = sortAndFilterItems(mockItems, priority);
    expect(result.length).toBe(2);
    expect(result[0].name).toBe('First Aid Kit'); // medical, good, 40
    expect(result[1].name).toBe('MRE'); // food, pristine, 20
  });

  it('should handle empty item list gracefully', () => {
    const priority: SurvivalPriority = { sortBy: 'name' };
    const result = sortAndFilterItems([], priority);
    expect(result).toEqual([]);
  });

  it('should handle filters that result in no items', () => {
    const priority: SurvivalPriority = { filterRarity: ['legendary'] };
    const result = sortAndFilterItems(mockItems, priority);
    expect(result).toEqual([]);
  });
});
