import React, { useRef, useEffect } from 'react';

function RippleCanvas({ eventDetails }) {
  const canvasRef = useRef(null);
  const { magnitude } = eventDetails;

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const context = canvas.getContext('2d');
    if (!context) return;

    const width = canvas.width;
    const height = canvas.height;
    const centerX = width / 2;
    const centerY = height / 2;
    const maxRadius = Math.min(width, height) / 2 - 10;

    // Clear canvas
    context.clearRect(0, 0, width, height);

    // Draw ripples
    for (let i = 0; i < magnitude; i++) {
      const rippleIndex = i + 1;
      const radius = (maxRadius / magnitude) * rippleIndex;
      const opacity = 1 - (rippleIndex / magnitude) * 0.7; // Ripples fade outwards
      const lineWidth = 2 + (magnitude - rippleIndex) * 0.1; // Inner ripples slightly thicker

      context.beginPath();
      context.arc(centerX, centerY, radius, 0, 2 * Math.PI);
      context.strokeStyle = `rgba(100, 149, 237, ${opacity})`; // Cornflower blue
      context.lineWidth = lineWidth;
      context.stroke();
      context.closePath();
    }
  }, [eventDetails, magnitude]); // Redraw when eventDetails or magnitude changes

  return (
    <canvas
      ref={canvasRef}
      width={400}
      height={400}
      className="ripple-canvas"
      aria-label="Chrono Ripple Visualization"
    ></canvas>
  );
}

export default RippleCanvas;
