const positiveWords = new Set([
  "love", "hope", "joy", "peace", "calm", "safe", "good", "happy", "strong",
  "together", "build", "grow", "thrive", "survive", "light", "warm", "friend",
  "help", "share", "progress", "bright", "success", "victory", "comfort",
  "secure", "flourish", "optimism", "resilience", "unity", "trust"
]);

const negativeWords = new Set([
  "fear", "despair", "danger", "threat", "sad", "alone", "broken", "lost",
  "cold", "hungry", "enemy", "fight", "attack", "ruin", "dark", "struggle",
  "pain", "worry", "anxious", "stress", "crisis", "collapse", "desperate",
  "hostile", "gloom", "desolation", "famine", "sickness", "betrayal", "doubt"
]);

export const analyzeSentiment = (text) => {
  if (!text) return 0;
  const words = text.toLowerCase().match(/\b\w+\b/g) || [];
  let score = 0;
  words.forEach(word => {
    if (positiveWords.has(word)) {
      score += 1;
    } else if (negativeWords.has(word)) {
      score -= 1;
    }
  });
  return score;
};

export const getMoodColor = (score) => {
  if (score > 5) return "#4CAF50"; // Strong Positive (Green)
  if (score > 2) return "#8BC34A"; // Moderate Positive (Light Green)
  if (score > 0) return "#CDDC39"; // Mild Positive (Lime)
  if (score === 0) return "#9E9E9E"; // Neutral (Grey)
  if (score < -5) return "#F44336"; // Strong Negative (Red)
  if (score < -2) return "#FF9800"; // Moderate Negative (Orange)
  if (score < 0) return "#FFC107"; // Mild Negative (Amber)
  return "#9E9E9E"; // Default to neutral if something unexpected
};
