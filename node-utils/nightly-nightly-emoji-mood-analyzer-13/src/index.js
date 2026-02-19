// Simple sentiment to emoji analyzer
const positiveWords = [
  "love", "happy", "joy", "awesome", "great", "good", "fantastic", "excellent", "wonderful", "sunny"
];
const negativeWords = [
  "hate", "sad", "bad", "terrible", "awful", "horrible", "depressed", "angry", "pain", "rainy"
];

function scoreText(text) {
  const words = text.toLowerCase().match(/\b\w+\b/g) || [];
  let score = 0;
  for (const w of words) {
    if (positiveWords.includes(w)) score += 1;
    else if (negativeWords.includes(w)) score -= 1;
  }
  return score;
}

function scoreToEmoji(score) {
  if (score > 2) return "😄";
  if (score >= 1) return "😊";
  if (score === 0) return "😐";
  if (score >= -2) return "🙁";
  return "😞";
}

function analyzeMood(text) {
  const s = scoreText(text);
  return scoreToEmoji(s);
}

// CLI mode
if (require.main === module) {
  const input = process.argv.slice(2).join(" ");
  if (!input) {
    console.error("Usage: node src/index.js \"your text here\"");
    process.exit(1);
  }
  console.log(analyzeMood(input));
}

module.exports = { analyzeMood };
