// tests/sorter.test.ts

import { StashSorter, CategorizedStash, Item, Category } from '../src/sorter';

describe('StashSorter', () => {
  let sorter: StashSorter;

  beforeEach(() => {
    sorter = new StashSorter();
  });

  it('should categorize items correctly based on keywords', () => {
    const items = [
      'half-eaten granola bar',
      'rusty wrench',
      'shiny bottle cap',
      'glowing mushroom',
      'tattered blanket',
      'unlabeled vial',
      'duct tape',
      'ancient scroll',
      'a random rock', // Should go to Shiny Baubles due to 'rock' keyword
      'chewy jerky', // Should go to Crunchy Sustenance
      'fancy hat', // Should go to Textiles
      'mysterious orb', // Should go to Mysterious Gadgets
      'a plain stick', // Should be uncategorized
    ];

    const categorized = sorter.categorizeAndPrioritize(items);

    expect(categorized['Crunchy Sustenance']).toBeDefined();
    expect(categorized['Crunchy Sustenance'].some(item => item.name === 'half-eaten granola bar')).toBe(true);
    expect(categorized['Crunchy Sustenance'].some(item => item.name === 'chewy jerky')).toBe(true);

    expect(categorized['Essential Oddities']).toBeDefined();
    expect(categorized['Essential Oddities'].some(item => item.name === 'rusty wrench')).toBe(true);
    expect(categorized['Essential Oddities'].some(item => item.name === 'duct tape')).toBe(true);

    expect(categorized['Shiny Baubles']).toBeDefined();
    expect(categorized['Shiny Baubles'].some(item => item.name === 'shiny bottle cap')).toBe(true);
    expect(categorized['Shiny Baubles'].some(item => item.name === 'a random rock')).toBe(true);

    expect(categorized['Mysterious Gadgets']).toBeDefined();
    expect(categorized['Mysterious Gadgets'].some(item => item.name === 'glowing mushroom')).toBe(true);
    expect(categorized['Mysterious Gadgets'].some(item => item.name === 'unlabeled vial')).toBe(true);
    expect(categorized['Mysterious Gadgets'].some(item => item.name === 'ancient scroll')).toBe(true);
    expect(categorized['Mysterious Gadgets'].some(item => item.name === 'mysterious orb')).toBe(true);

    expect(categorized['Textiles']).toBeDefined();
    expect(categorized['Textiles'].some(item => item.name === 'tattered blanket')).toBe(true);
    expect(categorized['Textiles'].some(item => item.name === 'fancy hat')).toBe(true);

    expect(categorized['Uncategorized Oddities']).toBeDefined();
    expect(categorized['Uncategorized Oddities'].some(item => item.name === 'a plain stick')).toBe(true);
  });

  it('should prioritize items within categories based on their primary attribute', () => {
    const items = [
      'very crunchy granola bar', // High crunchiness
      'slightly stale cookie',    // Medium crunchiness
      'soft bread',               // Low crunchiness
      'super shiny gem',          // High sparkle
      'dull rock',                // Low sparkle
      'dangerous glowing orb',    // High danger
      'mildly mysterious note',   // Medium danger
    ];

    const categorized = sorter.categorizeAndPrioritize(items);

    // Test Crunchy Sustenance prioritization (by crunchiness)
    const crunchyItems = categorized['Crunchy Sustenance'];
    expect(crunchyItems.length).toBe(3);
    expect(crunchyItems[0].name).toBe('very crunchy granola bar'); // # Mock rationale: Attributes are deterministically generated based on keywords/length.
    expect(crunchyItems[1].name).toBe('slightly stale cookie');
    expect(crunchyItems[2].name).toBe('soft bread');

    // Test Shiny Baubles prioritization (by sparkle)
    const shinyItems = categorized['Shiny Baubles'];
    expect(shinyItems.length).toBe(2);
    expect(shinyItems[0].name).toBe('super shiny gem'); // # Mock rationale: Attributes are deterministically generated based on keywords/length.
    expect(shinyItems[1].name).toBe('dull rock');

    // Test Mysterious Gadgets prioritization (by danger)
    const mysteriousItems = categorized['Mysterious Gadgets'];
    expect(mysteriousItems.length).toBe(2);
    expect(mysteriousItems[0].name).toBe('dangerous glowing orb'); // # Mock rationale: Attributes are deterministically generated based on keywords/length.
    expect(mysteriousItems[1].name).toBe('mildly mysterious note');
  });

  it('should handle empty input gracefully', () => {
    const categorized = sorter.categorizeAndPrioritize([]);
    expect(Object.keys(categorized).every(cat => categorized[cat].length === 0)).toBe(true);
  });

  it('should assign attributes deterministically', () => {
    const item1 = 'shiny rock';
    const item2 = 'shiny rock';
    const item3 = 'dull rock';

    const attributes1 = (sorter as any).generateWhimsicalAttributes(item1); // Access private for testing
    const attributes2 = (sorter as any).generateWhimsicalAttributes(item2);
    const attributes3 = (sorter as any).generateWhimsicalAttributes(item3);

    expect(attributes1).toEqual(attributes2);
    expect(attributes1).not.toEqual(attributes3);
    expect(attributes1.sparkle).toBeGreaterThan(attributes3.sparkle); // 'shiny' vs 'dull'
  });

  it('should sort uncategorized items by whimsy', () => {
    const items = [
      'a very whimsical item indeed', // Longer, potentially higher whimsy
      'a short item',                 // Shorter, potentially lower whimsy
      'another whimsical thing',
    ];

    const categorized = sorter.categorizeAndPrioritize(items);
    const uncategorized = categorized['Uncategorized Oddities'];
    expect(uncategorized).toBeDefined();
    expect(uncategorized.length).toBe(3);

    // # Mock rationale: Whimsy attribute is deterministically generated based on item name length.
    // Longer names tend to have higher whimsy in this mock implementation.
    // The exact order depends on the specific `generateWhimsicalAttributes` logic.
    // We'll check that the sorting is consistent with the mock logic.
    const item1Whimsy = (sorter as any).generateWhimsicalAttributes('a very whimsical item indeed').whimsy;
    const item2Whimsy = (sorter as any).generateWhimsicalAttributes('a short item').whimsy;
    const item3Whimsy = (sorter as any).generateWhimsicalAttributes('another whimsical thing').whimsy;

    // Sort expected items based on their generated whimsy
    const expectedOrder = [
      { name: 'a very whimsical item indeed', whimsy: item1Whimsy },
      { name: 'another whimsical thing', whimsy: item3Whimsy },
      { name: 'a short item', whimsy: item2Whimsy },
    ].sort((a, b) => b.whimsy - a.whimsy);

    expect(uncategorized[0].name).toBe(expectedOrder[0].name);
    expect(uncategorized[1].name).toBe(expectedOrder[1].name);
    expect(uncategorized[2].name).toBe(expectedOrder[2].name);
  });
});
