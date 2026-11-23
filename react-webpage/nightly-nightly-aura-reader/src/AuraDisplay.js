import React from 'react';

function AuraDisplay({ sentiment }) {
  let color = '#888'; // Default neutral grey
  let shape = '50%'; // Default circle
  let boxShadow = '0 0 20px rgba(136, 136, 136, 0.5)';

  if (sentiment === 1) {
    // Positive
    color = 'linear-gradient(45deg, #a8e063, #56ab2f)'; // Green to darker green
    shape = '50%'; // Smooth circle
    boxShadow = '0 0 30px rgba(86, 171, 47, 0.7)';
  } else if (sentiment === -1) {
    // Negative
    color = 'linear-gradient(45deg, #ff416c, #ff4b2b)'; // Red to orange-red
    shape = '60% 40% 50% 50% / 50% 50% 60% 40%'; // Slightly jagged/uneven shape
    boxShadow = '0 0 30px rgba(255, 65, 108, 0.7)';
  } else {
    // Neutral
    color = 'linear-gradient(45deg, #4facfe, #00f2fe)'; // Blue to cyan
    shape = '50%'; // Regular circle
    boxShadow = '0 0 20px rgba(79, 172, 254, 0.5)';
  }

  const auraStyle = {
    width: '150px',
    height: '150px',
    background: color,
    borderRadius: shape,
    transition: 'all 0.5s ease-in-out',
    boxShadow: boxShadow
  };

  return <div style={auraStyle}></div>;
}

export default AuraDisplay;
