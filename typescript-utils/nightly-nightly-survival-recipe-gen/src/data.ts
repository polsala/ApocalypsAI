import { Ingredient, Recipe } from './types';

export const allIngredients: Ingredient[] = [
  { name: 'Mutant Mushroom', category: 'vegetable', isEdibleRaw: false },
  { name: 'Glow-in-the-dark Berry', category: 'fruit', isEdibleRaw: true },
  { name: 'Canned Mystery Meat', category: 'protein', isEdibleRaw: true },
  { name: 'Dusty Water', category: 'liquid', isEdibleRaw: true },
  { name: 'Scavenged Spice Mix', category: 'spice', isEdibleRaw: true },
  { name: 'Ration Bar Crumbs', category: 'grain', isEdibleRaw: true },
  { name: 'Fungus Forage', category: 'vegetable', isEdibleRaw: false },
  { name: 'Wasteland Worms', category: 'protein', isEdibleRaw: false },
  { name: 'Irradiated Potato', category: 'vegetable', isEdibleRaw: false },
  { name: 'Pre-war Pasta', category: 'grain', isEdibleRaw: true },
  { name: 'Salt Lick', category: 'spice', isEdibleRaw: true },
  { name: 'Sun-bleached Greens', category: 'vegetable', isEdibleRaw: true },
  { name: 'Desiccated Fruit', category: 'fruit', isEdibleRaw: true },
  { name: 'Cactus Nectar', category: 'liquid', isEdibleRaw: true }
];

export const allRecipes: Recipe[] = [
  {
    name: 'Glowing Mushroom Stew',
    description: 'A hearty, slightly radioactive stew to warm your core.',
    requiredIngredients: [
      { ingredientName: 'Mutant Mushroom', quantity: 3 },
      { ingredientName: 'Dusty Water', quantity: 1 },
      { ingredientName: 'Scavenged Spice Mix', quantity: 1 },
      { ingredientName: 'Canned Mystery Meat', quantity: 1 }
    ],
    instructions: [
      'Chop Mutant Mushrooms (carefully!).',
      'Boil Dusty Water in a scavenged pot.',
      'Add chopped mushrooms, mystery meat, and spice mix.',
      'Simmer until mushrooms are tender and glowing softly.',
      'Serve hot, but don\'t stare too long at the glow.'
    ],
    servings: 2,
    difficulty: 'medium'
  },
  {
    name: 'Berry & Ration Crumble',
    description: 'A sweet treat for those rare moments of joy.',
    requiredIngredients: [
      { ingredientName: 'Glow-in-the-dark Berry', quantity: 5 },
      { ingredientName: 'Ration Bar Crumbs', quantity: 1 },
      { ingredientName: 'Scavenged Spice Mix', quantity: 0.5 } // Optional quantity, just for flavor
    ],
    instructions: [
      'Mash Glow-in-the-dark Berries in a bowl.',
      'Mix in Ration Bar Crumbs and a pinch of Scavenged Spice Mix.',
      'Form into small patties and bake over a low fire until slightly crispy (if fire available).',
      'Enjoy raw if no fire is present.'
    ],
    servings: 1,
    difficulty: 'easy'
  },
  {
    name: 'Wasteland Worm & Potato Hash',
    description: 'A protein-packed meal for the truly desperate, or adventurous.',
    requiredIngredients: [
      { ingredientName: 'Wasteland Worms', quantity: 10 },
      { ingredientName: 'Irradiated Potato', quantity: 2 },
      { ingredientName: 'Salt Lick', quantity: 1 }
    ],
    instructions: [
      'Clean Wasteland Worms thoroughly (don\'t ask how).',
      'Peel and dice Irradiated Potatoes.',
      'Fry worms and potatoes in a pan over medium heat until cooked through.',
      'Season with crushed Salt Lick to taste.',
      'Try not to think about what you\'re eating.'
    ],
    servings: 2,
    difficulty: 'hard'
  },
  {
    name: 'Cactus Nectar Refresher',
    description: 'A simple, hydrating drink to combat the desert heat.',
    requiredIngredients: [
      { ingredientName: 'Cactus Nectar', quantity: 1 },
      { ingredientName: 'Dusty Water', quantity: 1 }
    ],
    instructions: [
      'Mix Cactus Nectar with Dusty Water.',
      'Stir well until fully combined.',
      'Drink immediately to rehydrate. Best served lukewarm.'
    ],
    servings: 1,
    difficulty: 'easy'
  }
];
