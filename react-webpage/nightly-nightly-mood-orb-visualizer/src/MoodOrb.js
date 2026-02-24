import React from 'react';
import './MoodOrb.css';

const MoodOrb = ({ mood }) => {
  // Map mood (-100 to 100) to a hue (0 to 120 for red to green)
  // -100 (red) -> 0 hue
  // 0 (yellow/orange) -> 60 hue
  // 100 (green) -> 120 hue
  const hue = ((mood + 100) / 200) * 120;
  const saturation = 80; // Keep saturation high for vibrant colors
  const lightness = 50; // Keep lightness medium

  const orbColor = `hsl(${hue}, ${saturation}%, ${lightness}%)`;

  // Map mood to animation speed or intensity
  // More extreme moods (positive or negative) could have more intense animation
  const animationSpeed = 1.5 - (Math.abs(mood) / 100) * 0.5; // Faster for neutral, slower for extreme
  const glowIntensity = 0.5 + (Math.abs(mood) / 100) * 0.5; // More intense glow for extreme moods

  const orbStyle = {
    '--orb-color': orbColor,
    '--animation-speed': `${animationSpeed}s`,
    '--glow-intensity': `${glowIntensity}`,
    boxShadow: `0 0 ${20 * glowIntensity}px ${orbColor}, inset 0 0 ${10 * glowIntensity}px rgba(255,255,255,0.5)`,
  };

  return (
    <div className="mood-orb-container" data-testid="mood-orb"> {/* Added data-testid */}
      <div className="mood-orb" style={orbStyle}></div>
    </div>
  );
};

export default MoodOrb;
