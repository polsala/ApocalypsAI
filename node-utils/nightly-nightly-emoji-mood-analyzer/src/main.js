// Nightly Emoji Mood Analyzer
// Exported function analyzeMood(text) returns an emoji string.

function analyzeMood(text) {
  if (!text) return "ð¤";
  const lower = text.toLowerCase();
  const happy = ["love", "happy", "joy", "great", "awesome", "fantastic", "good", "wonderful", "glad", "excited"];
  const sad = ["sad", "unhappy", "depressed", "down", "bad", "terrible", "sorrow", "cry", "tears"];
  const angry = ["angry", "mad", "furious", "hate", "annoyed", "irritated", "rage"];
  const scared = ["scared", "fear", "afraid", "terrified", "panic"];
  const surprised = ["surprised", "shocked", "wow", "amazed", "astonished"];
  const neutral = ["okay", "fine", "meh", "average", "so-so"];

  const score = { happy: 0, sad: 0, angry: 0, scared: 0, surprised: 0, neutral: 0 };

  for (const word of happy) if (lower.includes(word)) score.happy++;
  for (const word of sad) if (lower.includes(word)) score.sad++;
  for (const word of angry) if (lower.includes(word)) score.angry++;
  for (const word of scared) if (lower.includes(word)) score.scared++;
  for (const word of surprised) if (lower.includes(word)) score.surprised++;
  for (const word of neutral) if (lower.includes(word)) score.neutral++;

  const max = Object.entries(score).reduce((a, b) => b[1] > a[1] ? b : a, ["neutral", 0]);
  const map = {
    happy: "ð",
    sad: "ð¢",
    angry: "ð ",
    scared: "ð±",
    surprised: "ð²",
    neutral: "ð"
  };
  return map[max[0]] || "ð¤";
}

// CLI mode
if (require.main === module) {
  const input = process.argv.slice(2).join(" ");
  console.log(analyzeMood(input));
}

module.exports = { analyzeMood };
