import { findRecipes } from '../src/recipeGenerator';
import { allRecipes } from '../src/data';

describe('Recipe Generator', () => {
  it('should find no recipes if no ingredients are available', () => {
    const available: string[] = [];
    const found = findRecipes(available);
    expect(found).toEqual([]);
  });

  it('should find "Glowing Mushroom Stew" if all its ingredients are available', () => {
    const available = ['Mutant Mushroom', 'Dusty Water', 'Scavenged Spice Mix', 'Canned Mystery Meat'];
    const found = findRecipes(available);
    expect(found.length).toBeGreaterThan(0);
    expect(found.some(r => r.name === 'Glowing Mushroom Stew')).toBe(true);
  });

  it('should find "Berry & Ration Crumble" if its ingredients are available', () => {
    const available = ['Glow-in-the-dark Berry', 'Ration Bar Crumbs'];
    const found = findRecipes(available);
    expect(found.length).toBeGreaterThan(0);
    expect(found.some(r => r.name === 'Berry & Ration Crumble')).toBe(true);
  });

  it('should find "Wasteland Worm & Potato Hash" if its ingredients are available', () => {
    const available = ['Wasteland Worms', 'Irradiated Potato', 'Salt Lick'];
    const found = findRecipes(available);
    expect(found.length).toBeGreaterThan(0);
    expect(found.some(r => r.name === 'Wasteland Worm & Potato Hash')).toBe(true);
  });

  it('should find "Cactus Nectar Refresher" if its ingredients are available', () => {
    const available = ['Cactus Nectar', 'Dusty Water'];
    const found = findRecipes(available);
    expect(found.length).toBeGreaterThan(0);
    expect(found.some(r => r.name === 'Cactus Nectar Refresher')).toBe(true);
  });

  it('should find multiple recipes if ingredients for several are available', () => {
    const available = [
      'Mutant Mushroom', 'Dusty Water', 'Scavenged Spice Mix', 'Canned Mystery Meat',
      'Glow-in-the-dark Berry', 'Ration Bar Crumbs',
      'Wasteland Worms', 'Irradiated Potato', 'Salt Lick',
      'Cactus Nectar'
    ];
    const found = findRecipes(available);
    expect(found.length).toBeGreaterThanOrEqual(4);
    expect(found.some(r => r.name === 'Glowing Mushroom Stew')).toBe(true);
    expect(found.some(r => r.name === 'Berry & Ration Crumble')).toBe(true);
    expect(found.some(r => r.name === 'Wasteland Worm & Potato Hash')).toBe(true);
    expect(found.some(r => r.name === 'Cactus Nectar Refresher')).toBe(true);
  });

  it('should be case-insensitive for ingredient matching', () => {
    const available = ['mutant mushroom', 'dusty water', 'scavenged spice mix', 'canned mystery meat'];
    const found = findRecipes(available);
    expect(found.length).toBeGreaterThan(0);
    expect(found.some(r => r.name === 'Glowing Mushroom Stew')).toBe(true);
  });

  it('should not find a recipe if a required ingredient is missing', () => {
    const available = ['Mutant Mushroom', 'Dusty Water', 'Scavenged Spice Mix']; // Missing Canned Mystery Meat
    const found = findRecipes(available);
    expect(found.some(r => r.name === 'Glowing Mushroom Stew')).toBe(false);
  });
});
