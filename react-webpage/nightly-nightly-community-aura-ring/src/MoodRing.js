import React from 'react';
import './MoodRing.css';

const moodColors = {
  'Calm': '#8BC34A',    // Light Green
  'Active': '#FFC107',  // Amber
  'Tense': '#F44336',   // Red
  'Joyful': '#03A9F4',  // Light Blue
  'Neutral': '#9E9E9E'  // Grey
};

function MoodRing({ mood }) {
  const ringColor = moodColors[mood] || moodColors['Neutral'];

  return (
    <div className="mood-ring-container">
      <div className="mood-ring" style={{ borderColor: ringColor }}>
        <span className="mood-text">{mood}</span>
      </div>
    </div>
  );
}

export default MoodRing;
