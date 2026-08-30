import React from 'react';
import './MoodRing.css'; // For basic styling

const MoodRing = ({ score, color }) => {
  const moodText = score > 0 ? "Positive" : score < 0 ? "Negative" : "Neutral";
  const absScore = Math.abs(score);
  let intensityText = "";
  if (absScore > 5) intensityText = "Strongly";
  else if (absScore > 2) intensityText = "Moderately";
  else if (absScore > 0) intensityText = "Mildly";

  return (
    <div className="mood-ring-container">
      <div className="mood-ring" style={{ backgroundColor: color }} role="presentation" aria-label="Mood Ring"></div>
      <p className="mood-text">Current Mood: {intensityText} {moodText}</p>
      <p className="mood-score">Sentiment Score: {score}</p>
    </div>
  );
};

export default MoodRing;
