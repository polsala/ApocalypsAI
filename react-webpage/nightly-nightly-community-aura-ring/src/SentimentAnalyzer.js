/**
 * A simple, keyword-based sentiment analyzer for mock GitHub event messages.
 * This is a simplified model for demonstration and deterministic testing.
 */
const sentimentKeywords = {
  'Tense': ['bug', 'error', 'fail', 'issue', 'critical', 'unexpected', 'investigating', 'problem'],
  'Active': ['feature', 'new', 'add', 'implement', 'working', 'reviewing', 'progress'],
  'Calm': ['fix', 'resolve', 'done', 'stable', 'resolved', 'patch', 'documentation', 'minor'],
  'Joyful': ['awesome', 'great', 'fantastic', 'good', 'success', 'happy', 'love']
};

/**
 * Analyzes a list of messages to determine a collective sentiment.
 * @param {string[]} messages - An array of strings representing event messages.
 * @returns {string} The determined mood ('Calm', 'Active', 'Tense', 'Joyful', 'Neutral').
 */
export function analyzeSentiment(messages) {
  let scores = {
    'Calm': 0,
    'Active': 0,
    'Tense': 0,
    'Joyful': 0,
    'Neutral': 0
  };

  if (!messages || messages.length === 0) {
    return 'Neutral';
  }

  messages.forEach(message => {
    const lowerMessage = message.toLowerCase();
    let messageMoodDetected = false;

    for (const mood in sentimentKeywords) {
      for (const keyword of sentimentKeywords[mood]) {
        if (lowerMessage.includes(keyword)) {
          scores[mood]++;
          messageMoodDetected = true;
          break; // Only count one keyword per mood per message for simplicity
        }
      }
    }
    if (!messageMoodDetected) {
      scores['Neutral']++;
    }
  });

  // Determine the dominant mood
  let dominantMood = 'Neutral';
  let maxScore = scores['Neutral']; // Neutral is baseline if no other strong mood

  // Prioritize non-neutral moods
  for (const mood of ['Tense', 'Active', 'Calm', 'Joyful']) { // Explicit order for deterministic tie-breaking
    if (scores[mood] > maxScore) {
      maxScore = scores[mood];
      dominantMood = mood;
    } else if (scores[mood] === maxScore && maxScore > 0) {
      // If tied, keep the current dominantMood unless the new one has higher implicit priority
      // (e.g., Tense > Active > Calm > Joyful if scores are equal)
      // This simple iteration order already provides a deterministic tie-break.
    }
  }

  return dominantMood;
}
