import { Recipe } from './types';
import { allRecipes } from './data';

export function findRecipes(availableIngredients: string[]): Recipe[] {
  const normalizedAvailable = new Set(availableIngredients.map(i => i.toLowerCase()));
  const foundRecipes: Recipe[] = [];

  for (const recipe of allRecipes) {
    const hasAllRequired = recipe.requiredIngredients.every(req =>
      normalizedAvailable.has(req.ingredientName.toLowerCase())
    );
    if (hasAllRequired) {
      foundRecipes.push(recipe);
    }
  }
  return foundRecipes;
}
