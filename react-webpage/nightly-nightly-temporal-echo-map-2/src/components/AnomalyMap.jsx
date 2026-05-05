import React from 'react';
import './AnomalyMap.css';

const AnomalyMap = ({ anomalies, gridSize }) => {
  const getCellIntensity = (x, y) => {
    // Sum intensities for all anomalies in this cell
    const totalIntensity = anomalies
      .filter(anomaly => anomaly.x === x && anomaly.y === y)
      .reduce((sum, anomaly) => sum + anomaly.intensity, 0);
    return totalIntensity; // Keep raw sum for title, cap for color calculation
  };

  const renderGrid = () => {
    const grid = [];
    for (let y = 0; y < gridSize; y++) {
      for (let x = 0; x < gridSize; x++) {
        const rawIntensity = getCellIntensity(x, y);
        const cappedIntensity = Math.min(rawIntensity, 255); // Cap at 255 for color calculation

        // Map intensity to a color scale from green (low) to red (high)
        const red = Math.min(255, cappedIntensity * 2); // Scale intensity to red component
        const green = Math.max(0, 255 - cappedIntensity * 2); // Scale intensity to green component
        const blue = 0;
        const backgroundColor = `rgb(${red}, ${green}, ${blue})`;

        grid.push(
          <div
            key={`${x}-${y}`}
            className="anomaly-cell"
            style={{ backgroundColor }}
            title={`Cell (${x},${y}) - Intensity: ${rawIntensity.toFixed(2)}`}
          >
            {/* Optional: display intensity value */}
            {/* {rawIntensity > 0 ? rawIntensity.toFixed(0) : ''} */}
          </div>
        );
      }
    }
    return grid;
  };

  return (
    <div 
      className="anomaly-map-grid" 
      style={{ 
        gridTemplateColumns: `repeat(${gridSize}, 1fr)`,
        gridTemplateRows: `repeat(${gridSize}, 1fr)`
      }}
    >
      {renderGrid()}
    </div>
  );
};

export default AnomalyMap;
