const keywordMap = {
  "worried": "considering",
  "anxious": "anticipating",
  "scared": "aware",
  "overwhelmed": "challenged",
  "difficult": "intriguing",
  "problem": "puzzle",
  "lonely": "reflective",
  "stressed": "energized",
  "bad": "interesting",
  "terrible": "unique",
  "fear": "awareness",
  "struggle": "endeavor"
};

const voidWhispers = [
  "The void hums a tune of possibility.",
  "A cosmic giggle echoes: all is well.",
  "Your thoughts are stardust, ever shifting.",
  "Embrace the glorious unknown, says the void.",
  "Even chaos has a rhythm, and you're part of it.",
  "The universe winks, suggesting a new perspective.",
  "Perhaps a squirrel holds the answer, whispers the void.",
  "All timelines converge into a moment of calm."
];

function reRollThought(originalThought) {
  let reRolled = originalThought.toLowerCase();

  for (const [oldWord, newWord] of Object.entries(keywordMap)) {
    // Use regex with global and case-insensitive flags for robust replacement
    // \b ensures whole word matching
    const regex = new RegExp(`\\b${oldWord}\\b`, 'gi');
    reRolled = reRolled.replace(regex, newWord);
  }

  const randomWhisper = voidWhispers[Math.floor(Math.random() * voidWhispers.length)];

  // Capitalize the first letter of the re-rolled thought for better readability
  reRolled = reRolled.charAt(0).toUpperCase() + reRolled.slice(1);

  return `${reRolled}. ${randomWhisper}`;
}

module.exports = { reRollThought, keywordMap, voidWhispers };
