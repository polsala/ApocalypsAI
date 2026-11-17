export function analyzeSentiment(text) {
  if (!text) return 0;

  const lowerText = text.toLowerCase();
  let score = 0;

  const positiveKeywords = ['good', 'great', 'happy', 'success', 'love', 'awesome', 'excellent', 'positive', 'stable', 'nominal', 'functional', 'working', 'resolved'];
  const negativeKeywords = ['bad', 'fail', 'sad', 'error', 'bug', 'broken', 'issue', 'problem', 'negative', 'unstable', 'anomaly', 'critical', 'failure'];

  for (const keyword of positiveKeywords) {
    if (lowerText.includes(keyword)) {
      score++;
    }
  }

  for (const keyword of negativeKeywords) {
    if (lowerText.includes(keyword)) {
      score--;
    }
  }

  if (score > 0) return 1; // Overall positive
  if (score < 0) return -1; // Overall negative
  return 0; // Neutral or balanced
}
