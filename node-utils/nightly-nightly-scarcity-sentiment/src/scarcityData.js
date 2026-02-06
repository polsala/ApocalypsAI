/**
 * Predefined scarcity factors for various item categories in a post-apocalyptic setting.
 * These values are subjective and can be adjusted based on the specific apocalypse scenario.
 * 
 * - `base`: Base scarcity score for the category.
 * - `decay`: Multiplier applied monthly (per 30 days) to simulate spoilage/wear.
 * - `valueMultiplier`: How much the user's perceived value impacts the score.
 */
const scarcityFactors = {
  "food": { base: 10, decay: 0.8, valueMultiplier: 1.5 }, // High base scarcity, decays over time, high value
  "water": { base: 12, decay: 0.9, valueMultiplier: 2.0 }, // Very high base scarcity, decays slowly, critical value
  "medicine": { base: 15, decay: 0.7, valueMultiplier: 2.5 }, // Extremely high base scarcity, decays, life-saving value
  "tools": { base: 8, decay: 0.95, valueMultiplier: 1.2 }, // Moderate scarcity, durable, practical value
  "ammo": { base: 10, decay: 0.9, valueMultiplier: 1.8 }, // High scarcity, critical for defense, high value
  "fuel": { base: 9, decay: 0.85, valueMultiplier: 1.6 }, // High scarcity, decays, utility value
  "luxury": { base: 3, decay: 0.5, valueMultiplier: 0.5 }, // Low base scarcity, decays quickly, low practical value
  "information": { base: 7, decay: 0.98, valueMultiplier: 1.3 }, // Moderate scarcity, very durable, intellectual value
  "components": { base: 6, decay: 0.92, valueMultiplier: 1.1 }, // Moderate scarcity, durable, crafting value
  "shelter_material": { base: 5, decay: 0.99, valueMultiplier: 1.0 }, // Low scarcity, very durable, foundational value
  "misc": { base: 4, decay: 0.9, valueMultiplier: 0.7 } // Default for uncategorized items
};

module.exports = scarcityFactors;
