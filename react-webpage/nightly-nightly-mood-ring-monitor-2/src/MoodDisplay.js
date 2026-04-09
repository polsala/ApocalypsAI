import React from 'react';
import './App.css'; // Reusing App.css for general styles

const MoodDisplay = ({ moodText }) => {
  return (
    <p className="mood-text">Current Vibe: {moodText}</p>
  );
};

export default MoodDisplay;
