export const analyzeTextForAura = (text) => {
  const lowerText = text.toLowerCase();

  // Define keywords for each aura type and their associated colors
  const auraKeywords = {
    "Despair-ridden Gloom": {
      keywords: ['death', 'ruin', 'despair', 'hopeless', 'lost', 'danger', 'threat', 'fear', 'darkness', 'collapse', 'broken', 'suffering', 'wasteland', 'radiation', 'mutant'],
      color: '#8B0000' // Dark Red
    },
    "Scavenger's Hope": {
      keywords: ['resource', 'supply', 'water', 'food', 'shelter', 'find', 'discover', 'hope', 'survive', 'build', 'repair', 'safe', 'cache', 'trade', 'alliance', 'growth'],
      color: '#32CD32' // Lime Green
    },
    "Temporal Ripple": {
      keywords: ['time', 'anomaly', 'rift', 'echo', 'past', 'future', 'loop', 'distortion', 'glitch', 'temporal', 'shift', 'paradox', 'event horizon'],
      color: '#8A2BE2' // Blue Violet
    },
    "Whispers of the Void": {
      keywords: ['void', 'whisper', 'unknown', 'mystery', 'entity', 'cosmic', 'ancient', 'shadow', 'abyss', 'unseen', 'eldritch', 'dream', 'prophecy', 'omen'],
      color: '#4B0082' // Indigo
    }
  };

  let detectedAura = {
    type: "Neutral Dust",
    color: '#A9A9A9' // Dark Gray
  };
  let maxKeywordMatches = 0;

  // Iterate through each aura type to find the best match
  for (const auraType in auraKeywords) {
    let currentMatches = 0;
    for (const keyword of auraKeywords[auraType].keywords) {
      if (lowerText.includes(keyword)) {
        currentMatches++;
      }
    }
    // If current aura type has more matches, or equal matches but it's the first encountered (for deterministic ties),
    // update the detected aura.
    if (currentMatches > maxKeywordMatches) {
      maxKeywordMatches = currentMatches;
      detectedAura = {
        type: auraType,
        color: auraKeywords[auraType].color
      };
    } else if (currentMatches === maxKeywordMatches && currentMatches > 0) {
      // For ties, the first defined aura in the object takes precedence.
      // This ensures deterministic behavior for equal match counts.
      // No change needed here as the loop naturally prioritizes earlier keys.
    }
  }

  return detectedAura;
};
