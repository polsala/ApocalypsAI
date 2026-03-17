// nightly-emoji-mood-analyzer
// Simple sentiment analyzer that returns an emoji based on word cues.

const POSITIVE_WORDS = new Set([
  "love",
  "happy",
  "joy",
  "joyful",
  "great",
  "awesome",
  "fantastic",
  "good",
  "wonderful",
  "excellent",
  "sunny",
  "delight",
  "pleased",
  "smile",
  "laugh",
  "peace",
  "cheer",
  "glad"
]);

const NEGATIVE_WORDS = new Set([
  "hate",
  "sad",
  "angry",
  "frustrated",
  "bad",
  "terrible",
  "awful",
  "worst",
  "pain",
  "sick",
  "depressed",
  "cry",
  "tear",
  "upset",
  "annoy",
  "disappointed",
  "stress"
]);

/**
 * Analyze the mood of a given text.
 * @param {string} text - Input sentence.
 * @returns {string} Emoji representing the mood.
 */
function analyzeMood(text) {
  if (typeof text !== "string" || text.trim().length === 0) {
    return "🤔"; // neutral / thinking
  }
  const words = text
    .toLowerCase()
    .replace(/[^a-z\s]/g, "")
    .split(/\s+/)
    .filter(Boolean);

  let score = 0;
  for (const w of words) {
    if (POSITIVE_WORDS.has(w)) score++;
    if (NEGATIVE_WORDS.has(w)) score--;
  }

  if (score > 1) return "😊"; // happy
  if (score < -1) return "😠"; // angry
  if (score === 1) return "🙂"; // slightly happy
  if (score === -1) return "🙁"; // slightly sad
  return "😐"; // neutral
}

// CLI handling
if (require.main === module) {
  const input = process.argv[2];
  if (!input) {
    console.error("Usage: node src/index.js \"Your sentence here\"");
    process.exit(1);
  }
  console.log(analyzeMood(input));
}

module.exports = { analyzeMood };
