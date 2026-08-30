import React from 'react';
import './MoodRing.css';

const MoodRing = ({ mood, color }) => {
  return (
    <div className="mood-ring-container">
      <div className="mood-ring" style={{ backgroundColor: color }}>
        <span className="mood-text">{mood}</span>
      </div>
    </div>
  );
};

export default MoodRing;
