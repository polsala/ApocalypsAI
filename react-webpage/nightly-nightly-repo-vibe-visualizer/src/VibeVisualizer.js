import React from 'react';
import './VibeVisualizer.css';

const VIBE_COLORS = {
  Optimistic: '#4CAF50', // Green
  Chaotic: '#F44336',    // Red
  Serene: '#2196F3',     // Blue
  Mysterious: '#9E9E9E'  // Grey
};

const VIBE_DESCRIPTIONS = {
  Optimistic: 'The repository is buzzing with new features and improvements!',
  Chaotic: 'There are many fixes and urgent changes. Hold on tight!',
  Serene: 'Refactoring, documentation, and cleanup are the focus. Calm waters ahead.',
  Mysterious: 'A mix of minor updates and tweaks. The path forward is unclear...'
};

function VibeVisualizer({ vibe }) {
  const color = VIBE_COLORS[vibe] || VIBE_COLORS.Mysterious;
  const description = VIBE_DESCRIPTIONS[vibe] || VIBE_DESCRIPTIONS.Mysterious;

  return (
    <div className="vibe-container">
      <div className="vibe-ring" style={{ borderColor: color }}>
        <div className="vibe-dot" style={{ backgroundColor: color }}></div>
      </div>
      <h2 className="vibe-text" style={{ color: color }}>{vibe}</h2>
      <p className="vibe-description">{description}</p>
    </div>
  );
}

export default VibeVisualizer;
