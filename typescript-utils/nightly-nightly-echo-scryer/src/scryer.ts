import { ScryOptions, ScryReport, KeywordCategory, KeywordMatch } from './types';

const APOCALYPTIC_KEYWORDS: { [key in KeywordCategory]: string[] } = {
  Survival: ['shelter', 'water', 'food', 'safe', 'survive', 'rations', 'medicine', 'camp', 'hideout', 'secure'],
  Danger: ['threat', 'danger', 'enemy', 'attack', 'raid', 'infected', 'mutant', 'radiation', 'collapse', 'warning'],
  Resource: ['fuel', 'ammo', 'parts', 'scrap', 'supplies', 'battery', 'map', 'tools', 'gear', 'cache'],
  Hope: ['beacon', 'signal', 'hope', 'future', 'rebuild', 'community', 'alliance', 'peace', 'dawn', 'new beginning'],
  Mystery: ['anomaly', 'signal', 'unknown', 'whisper', 'void', 'strange', 'glitch', 'rumor', 'shadow', 'unseen'],
  Technology: ['radio', 'computer', 'network', 'power grid', 'generator', 'drone', 'satellite', 'data', 'circuit', 'system']
};

export function scryText(text: string, options: ScryOptions): ScryReport {
  const originalText = text;
  let cleanedText = text.toLowerCase();

  // Simple fragmentation cleaning: remove non-alphanumeric noise, normalize spaces
  // The fragmentThreshold could be used here to control how aggressively we clean.
  // For simplicity, let's just do a basic cleanup.
  cleanedText = cleanedText.replace(/[^a-z0-9\s]/g, ' ').replace(/\s+/g, ' ').trim();

  const identifiedKeywords: KeywordMatch[] = [];
  const categoryCounts: Record<KeywordCategory, number> = {
    Survival: 0,
    Danger: 0,
    Resource: 0,
    Hope: 0,
    Mystery: 0,
    Technology: 0
  };

  const words = cleanedText.split(' ');

  for (const category in APOCALYPTIC_KEYWORDS) {
    const keywords = APOCALYPTIC_KEYWORDS[category as KeywordCategory];
    for (const keyword of keywords) {
      // Use regex for whole word matching to avoid partial matches
      const regex = new RegExp(`\\b${keyword}\\b`, 'g');
      let match;
      while ((match = regex.exec(cleanedText)) !== null) {
        identifiedKeywords.push({ keyword, category: category as KeywordCategory, index: match.index });
        categoryCounts[category as KeywordCategory]++;
      }
    }
  }

  // Sort keywords by index for consistent highlighting later
  identifiedKeywords.sort((a, b) => a.index - b.index);

  let dominantCategory: KeywordCategory | 'Neutral' = 'Neutral';
  let maxCount = 0;
  for (const category in categoryCounts) {
    if (categoryCounts[category as KeywordCategory] > maxCount) {
      maxCount = categoryCounts[category as KeywordCategory];
      dominantCategory = category as KeywordCategory;
    } else if (categoryCounts[category as KeywordCategory] === maxCount && maxCount > 0) {
      // If there's a tie, it's less clear, keep it 'Neutral' or pick one arbitrarily.
      // For now, let's say if there's a tie, it's less dominant.
      // Or, we could make it more complex, e.g., "Mixed Vibe".
      // Let's keep the first one found as dominant if tied, or 'Neutral' if no keywords.
    }
  }
  if (maxCount === 0) dominantCategory = 'Neutral';


  let apocalypticVibe = 'The echoes are faint, but a presence is felt.';
  let suggestedAction = 'Remain vigilant.';

  switch (dominantCategory) {
    case 'Survival':
      apocalypticVibe = 'A strong sense of perseverance and self-preservation permeates the echoes.';
      suggestedAction = 'Prioritize immediate needs: food, water, shelter. Fortify your position.';
      break;
    case 'Danger':
      apocalypticVibe = 'Warning! The echoes resonate with imminent threat and peril.';
      suggestedAction = 'Prepare for conflict or evasion. Assess your defenses and escape routes.';
      break;
    case 'Resource':
      apocalypticVibe = 'The echoes speak of valuable findings and essential supplies.';
      suggestedAction = 'Scavenge wisely. Secure and catalog any resources found.';
      break;
    case 'Hope':
      apocalypticVibe = 'A glimmer of hope shines through the static, suggesting connection or a new beginning.';
      suggestedAction = 'Seek out potential allies or signals. Maintain morale.';
      break;
    case 'Mystery':
      apocalypticVibe = 'An unsettling enigma shrouds the echoes, hinting at the unknown.';
      suggestedAction = 'Proceed with extreme caution. Document anomalies and avoid direct confrontation.';
      break;
    case 'Technology':
      apocalypticVibe = 'Flickers of old-world tech or advanced systems are detected.';
      suggestedAction = 'Investigate technological remnants. Power up or repurpose devices if possible.';
      break;
    case 'Neutral':
      apocalypticVibe = 'The echoes are indistinct, offering no clear direction or dominant theme.';
      suggestedAction = 'Continue monitoring. Observe your surroundings carefully.';
      break;
  }

  if (options.contextLevel === 'medium') {
    if (categoryCounts.Danger > 0 && categoryCounts.Survival > 0) {
      apocalypticVibe += ' A struggle for survival against odds is evident.';
      suggestedAction = 'Balance defense with resource gathering. Stay mobile if necessary.';
    }
  } else if (options.contextLevel === 'high') {
    if (categoryCounts.Danger > 0 && categoryCounts.Hope > 0) {
      apocalypticVibe += ' Despite the peril, a resilient spirit of hope persists.';
      suggestedAction = 'Identify sources of danger and hope. Protect the hopeful elements.';
    }
    if (categoryCounts.Resource > 0 && categoryCounts.Technology > 0) {
      apocalypticVibe += ' Old tech holds the key to new resources.';
      suggestedAction = 'Prioritize salvaging and understanding technological components for resource generation.';
    }
  }


  return {
    originalText,
    cleanedText,
    identifiedKeywords,
    categoryCounts,
    dominantCategory,
    apocalypticVibe,
    suggestedAction,
  };
}
