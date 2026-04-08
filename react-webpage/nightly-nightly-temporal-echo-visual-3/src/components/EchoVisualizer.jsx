import React, { useState, useEffect, useCallback } from 'react';

const GRID_SIZE = 10; // 10x10 grid
const CELL_SIZE = 50; // Size of each cell in pixels
const SVG_WIDTH = GRID_SIZE * CELL_SIZE;
const SVG_HEIGHT = GRID_SIZE * CELL_SIZE;
const UPDATE_INTERVAL_MS = 200; // How often the echoes update

// Helper to initialize echo points
const initializeEchoPoints = () => {
  const points = [];
  for (let r = 0; r < GRID_SIZE; r++) {
    for (let c = 0; c < GRID_SIZE; c++) {
      points.push({
        id: `echo-${r}-${c}`,
        x: c * CELL_SIZE + CELL_SIZE / 2,
        y: r * CELL_SIZE + CELL_SIZE / 2,
        value: Math.random(), // Initial echo strength (0 to 1)
      });
    }
  }
  return points;
};

const EchoVisualizer = () => {
  const [echoPoints, setEchoPoints] = useState(initializeEchoPoints);

  const updateEchoes = useCallback(() => {
    setEchoPoints(prevPoints => {
      return prevPoints.map(point => {
        // Simulate echo decay and random fluctuation
        const newValue = Math.max(0, point.value * 0.95 + (Math.random() - 0.5) * 0.2);
        return { ...point, value: newValue };
      });
    });
  }, []);

  useEffect(() => {
    const intervalId = setInterval(updateEchoes, UPDATE_INTERVAL_MS);
    return () => clearInterval(intervalId);
  }, [updateEchoes]);

  return (
    <div className="echo-visualizer-container">
      <svg
        width={SVG_WIDTH}
        height={SVG_HEIGHT}
        viewBox={`0 0 ${SVG_WIDTH} ${SVG_HEIGHT}`}
        className="echo-grid"
        data-testid="echo-grid-svg"
      >
        {echoPoints.map(point => (
          <circle
            key={point.id}
            cx={point.x}
            cy={point.y}
            r={point.value * (CELL_SIZE / 2) * 0.8} // Radius based on value
            fill={`rgba(100, 150, 255, ${point.value})`} // Color based on value
            stroke="rgba(50, 100, 200, 0.5)"
            strokeWidth="1"
          />
        ))}
      </svg>
    </div>
  );
};

export default EchoVisualizer;
