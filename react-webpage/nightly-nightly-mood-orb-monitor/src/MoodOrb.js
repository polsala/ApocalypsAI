import React from 'react';
import './App.css'; // Using App.css for orb styles for simplicity

function MoodOrb({ sentiment }) {
  const getOrbStyle = () => {
    let color;
    let animationClass = 'orb-pulse-neutral'; // Default animation

    if (sentiment >= 8) {
      color = '#8aff8a'; // Vibrant Green
      animationClass = 'orb-pulse-high';
    } else if (sentiment >= 4) {
      color = '#ffff8a'; // Stable Yellow
      animationClass = 'orb-pulse-neutral';
    } else {
      color = '#ff8a8a'; // Anxious Red
      animationClass = 'orb-pulse-low';
    }

    return {
      backgroundColor: color,
      boxShadow: `0 0 15px ${color}, 0 0 30px ${color} inset`,
    };
  };

  const getOrbLabel = () => {
    if (sentiment >= 8) return 'Radiant';
    if (sentiment >= 4) return 'Stable';
    return 'Flickering';
  };

  return (
    <div className={`mood-orb ${getOrbLabel().toLowerCase()} ${getOrbStyle().animationClass || ''}`} style={getOrbStyle()}>
      <span className="orb-label">{getOrbLabel()} ({sentiment})</span>
    </div>
  );
}

export default MoodOrb;
