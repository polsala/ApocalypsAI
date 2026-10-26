import React from 'react';
import './MoodRing.css';

function MoodRing({ mood }) {
  return (
    <div className="mood-ring-wrapper">
      <div className="mood-ring" style={{ backgroundColor: mood.color }}>
        <div className="mood-text">
          <h2>{mood.name}</h2>
          <p>{mood.description}</p>
        </div>
      </div>
    </div>
  );
}

export default MoodRing;
