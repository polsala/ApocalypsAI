import React from 'react';
import './MoodRing.css';

const MoodRing = ({ sentiment }) => {
  let ringColor = '#FFEB3B'; // Default neutral yellow

  switch (sentiment) {
    case 'positive':
      ringColor = '#4CAF50'; // Green
      break;
    case 'negative':
      ringColor = '#F44336'; // Red
      break;
    case 'neutral':
    default:
      ringColor = '#FFEB3B'; // Yellow
      break;
  }

  return (
    <div className="mood-ring-container">
      <div className="mood-ring" style={{ backgroundColor: ringColor }} data-testid="mood-ring"></div>
    </div>
  );
};

export default MoodRing;
