export type Ingredient = {
  name: string;
  category: 'protein' | 'vegetable' | 'fruit' | 'grain' | 'liquid' | 'spice' | 'other';
  isEdibleRaw: boolean;
};

export type Recipe = {
  name: string;
  description: string;
  requiredIngredients: { ingredientName: string; quantity?: number }[];
  instructions: string[];
  servings: number;
  difficulty: 'easy' | 'medium' | 'hard';
};
