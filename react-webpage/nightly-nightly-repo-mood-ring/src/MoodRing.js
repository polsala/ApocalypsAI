import React from 'react';
import './MoodRing.css';

function MoodRing({ color, moodText }) {
  return (
    <div className="mood-ring-container">
      <div className="mood-ring" style={{ backgroundColor: color }}>
        <span className="mood-text">{moodText}</span>
      </div>
      <p className="mood-label">Current Repo Mood</p>
    </div>
  );
}

export default MoodRing;
