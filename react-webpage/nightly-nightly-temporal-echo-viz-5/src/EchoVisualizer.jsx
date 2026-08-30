import React from 'react';
import './EchoVisualizer.css';

const EchoVisualizer = ({ params }) => {
  if (!params) {
    return null;
  }

  const { rippleCount, baseFrequency, colorHue, distortionMagnitude, animationSpeed, seed } = params;

  const circles = Array.from({ length: rippleCount }).map((_, i) => {
    const radius = 20 + i * (30 + distortionMagnitude * 10);
    const strokeWidth = 2 + (rippleCount - i) * 0.5;
    const opacity = 0.8 - i * (0.8 / rippleCount);
    const delay = i * (0.2 / animationSpeed);
    const duration = 2 + (rippleCount - i) * (0.5 / animationSpeed);

    // Generate a slightly different hue for each ripple based on the seed and index
    const rippleHue = (colorHue + (seed % 100) + i * 15) % 360;
    const strokeColor = `hsl(${rippleHue}, 70%, 60%)`;

    return (
      <circle
        key={i}
        cx="50%"
        cy="50%"
        r={radius}
        stroke={strokeColor}
        strokeWidth={strokeWidth}
        fill="none"
        opacity={opacity}
        style={{
          animation: `ripple ${duration}s infinite ease-out ${delay}s`,
          transformOrigin: 'center center'
        }}
      />
    );
  });

  return (
    <svg className="echo-visualizer" viewBox="0 0 400 400">
      {circles}
    </svg>
  );
};

export default EchoVisualizer;
