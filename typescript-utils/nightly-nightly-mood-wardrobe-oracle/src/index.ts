import { ClothingItem, Mood, OutfitSuggestion, ClothingCategory, Color, StyleTag, WarmthLevel } from './types';

// Sample data (can be loaded from a file or passed in CLI)
const sampleWardrobe: ClothingItem[] = [
  { id: 't1', name: 'Blue T-Shirt', category: 'top', color: 'blue', styleTags: ['casual'], warmth: 'mild', available: true },
  { id: 't2', name: 'White Blouse', category: 'top', color: 'white', styleTags: ['formal', 'minimalist'], warmth: 'mild', available: true },
  { id: 'b1', name: 'Denim Jeans', category: 'bottom', color: 'blue', styleTags: ['casual'], warmth: 'mild', available: true },
  { id: 'b2', name: 'Black Skirt', category: 'bottom', color: 'black', styleTags: ['formal', 'minimalist'], warmth: 'mild', available: true },
  { id: 'o1', name: 'Leather Jacket', category: 'outerwear', color: 'black', styleTags: ['edgy', 'casual'], warmth: 'cool', available: true },
  { id: 'o2', name: 'Wool Cardigan', category: 'outerwear', color: 'grey', styleTags: ['cozy', 'casual'], warmth: 'cold', available: true },
  { id: 'f1', name: 'Sneakers', category: 'footwear', color: 'white', styleTags: ['sporty', 'casual'], warmth: 'mild', available: true },
  { id: 'f2', name: 'Boots', category: 'footwear', color: 'brown', styleTags: ['edgy', 'casual'], warmth: 'cool', available: true },
  { id: 'a1', name: 'Scarf', category: 'accessory', color: 'red', styleTags: ['cozy'], warmth: 'cold', available: true },
  { id: 'a2', name: 'Silver Necklace', category: 'accessory', color: 'grey', styleTags: ['minimalist', 'formal'], warmth: 'mild', available: true },
  { id: 't3', name: 'Red Hoodie', category: 'top', color: 'red', styleTags: ['casual', 'sporty', 'cozy'], warmth: 'cool', available: true },
  { id: 'b3', name: 'Sweatpants', category: 'bottom', color: 'grey', styleTags: ['casual', 'sporty', 'cozy'], warmth: 'mild', available: true },
  { id: 'f3', name: 'Sandals', category: 'footwear', color: 'brown', styleTags: ['casual'], warmth: 'hot', available: true },
  { id: 'o3', name: 'Light Raincoat', category: 'outerwear', color: 'yellow', styleTags: ['casual', 'sporty'], warmth: 'mild', available: true }
];

const sampleMoods: Mood[] = [
  {
    name: 'Cozy Evening',
    preferredColors: ['grey', 'blue', 'brown'],
    preferredStyleTags: ['cozy', 'casual'],
    warmthPreference: 'cold',
    requiredCategories: ['top', 'bottom', 'footwear'],
    optionalCategories: ['outerwear', 'accessory'],
  },
  {
    name: 'Formal Business',
    preferredColors: ['black', 'white', 'grey'],
    preferredStyleTags: ['formal', 'minimalist'],
    warmthPreference: 'mild',
    requiredCategories: ['top', 'bottom', 'footwear'],
    optionalCategories: ['accessory'],
  },
  {
    name: 'Adventurous Explorer',
    preferredColors: ['green', 'brown', 'blue', 'yellow'],
    preferredStyleTags: ['sporty', 'casual'],
    warmthPreference: 'mild',
    requiredCategories: ['top', 'bottom', 'footwear'],
    optionalCategories: ['outerwear', 'accessory'],
  },
  {
    name: 'Edgy Rebel',
    preferredColors: ['black', 'red'],
    preferredStyleTags: ['edgy', 'casual'],
    warmthPreference: 'cool',
    requiredCategories: ['top', 'bottom', 'footwear'],
    optionalCategories: ['outerwear', 'accessory'],
  },
];

export function suggestOutfit(mood: Mood, wardrobe: ClothingItem[]): OutfitSuggestion | null {
  const availableItems = wardrobe.filter(item => item.available);
  const outfit: ClothingItem[] = [];
  let score = 0;

  const selectedCategories = new Set<ClothingCategory>();

  // Prioritize required categories
  for (const category of mood.requiredCategories) {
    const candidates = availableItems.filter(item =>
      item.category === category &&
      item.warmth === mood.warmthPreference &&
      mood.preferredColors.includes(item.color) &&
      item.styleTags.some(tag => mood.preferredStyleTags.includes(tag))
    );

    if (candidates.length > 0) {
      // Simple selection: pick the first matching item
      outfit.push(candidates[0]);
      selectedCategories.add(category);
      score += 10; // Base score for fulfilling a required category
    } else {
      // Fallback: try to find any item for the required category, even if it doesn't perfectly match color/style/warmth
      const fallbackCandidates = availableItems.filter(item => item.category === category);
      if (fallbackCandidates.length > 0) {
        outfit.push(fallbackCandidates[0]);
        selectedCategories.add(category);
        score += 5; // Lower score for fallback
      } else {
        return null; // Cannot fulfill a required category at all
      }
    }
  }

  // Add optional categories if available and fitting
  for (const category of mood.optionalCategories) {
    if (!selectedCategories.has(category)) { // Only add if not already added as required
      const candidates = availableItems.filter(item =>
        item.category === category &&
        item.warmth === mood.warmthPreference &&
        mood.preferredColors.includes(item.color) &&
        item.styleTags.some(tag => mood.preferredStyleTags.includes(tag))
      );
      if (candidates.length > 0) {
        outfit.push(candidates[0]);
        score += 3; // Score for optional category
      }
    }
  }

  // Refine score based on overall match
  const outfitColors = new Set(outfit.map(item => item.color));
  const outfitStyleTags = new Set(outfit.flatMap(item => item.styleTags));

  mood.preferredColors.forEach(color => {
    if (outfitColors.has(color)) score += 1;
  });
  mood.preferredStyleTags.forEach(tag => {
    if (outfitStyleTags.has(tag)) score += 1;
  });

  if (outfit.length === 0) return null;

  return {
    mood,
    items: outfit,
    score,
    message: `A ${mood.name} outfit has been conjured!`, 
  };
}

// CLI entry point
if (require.main === module) {
  const moodName = process.argv[2];
  if (!moodName) {
    console.log('Usage: ts-node src/index.ts <mood_name>');
    console.log('Available moods:', sampleMoods.map(m => m.name).join(', '));
    process.exit(1);
  }

  const selectedMood = sampleMoods.find(m => m.name.toLowerCase() === moodName.toLowerCase());

  if (!selectedMood) {
    console.log(`Mood "${moodName}" not found. Available moods:`, sampleMoods.map(m => m.name).join(', '));
    process.exit(1);
  }

  const suggestion = suggestOutfit(selectedMood, sampleWardrobe);

  if (suggestion) {
    console.log(`\n✨ ${suggestion.message} (Score: ${suggestion.score}) ✨`);
    console.log(`For a "${suggestion.mood.name}" vibe, try these items:`);
    suggestion.items.forEach(item => {
      console.log(`- ${item.name} (${item.color}, ${item.category}, ${item.styleTags.join(', ')})`);
    });
  } else {
    console.log(`Alas, no suitable outfit could be found for the "${selectedMood.name}" mood with your current wardrobe.`);
  }
}
