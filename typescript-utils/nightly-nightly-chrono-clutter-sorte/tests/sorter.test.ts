import { ChronoClutterSorter, ChronoConfig, Category, Rule, SortedResult } from '../src/sorter';

describe('ChronoClutterSorter', () => {
  const mockCategories: Category[] = [
    { id: 'urgent-void', name: 'Urgent Void', description: 'Critical', priority: 1 },
    { id: 'temporal-drift', name: 'Temporal Drift', description: 'Important', priority: 2 },
    { id: 'future-echo', name: 'Future Echo', description: 'Long-term', priority: 3 },
    { id: 'forgotten-relic', name: 'Forgotten Relic', description: 'Archive', priority: 4 }
  ];

  const mockRules: Rule[] = [
    { keyword: 'urgent', targetCategoryId: 'urgent-void' },
    { keyword: 'critical', targetCategoryId: 'urgent-void' },
    { keyword: 'review', targetCategoryId: 'temporal-drift' },
    { keyword: 'plan', targetCategoryId: 'future-echo' },
    { keyword: 'archive', targetCategoryId: 'forgotten-relic' }
  ];

  const defaultCategoryId = 'temporal-drift';

  const mockConfig: ChronoConfig = {
    categories: mockCategories,
    rules: mockRules,
    defaultCategoryId: defaultCategoryId
  };

  it('should initialize with valid configuration', () => {
    const sorter = new ChronoClutterSorter(mockConfig);
    expect(sorter).toBeInstanceOf(ChronoClutterSorter);
    expect(sorter.getCategoryById('urgent-void')).toEqual(mockCategories[0]);
  });

  it('should throw error if no categories are provided', () => {
    const invalidConfig = { ...mockConfig, categories: [] };
    expect(() => new ChronoClutterSorter(invalidConfig)).toThrow('Configuration must contain at least one category.');
  });

  it('should throw error if defaultCategoryId is missing', () => {
    const invalidConfig = { ...mockConfig, defaultCategoryId: '' };
    expect(() => new ChronoClutterSorter(invalidConfig)).toThrow('Configuration must specify a defaultCategoryId.');
  });

  it('should throw error if defaultCategoryId does not exist', () => {
    const invalidConfig = { ...mockConfig, defaultCategoryId: 'non-existent' };
    expect(() => new ChronoClutterSorter(invalidConfig)).toThrow("Default category with ID 'non-existent' not found.");
  });

  it('should sort items correctly based on keywords (case-insensitive)', () => {
    const sorter = new ChronoClutterSorter(mockConfig);
    const items = [
      'Fix urgent bug',           // urgent-void
      'Review code changes',      // temporal-drift
      'Plan next feature',        // future-echo
      'Archive old documents',    // forgotten-relic
      'Critical system alert',    // urgent-void
      'Just a random note'        // default: temporal-drift
    ];

    const expected: SortedResult = {
      'urgent-void': ['Fix urgent bug', 'Critical system alert'],
      'temporal-drift': ['Review code changes', 'Just a random note'],
      'future-echo': ['Plan next feature'],
      'forgotten-relic': ['Archive old documents']
    };

    const result = sorter.sort(items);
    expect(result['urgent-void']).toEqual(expect.arrayContaining(expected['urgent-void']));
    expect(result['temporal-drift']).toEqual(expect.arrayContaining(expected['temporal-drift']));
    expect(result['future-echo']).toEqual(expect.arrayContaining(expected['future-echo']));
    expect(result['forgotten-relic']).toEqual(expect.arrayContaining(expected['forgotten-relic']));
    // Ensure no other categories have items if they shouldn't
    expect(result['urgent-void'].length).toBe(expected['urgent-void'].length);
    expect(result['temporal-drift'].length).toBe(expected['temporal-drift'].length);
    expect(result['future-echo'].length).toBe(expected['future-echo'].length);
    expect(result['forgotten-relic'].length).toBe(expected['forgotten-relic'].length);
  });

  it('should assign items to the default category if no rules match', () => {
    const sorter = new ChronoClutterSorter(mockConfig);
    const items = [
      'A completely unrelated item',
      'Another item with no keywords'
    ];

    const result = sorter.sort(items);
    expect(result[defaultCategoryId]).toEqual(expect.arrayContaining(items));
    expect(result[defaultCategoryId].length).toBe(items.length);
    expect(result['urgent-void'].length).toBe(0);
  });

  it('should handle empty item list', () => {
    const sorter = new ChronoClutterSorter(mockConfig);
    const items: string[] = [];
    const result = sorter.sort(items);
    expect(result['urgent-void']).toEqual([]);
    expect(result['temporal-drift']).toEqual([]);
    expect(result['future-echo']).toEqual([]);
    expect(result['forgotten-relic']).toEqual([]);
  });

  it('should handle rules with unknown target categories gracefully (warn and use default)', () => {
    const configWithBadRule: ChronoConfig = {
      ...mockConfig,
      rules: [...mockRules, { keyword: 'unknown', targetCategoryId: 'non-existent-category' }]
    };
    const sorter = new ChronoClutterSorter(configWithBadRule);
    const consoleWarnSpy = jest.spyOn(console, 'warn').mockImplementation(() => {}); // Mock rationale: Suppress console.warn output during test to keep test output clean.

    const items = ['Item with unknown keyword'];
    const result = sorter.sort(items);

    expect(consoleWarnSpy).toHaveBeenCalledWith(
      "Warning: Rule for keyword 'unknown' targets unknown category ID 'non-existent-category'. Item 'Item with unknown keyword' will be sorted to default."
    );
    expect(result[defaultCategoryId]).toEqual(['Item with unknown keyword']);
    consoleWarnSpy.mockRestore(); // Restore console.warn
  });

  it('should return categories sorted by priority', () => {
    const sorter = new ChronoClutterSorter(mockConfig);
    const categories = sorter.getAllCategories();
    expect(categories.map(c => c.id)).toEqual(['urgent-void', 'temporal-drift', 'future-echo', 'forgotten-relic']);
  });
});

// Mock rationale: The tests for sorter.ts are pure unit tests and do not require file system access.
// The main CLI (index.ts) handles file system operations, which would be mocked if tested directly.
// For this utility, testing the core sorting logic in isolation is sufficient and deterministic.
