import { Relic, Rarity, ClassificationResult, KeywordRule } from './types';

const DEFAULT_RULES: KeywordRule[] = [
  { keywords: ['broken', 'rusty', 'junk'], rarityBoost: 'Common', utilityBoost: -2, description: 'Indicates low quality or damage.' },
  { keywords: ['shiny', 'gleaming', 'intact'], rarityBoost: 'Uncommon', utilityBoost: 1, description: 'Suggests good condition or aesthetic value.' },
  { keywords: ['data-chip', 'circuit', 'module'], rarityBoost: 'Uncommon', utilityBoost: 3, description: 'Electronic components, potentially useful.' },
  { keywords: ['power-cell', 'energy-core', 'reactor'], rarityBoost: 'Rare', utilityBoost: 5, description: 'Power sources are always valuable.' },
  { keywords: ['ancient', 'pre-fall', 'artifact'], rarityBoost: 'Rare', utilityBoost: 4, description: 'Historical significance, might hold secrets.' },
  { keywords: ['glowing', 'pulsating', 'anomalous'], rarityBoost: 'Legendary', utilityBoost: 7, description: 'Unusual properties, high potential.' },
  { keywords: ['schematic', 'blueprint', 'formula'], rarityBoost: 'Legendary', utilityBoost: 8, description: 'Knowledge is power, especially lost knowledge.' },
  { keywords: ['void-shard', 'temporal-flux', 'reality-anchor'], rarityBoost: 'Mythic', utilityBoost: 10, description: 'Items of immense, possibly dangerous, power.' },
];

const RARITY_ORDER: Rarity[] = ['Common', 'Uncommon', 'Rare', 'Legendary', 'Mythic'];

export function classifyRelic(relic: Relic, customRules: KeywordRule[] = []): ClassificationResult {
  let currentRarity: Rarity = 'Common';
  let currentUtilityScore: number = 0;
  const reasons: string[] = [];

  const allRules = [...DEFAULT_RULES, ...customRules];
  const relicText = `${relic.name} ${relic.description || ''}`.toLowerCase();

  for (const rule of allRules) {
    const matchedKeywords = rule.keywords.filter(kw => relicText.includes(kw.toLowerCase()));
    if (matchedKeywords.length > 0) {
      reasons.push(`${rule.description || 'Matched rule'}: ${matchedKeywords.join(', ')}`);

      if (rule.rarityBoost) {
        const ruleRarityIndex = RARITY_ORDER.indexOf(rule.rarityBoost);
        const currentRarityIndex = RARITY_ORDER.indexOf(currentRarity);
        if (ruleRarityIndex > currentRarityIndex) {
          currentRarity = rule.rarityBoost;
        }
      }
      if (rule.utilityBoost !== undefined) {
        currentUtilityScore += rule.utilityBoost;
      }
    }
  }

  // Ensure utility score is within a reasonable range
  currentUtilityScore = Math.max(0, Math.min(10, currentUtilityScore));

  return {
    relic,
    rarity: currentRarity,
    utilityScore: currentUtilityScore,
    reason: reasons.length > 0 ? reasons : ['No specific rules matched, classified as Common.'],
  };
}

export function sortClassifiedRelics(results: ClassificationResult[]): ClassificationResult[] {
  return results.sort((a, b) => {
    // Primary sort: Rarity (Mythic > Legendary > ...)
    const rarityDiff = RARITY_ORDER.indexOf(b.rarity) - RARITY_ORDER.indexOf(a.rarity);
    if (rarityDiff !== 0) {
      return rarityDiff;
    }
    // Secondary sort: Utility Score (higher is better)
    return b.utilityScore - a.utilityScore;
  });
}
