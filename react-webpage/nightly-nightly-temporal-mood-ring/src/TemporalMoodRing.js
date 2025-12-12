import React from 'react';
import './TemporalMoodRing.css';

const getMood = (severity) => {
  if (severity < 0.2) {
    return { mood: 'Temporal Calm', color: '#4CAF50' }; // Green
  } else if (severity < 0.4) {
    return { mood: 'Mild Ripples', color: '#8BC34A' }; // Light Green
  } else if (severity < 0.6) {
    return { mood: 'Wobbly Warp', color: '#FFEB3B' }; // Yellow
  } else if (severity < 0.8) {
    return { mood: 'Chronal Instability', color: '#FF9800' }; // Orange
  } else {
    return { mood: 'Chronal Chaos!', color: '#F44336' }; // Red
  }
};

function TemporalMoodRing({ severity }) {
  const { mood, color } = getMood(severity);

  return (
    <div className="temporal-mood-ring-container">
      <div className="temporal-orb" style={{ backgroundColor: color }} data-testid="temporal-orb">
        <div className="orb-inner-glow"></div>
      </div>
      <p className="temporal-mood-text">Current Temporal Mood: <strong>{mood}</strong></p>
      <p className="temporal-severity-display">Severity Index: {severity.toFixed(2)}</p>
    </div>
  );
}

export default TemporalMoodRing;
