import React from 'react';
import './MoodInput.css';

function MoodInput({ currentMood, onMoodChange }) {
  const handleChange = (event) => {
    onMoodChange(parseInt(event.target.value, 10));
  };

  return (
    <div className="mood-input-container">
      <label htmlFor="mood-slider">Mood Level: {currentMood}</label>
      <input
        type="range"
        id="mood-slider"
        min="1"
        max="10"
        value={currentMood}
        onChange={handleChange}
        className="mood-slider"
      />
      <p className="mood-description">
        {currentMood <= 3 && "The garden feels a bit parched..."}
        {currentMood > 3 && currentMood <= 7 && "The garden is growing steadily."}
        {currentMood > 7 && "A vibrant, flourishing garden!"}
      </p>
    </div>
  );
}

export default MoodInput;
