import { suggestOutfit } from '../src/index';
import { ClothingItem, Mood, ClothingCategory, Color, StyleTag, WarmthLevel } from '../src/types';

describe('suggestOutfit', () => {
  const mockWardrobe: ClothingItem[] = [
    { id: 't1', name: 'Casual Tee', category: 'top', color: 'blue', styleTags: ['casual'], warmth: 'mild', available: true },
    { id: 't2', name: 'Formal Shirt', category: 'top', color: 'white', styleTags: ['formal'], warmth: 'mild', available: true },
    { id: 't3', name: 'Warm Sweater', category: 'top', color: 'grey', styleTags: ['cozy'], warmth: 'cold', available: true },
    { id: 'b1', name: 'Denim Jeans', category: 'bottom', color: 'blue', styleTags: ['casual'], warmth: 'mild', available: true },
    { id: 'b2', name: 'Dress Pants', category: 'bottom', color: 'black', styleTags: ['formal'], warmth: 'mild', available: true },
    { id: 'b3', name: 'Sweatpants', category: 'bottom', color: 'grey', styleTags: ['cozy'], warmth: 'cold', available: true },
    { id: 'f1', name: 'Sneakers', category: 'footwear', color: 'white', styleTags: ['casual'], warmth: 'mild', available: true },
    { id: 'f2', name: 'Dress Shoes', category: 'footwear', color: 'black', styleTags: ['formal'], warmth: 'mild', available: true },
    { id: 'f3', name: 'Boots', category: 'footwear', color: 'brown', styleTags: ['cozy'], warmth: 'cold', available: true },
    { id: 'o1', name: 'Light Jacket', category: 'outerwear', color: 'green', styleTags: ['casual'], warmth: 'cool', available: true },
    { id: 'a1', name: 'Scarf', category: 'accessory', color: 'red', styleTags: ['cozy'], warmth: 'cold', available: true },
    { id: 'a2', name: 'Tie', category: 'accessory', color: 'blue', styleTags: ['formal'], warmth: 'mild', available: true },
    { id: 't4', name: 'Unavailable Top', category: 'top', color: 'red', styleTags: ['casual'], warmth: 'mild', available: false } // Unavailable item
  ]; // Mock rationale: Provides a controlled, deterministic set of clothing items for testing outfit suggestions.

  it('should suggest a "Cozy Evening" outfit', () => {
    const cozyMood: Mood = {
      name: 'Cozy Evening',
      preferredColors: ['grey', 'blue'],
      preferredStyleTags: ['cozy', 'casual'],
      warmthPreference: 'cold',
      requiredCategories: ['top', 'bottom', 'footwear'],
      optionalCategories: ['outerwear', 'accessory'],
    };

    const suggestion = suggestOutfit(cozyMood, mockWardrobe);

    expect(suggestion).not.toBeNull();
    expect(suggestion?.mood.name).toBe('Cozy Evening');
    expect(suggestion?.items.length).toBeGreaterThanOrEqual(3); // At least required categories
    expect(suggestion?.items.some(item => item.name === 'Warm Sweater')).toBe(true);
    expect(suggestion?.items.some(item => item.name === 'Sweatpants')).toBe(true);
    expect(suggestion?.items.some(item => item.name === 'Boots')).toBe(true);
    expect(suggestion?.score).toBeGreaterThan(0);
  });

  it('should suggest a "Formal Business" outfit', () => {
    const formalMood: Mood = {
      name: 'Formal Business',
      preferredColors: ['black', 'white'],
      preferredStyleTags: ['formal'],
      warmthPreference: 'mild',
      requiredCategories: ['top', 'bottom', 'footwear'],
      optionalCategories: ['accessory'],
    };

    const suggestion = suggestOutfit(formalMood, mockWardrobe);

    expect(suggestion).not.toBeNull();
    expect(suggestion?.mood.name).toBe('Formal Business');
    expect(suggestion?.items.length).toBeGreaterThanOrEqual(3);
    expect(suggestion?.items.some(item => item.name === 'Formal Shirt')).toBe(true);
    expect(suggestion?.items.some(item => item.name === 'Dress Pants')).toBe(true);
    expect(suggestion?.items.some(item => item.name === 'Dress Shoes')).toBe(true);
    expect(suggestion?.score).toBeGreaterThan(0);
  });

  it('should return null if a required category cannot be fulfilled', () => {
    const impossibleMood: Mood = {
      name: 'Impossible',
      preferredColors: ['purple'], // No purple items
      preferredStyleTags: ['edgy'],
      warmthPreference: 'hot',
      requiredCategories: ['top', 'bottom', 'footwear'],
      optionalCategories: [],
    };

    const suggestion = suggestOutfit(impossibleMood, mockWardrobe);
    expect(suggestion).toBeNull();
  });

  it('should not include unavailable items', () => {
    const casualMood: Mood = {
      name: 'Casual Day',
      preferredColors: ['red', 'blue'],
      preferredStyleTags: ['casual'],
      warmthPreference: 'mild',
      requiredCategories: ['top', 'bottom', 'footwear'],
      optionalCategories: [],
    };

    const suggestion = suggestOutfit(casualMood, mockWardrobe);
    expect(suggestion).not.toBeNull();
    expect(suggestion?.items.some(item => item.name === 'Unavailable Top')).toBe(false);
  });

  it('should prioritize items matching warmth preference', () => {
    const hotWeatherMood: Mood = {
      name: 'Hot Day',
      preferredColors: ['white'],
      preferredStyleTags: ['casual'],
      warmthPreference: 'hot',
      requiredCategories: ['top'],
      optionalCategories: [],
    };
    const hotWardrobe: ClothingItem[] = [
      { id: 't1', name: 'Tank Top', category: 'top', color: 'white', styleTags: ['casual'], warmth: 'hot', available: true },
      { id: 't2', name: 'T-Shirt', category: 'top', color: 'white', styleTags: ['casual'], warmth: 'mild', available: true },
    ]; // Mock rationale: Provides specific items to test warmth preference logic.

    const suggestion = suggestOutfit(hotWeatherMood, hotWardrobe);
    expect(suggestion).not.toBeNull();
    expect(suggestion?.items.some(item => item.name === 'Tank Top')).toBe(true);
    expect(suggestion?.items.some(item => item.name === 'T-Shirt')).toBe(false);
  });

  it('should include optional categories if they fit the mood', () => {
    const cozyMoodWithOptional: Mood = {
      name: 'Cozy Evening',
      preferredColors: ['grey', 'blue'],
      preferredStyleTags: ['cozy', 'casual'],
      warmthPreference: 'cold',
      requiredCategories: ['top', 'bottom', 'footwear'],
      optionalCategories: ['accessory'],
    };

    const suggestion = suggestOutfit(cozyMoodWithOptional, mockWardrobe);
    expect(suggestion).not.toBeNull();
    expect(suggestion?.items.some(item => item.name === 'Scarf')).toBe(true); // Scarf is an accessory that fits 'cozy' and 'cold'
  });

  it('should return null if wardrobe is empty', () => {
    const mood: Mood = {
      name: 'Any Mood',
      preferredColors: ['blue'],
      preferredStyleTags: ['casual'],
      warmthPreference: 'mild',
      requiredCategories: ['top'],
      optionalCategories: [],
    };
    const emptyWardrobe: ClothingItem[] = []; // Mock rationale: Tests edge case of an empty wardrobe.
    const suggestion = suggestOutfit(mood, emptyWardrobe);
    expect(suggestion).toBeNull();
  });

  it('should handle moods with no preferred colors or styles gracefully', () => {
    const neutralMood: Mood = {
      name: 'Neutral Day',
      preferredColors: [],
      preferredStyleTags: [],
      warmthPreference: 'mild',
      requiredCategories: ['top', 'bottom'],
      optionalCategories: [],
    };
    const suggestion = suggestOutfit(neutralMood, mockWardrobe);
    expect(suggestion).not.toBeNull();
    expect(suggestion?.items.length).toBeGreaterThanOrEqual(2);
  });
});
