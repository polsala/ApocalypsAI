import React from 'react';
import './EchoVisualizer.css';

const EchoVisualizer = ({ echoes }) => {
  const getColorForDistortion = (type) => {
    switch (type) {
      case 'Ripple': return '#FFD700'; // Gold
      case 'Warp': return '#FF4500';   // OrangeRed
      case 'Flicker': return '#00BFFF'; // DeepSkyBlue
      case 'Phase Shift': return '#9370DB'; // MediumPurple
      default: return '#A9A9A9'; // DarkGray
    }
  };

  return (
    <div className="echo-visualizer-container">
      <h2>Temporal Echoes</h2>
      {echoes.length === 0 ? (
        <p className="no-echoes">Enter a coordinate and generate echoes to see the temporal ripples.</p>
      ) : (
        <div className="timeline">
          <div className="timeline-axis">
            <span className="axis-label start">Past</span>
            <span className="axis-label center">Coordinate</span>
            <span className="axis-label end">Future</span>
          </div>
          <div className="echo-display">
            {echoes.map(echo => (
              <div
                key={echo.id}
                className="echo-bar"
                style={{
                  left: `calc(50% + ${echo.offset}px)`, // Position relative to center
                  width: `${echo.duration}px`,
                  backgroundColor: getColorForDistortion(echo.distortionType),
                  opacity: echo.intensity,
                  transform: `translateX(-${echo.duration / 2}px)` // Center the bar
                }}
                title={`Type: ${echo.distortionType}, Intensity: ${echo.intensity.toFixed(2)}, Offset: ${echo.offset}px`}
              >
                <span className="echo-label">{echo.distortionType}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default EchoVisualizer;
