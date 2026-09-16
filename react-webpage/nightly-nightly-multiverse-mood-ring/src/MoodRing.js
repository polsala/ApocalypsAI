import React from 'react';
import './MoodRing.css';

const MoodRing = ({ name, status, color, animationClass }) => {
  return (
    <div className={`mood-ring ${animationClass}`} style={{ backgroundColor: color }}>
      <h3>{name}</h3>
      <p>{status}</p>
    </div>
  );
};

export default MoodRing;
