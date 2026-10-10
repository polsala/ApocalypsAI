import React from 'react';
import './App.css'; // Re-using App.css for general styles

const SignalVisualizer = ({ data }) => {
  if (!data) {
    return null;
  }

  const { numRings, hueStart, hueEnd, rotationSpeed, flickerIntensity, ringThickness } = data;

  const rings = Array.from({ length: numRings }).map((_, i) => {
    const radius = 20 + i * 25; // Increase radius for each ring
    const strokeWidth = ringThickness;
    const hue = hueStart + (i / numRings) * (hueEnd - hueStart);
    const color = `hsl(${hue % 360}, 70%, 60%)`;
    const animationDelay = `${i * 0.1}s`;
    const animationDuration = `${4 / rotationSpeed}s`;

    return (
      <circle
        key={i}
        cx="200"
        cy="200"
        r={radius}
        fill="none"
        stroke={color}
        strokeWidth={strokeWidth}
        className="signal-ring"
        style={{
          animationDelay,
          animationDuration,
          '--flicker-intensity': flickerIntensity
        }}
      />
    );
  });

  return (
    <div className="signal-visualizer-container">
      <svg className="signal-svg" viewBox="0 0 400 400">
        {rings}
      </svg>
    </div>
  );
};

export default SignalVisualizer;
