import React from 'react';
import './App.css'; // Reusing App.css for general styles

const MoodRing = ({ moodValue }) => {
  // moodValue is expected to be between 0 and 100
  const getColor = (value) => {
    if (value < 25) return '#FF4500'; // OrangeRed - Chaotic
    if (value < 50) return '#FFD700'; // Gold - Uncertain
    if (value < 75) return '#32CD32'; // LimeGreen - Balanced
    return '#1E90FF'; // DodgerBlue - Serene
  };

  const ringStyle = {
    backgroundColor: getColor(moodValue),
    boxShadow: `0 0 20px 5px ${getColor(moodValue)}`
  };

  return (
    <div className="mood-ring" style={ringStyle}>
      <div className="mood-ring-inner"></div>
    </div>
  );
};

export default MoodRing;
