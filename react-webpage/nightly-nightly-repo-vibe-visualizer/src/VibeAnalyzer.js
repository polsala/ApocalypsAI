const VIBE_KEYWORDS = {
  Optimistic: ['feat', 'add', 'new', 'improve', 'enhance', 'release', 'implement'],
  Chaotic: ['fix', 'bug', 'error', 'break', 'urgent', 'hotfix', 'vulnerability', 'resolve'],
  Serene: ['refactor', 'clean', 'docs', 'style', 'chore', 'test', 'cleanup', 'format'],
  Mysterious: ['update', 'adjust', 'tweak', 'change', 'revert', 'config', 'dependencies']
};

export function analyzeVibe(contributions) {
  const vibeCounts = {
    Optimistic: 0,
    Chaotic: 0,
    Serene: 0,
    Mysterious: 0
  };

  contributions.forEach(contribution => {
    const lowerCaseContribution = contribution.toLowerCase();
    let matched = false;

    for (const vibeCategory in VIBE_KEYWORDS) {
      for (const keyword of VIBE_KEYWORDS[vibeCategory]) {
        if (lowerCaseContribution.includes(keyword)) {
          vibeCounts[vibeCategory]++;
          matched = true;
          // Break after first match for a category to avoid double counting for a single contribution
          // e.g., "fix(bug): resolve issue" counts as 1 for Chaotic, not multiple.
          break; // Move to the next vibeCategory for this contribution
        }
      }
    }
    // If no specific vibe keyword is matched, it leans towards Mysterious
    if (!matched) {
        vibeCounts.Mysterious++;
    }
  });

  let dominantVibe = 'Mysterious';
  let maxCount = -1;

  // Find the dominant vibe, prioritizing if counts are equal (e.g., Optimistic > Chaotic > Serene > Mysterious)
  // This prioritization is arbitrary but ensures deterministic output for ties.
  const orderedVibes = ['Optimistic', 'Chaotic', 'Serene', 'Mysterious'];

  for (const vibe of orderedVibes) {
    if (vibeCounts[vibe] > maxCount) {
      maxCount = vibeCounts[vibe];
      dominantVibe = vibe;
    }
  }

  return dominantVibe;
}
