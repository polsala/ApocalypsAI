import React from 'react';
import './MoodRing.css';

function MoodRing({ mood }) {
  return (
    <div className="mood-container">
      <div className="mood-ring" data-testid="mood-ring-element" style={{ borderColor: mood.color }}>
        <div className="mood-indicator" style={{ backgroundColor: mood.color }}></div>
      </div>
      <p className="mood-description" style={{ color: mood.color }}>
        Current Mood: {mood.description}
      </p>
    </div>
  );
}

export default MoodRing;
