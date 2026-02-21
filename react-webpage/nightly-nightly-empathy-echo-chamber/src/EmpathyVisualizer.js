import React from 'react';
import './EmpathyVisualizer.css';

const EmpathyVisualizer = ({ mood, color }) => {
  const getShapeClass = (currentMood) => {
    switch (currentMood) {
      case 'calm': return 'shape-circle';
      case 'tense': return 'shape-triangle';
      case 'hopeful': return 'shape-diamond'; // Simplified from star
      case 'chaotic': return 'shape-square';
      default: return 'shape-none';
    }
  };

  return (
    <div className="empathy-visualizer-container">
      <h3>Empathy Echo:</h3>
      <div className="visual-feedback" style={{ backgroundColor: color }}>
        <div className={`mood-shape ${getShapeClass(mood)}`}></div>
        <p className="mood-text">{mood ? `Feeling: ${mood.charAt(0).toUpperCase() + mood.slice(1)}` : 'Awaiting input...'}</p>
      </div>
    </div>
  );
};

export default EmpathyVisualizer;
