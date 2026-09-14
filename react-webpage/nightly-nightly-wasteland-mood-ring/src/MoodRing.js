import React from 'react';

const moodDefinitions = {
  "Serene Oasis": {
    color: "#8BC34A", // Light Green
    keywords: ["water", "shelter", "calm", "safe", "grow", "find", "peace", "rest", "oasis", "garden", "verdant"],
    interpretation: "A tranquil moment in the wasteland. Resources are abundant, or peace is found within."
  },
  "Dusty Despair": {
    color: "#795548", // Brown
    keywords: ["lost", "empty", "ruin", "alone", "despair", "broken", "scarcity", "hopeless", "barren", "ash", "dust", "decay"],
    interpretation: "The weight of the dust settles. A feeling of loss, scarcity, or overwhelming sadness."
  },
  "Scavenger's Spark": {
    color: "#FFC107", // Amber
    keywords: ["found", "craft", "build", "hope", "bright", "idea", "discovery", "ingenuity", "spark", "gleam", "fix", "create"],
    interpretation: "A flicker of hope, a new discovery, or the thrill of crafting something useful from nothing."
  },
  "Rift Rumbles": {
    color: "#F44336", // Red
    keywords: ["danger", "attack", "fight", "rift", "anomaly", "threat", "anger", "warning", "unstable", "quake", "blast", "hostile"],
    interpretation: "Temporal distortions or immediate threats loom. Proceed with extreme caution, or prepare for conflict."
  },
  "Void Whispers": {
    color: "#3F51B5", // Indigo
    keywords: ["void", "echo", "strange", "unknown", "whisper", "mystery", "existential", "unseen", "shadow", "cosmic", "abyss", "unfathomable"],
    interpretation: "The void speaks, or unseen forces are at play. A sense of the unknown, or profound cosmic contemplation."
  }
};

export const analyzeMood = (text) => {
  if (!text || text.trim() === '') {
    return { name: "Neutral Haze", color: "#BDBDBD", interpretation: "The wasteland is vast and indifferent. No strong resonance detected." };
  }

  const lowerText = text.toLowerCase();
  let bestMood = { name: "Neutral Haze", color: "#BDBDBD", interpretation: "The wasteland is vast and indifferent. No strong resonance detected." };
  let maxScore = 0;

  for (const moodName in moodDefinitions) {
    const mood = moodDefinitions[moodName];
    let score = 0;
    mood.keywords.forEach(keyword => {
      // Use regex for whole word matching to avoid partial matches (e.g., "grow" in "growing")
      const regex = new RegExp(`\\b${keyword}\\b`, 'g');
      score += (lowerText.match(regex) || []).length;
    });

    if (score > maxScore) {
      maxScore = score;
      bestMood = {
        name: moodName,
        color: mood.color,
        interpretation: mood.interpretation
      };
    } else if (score === maxScore && score > 0) {
      // If scores are tied, prefer the first one encountered (or could add more complex tie-breaking)
      // For simplicity, we'll just keep the first one found.
    }
  }
  return bestMood;
};

const MoodRing = ({ text }) => {
  const { name, color, interpretation } = analyzeMood(text);

  return (
    <div className="mood-ring-container" style={{ backgroundColor: color }}>
      <h3 className="mood-name">{name}</h3>
      <p className="mood-interpretation">{interpretation}</p>
    </div>
  );
};

export default MoodRing;
