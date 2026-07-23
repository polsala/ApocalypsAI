interface ScavengedItemClassification {
  category: 'Food/Water' | 'Tool/Weapon' | 'Resource/Material' | 'Medical/Survival' | 'Junk/Curiosity' | 'Uncategorized';
  utilityScore: number; // 1-10
  whimsicalRating: string;
  notes: string;
}

function getWhimsicalRating(score: number): string {
  if (score >= 9) return "Apocalypse Essential";
  if (score >= 7) return "Quite Handy";
  if (score >= 5) return "Potentially Useful";
  if (score >= 3) return "Mildly Amusing";
  return "Dust Collector";
}

export function classifyItem(description: string): ScavengedItemClassification {
  const lowerDesc = description.toLowerCase();
  let category: ScavengedItemClassification['category'] = 'Uncategorized';
  let utilityScore: number = 1;
  let notes: string = "Further inspection recommended.";

  // Mock rationale: Math.random() is used for whimsical score variation.
  // For deterministic tests, we'll mock Math.random() in the test file.
  const randomFactor = Math.random();

  // Food/Water
  if (/(can of|jar of|bottle of|purified|ration|water|food|beans|soup|jerky|mre|canned|drink|berry|mushroom|apple|bread)/.test(lowerDesc)) {
    category = 'Food/Water';
    utilityScore = Math.min(10, Math.max(1, Math.floor(randomFactor * 5) + 6)); // High score for food/water (6-10)
    notes = "Sustenance for the journey ahead.";
  }
  // Tool/Weapon
  else if (/(wrench|knife|crowbar|hammer|axe|gun|pistol|rifle|bow|arrow|flashlight|radio|multitool|saw|shovel|pickaxe|battery|charger)/.test(lowerDesc)) {
    category = 'Tool/Weapon';
    utilityScore = Math.min(10, Math.max(1, Math.floor(randomFactor * 6) + 4)); // Mid-high score (4-9)
    notes = "Could be used for crafting, defense, or utility.";
  }
  // Resource/Material
  else if (/(scrap metal|wire|cloth|fabric|wood|plastic|fuel|gasoline|oil|rope|leather|rubber|component|circuit|pipe|brick|stone)/.test(lowerDesc)) {
    category = 'Resource/Material';
    utilityScore = Math.min(10, Math.max(1, Math.floor(randomFactor * 6) + 3)); // Mid score (3-8)
    notes = "Valuable for crafting, repairs, or trade.";
  }
  // Medical/Survival
  else if (/(bandages|first aid|medkit|antiseptic|painkiller|antibiotic|splint|tourniquet|iodine|mask|gloves|tent|sleeping bag|compass|map)/.test(lowerDesc)) {
    category = 'Medical/Survival';
    utilityScore = Math.min(10, Math.max(1, Math.floor(randomFactor * 5) + 7)); // Very high score (7-10)
    notes = "Crucial for health and long-term survival.";
  }
  // Junk/Curiosity
  else if (/(broken toy|old book|shiny rock|dusty photo|magazine|newspaper|trinket|figurine|coin|keychain|empty bottle|rusty nail)/.test(lowerDesc)) {
    category = 'Junk/Curiosity';
    utilityScore = Math.min(10, Math.max(1, Math.floor(randomFactor * 4) + 1)); // Low score (1-4)
    notes = "Might hold sentimental value, or just be clutter.";
  }

  // Ensure utilityScore is within 1-10 range (redundant due to Math.min/max, but good for clarity)
  utilityScore = Math.max(1, Math.min(10, utilityScore));

  return {
    category,
    utilityScore,
    whimsicalRating: getWhimsicalRating(utilityScore),
    notes,
  };
}

// CLI execution
if (require.main === module) {
  const description = process.argv[2];
  if (!description) {
    console.error("Usage: ts-node src/index.ts \"<item description>\"");
    process.exit(1);
  }

  const classification = classifyItem(description);
  console.log(`\n--- Scavenged Item Report ---`);
  console.log(`Description: "${description}"`);
  console.log(`Category: ${classification.category}`);
  console.log(`Utility Score: ${classification.utilityScore}/10`);
  console.log(`Whimsical Rating: ${classification.whimsicalRating}`);
  console.log(`Notes: ${classification.notes}`);
  console.log(`-----------------------------\n`);
}
