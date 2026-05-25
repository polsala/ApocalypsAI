import React from 'react';
import './App.css';

const EchoVisualizer = ({ data }) => {
  if (!data || data.length === 0) {
    return <div className="echo-visualizer">No echo data to display.</div>;
  }

  const maxIntensity = Math.max(...data.map(d => d.intensity));

  const getBarHeight = (intensity) => {
    return `${(intensity / maxIntensity) * 100}%`;
  };

  const getBarColor = (distortionType) => {
    switch (distortionType) {
      case 'Chronal Ripple': return 'var(--color-ripple)';
      case 'Paradox Pulse': return 'var(--color-pulse)';
      case 'Void Whisper': return 'var(--color-whisper)';
      default: return 'var(--color-default)';
    }
  };

  return (
    <div className="echo-visualizer">
      <div className="echo-grid-container">
        {data.map((echo, index) => (
          <div
            key={index}
            className="echo-bar"
            style={{
              height: getBarHeight(echo.intensity),
              backgroundColor: getBarColor(echo.distortionType),
              opacity: echo.intensity * 0.8 + 0.2 // Min opacity 0.2 for visibility
            }}
            title={`Offset: ${echo.offset}s, Intensity: ${echo.intensity.toFixed(2)}, Type: ${echo.distortionType}`}
          ></div>
        ))}
      </div>
      <div className="legend">
        <span style={{ '--legend-color': 'var(--color-ripple)' }}>Chronal Ripple</span>
        <span style={{ '--legend-color': 'var(--color-pulse)' }}>Paradox Pulse</span>
        <span style={{ '--legend-color': 'var(--color-whisper)' }}>Void Whisper</span>
      </div>
    </div>
  );
};

export default EchoVisualizer;
