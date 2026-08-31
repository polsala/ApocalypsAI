export type ClothingCategory = "top" | "bottom" | "outerwear" | "footwear" | "accessory";
export type Color = "red" | "blue" | "green" | "yellow" | "black" | "white" | "grey" | "pink" | "purple" | "brown" | "orange";
export type StyleTag = "casual" | "formal" | "sporty" | "boho" | "vintage" | "minimalist" | "cozy" | "edgy";
export type WarmthLevel = "cold" | "cool" | "mild" | "warm" | "hot";

export interface ClothingItem {
  id: string;
  name: string;
  category: ClothingCategory;
  color: Color;
  styleTags: StyleTag[];
  warmth: WarmthLevel;
  available: boolean;
}

export interface Mood {
  name: string;
  preferredColors: Color[];
  preferredStyleTags: StyleTag[];
  warmthPreference: WarmthLevel;
  requiredCategories: ClothingCategory[];
  optionalCategories: ClothingCategory[];
}

export interface OutfitSuggestion {
  mood: Mood;
  items: ClothingItem[];
  score: number; // How well it matches the mood
  message: string;
}
