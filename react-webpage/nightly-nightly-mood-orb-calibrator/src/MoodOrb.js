import React from 'react';

const MoodOrb = ({ sentiment }) => {
  let orbStyle = {};
  let emoji = '⚪'; // Default neutral

  switch (sentiment) {
    case 'positive':
      orbStyle = { backgroundColor: '#8BC34A' }; // Light Green
      emoji = '😊';
      break;
    case 'negative':
      orbStyle = { backgroundColor: '#F44336' }; // Red
      emoji = '😟';
      break;
    case 'neutral':
    default:
      orbStyle = { backgroundColor: '#FFEB3B' }; // Yellow
      emoji = '😐';
      break;
  }

  return (
    <div className="mood-orb" style={orbStyle}>
      <span className="mood-emoji" role="img" aria-label={sentiment + " mood"}>
        {emoji}
      </span>
    </div>
  );
};

export default MoodOrb;
