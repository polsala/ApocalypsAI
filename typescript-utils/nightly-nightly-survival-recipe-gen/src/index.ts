import { findRecipes } from './recipeGenerator';
import { allIngredients } from './data';

function main() {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    console.log('Usage: npm run cli <ingredient1> <ingredient2> ...');
    console.log('\nAvailable ingredients:');
    allIngredients.forEach(ing => console.log(`- ${ing.name}`));
    return;
  }

  const availableIngredients = args;
  const recipes = findRecipes(availableIngredients);

  if (recipes.length === 0) {
    console.log('No recipes found with your available ingredients. Keep scavenging!');
  } else {
    console.log('Found the following recipes:');
    recipes.forEach(recipe => {
      console.log(`\n--- ${recipe.name.toUpperCase()} ---`);
      console.log(`Description: ${recipe.description}`);
      console.log(`Difficulty: ${recipe.difficulty.charAt(0).toUpperCase() + recipe.difficulty.slice(1)}`);
      console.log(`Servings: ${recipe.servings}`);
      console.log('Required Ingredients:');
      recipe.requiredIngredients.forEach(req => console.log(`  - ${req.ingredientName}${req.quantity ? ` (x${req.quantity})` : ''}`));
      console.log('Instructions:');
      recipe.instructions.forEach((step, i) => console.log(`  ${i + 1}. ${step}`));
    });
  }
}

main();
