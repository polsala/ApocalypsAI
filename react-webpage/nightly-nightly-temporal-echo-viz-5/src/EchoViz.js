import React, { useRef, useEffect } from 'react';

/**
 * @typedef {Object} TemporalEcho
 * @property {string} id - Unique identifier for the echo.
 * @property {number} x - X coordinate (0-1, relative to canvas width).
 * @property {number} y - Y coordinate (0-1, relative to canvas height).
 * @property {number} intensity - How strong the echo is (0-1).
 * @property {number} age - How old the echo is (0-1, 1 being fully faded).
 */

/**
 * EchoViz component to visualize temporal echoes on a canvas.
 * @param {Object} props
 * @param {TemporalEcho[]} props.echoData - Array of temporal echo objects.
 */
const EchoViz = ({ echoData }) => {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Set canvas dimensions to fill parent
    const parent = canvas.parentElement;
    canvas.width = parent.clientWidth;
    canvas.height = parent.clientHeight;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    echoData.forEach(echo => {
      const x = echo.x * canvas.width;
      const y = echo.y * canvas.height;
      const radius = 5 + echo.intensity * 10; // Larger for stronger echoes
      const alpha = Math.max(0, 1 - echo.age - (1 - echo.intensity)); // Fade out with age and low intensity

      if (alpha <= 0) return; // Don't draw fully faded echoes

      // Draw echo as a glowing circle
      ctx.beginPath();
      ctx.arc(x, y, radius, 0, Math.PI * 2);
      ctx.fillStyle = `rgba(100, 180, 255, ${alpha})`; // Blueish glow
      ctx.shadowBlur = radius * 2;
      ctx.shadowColor = `rgba(100, 180, 255, ${alpha * 0.8})`;
      ctx.fill();

      ctx.shadowBlur = 0; // Reset shadow for next draws
    });
  }, [echoData]); // Redraw when echoData changes

  return (
    <canvas
      ref={canvasRef}
      role="img" 
      aria-label="Temporal Echo Visualization"
      style={{
        display: 'block',
        width: '100%',
        height: '100%',
        backgroundColor: 'transparent' // Parent handles background
      }}
    />
  );
};

export default EchoViz;
