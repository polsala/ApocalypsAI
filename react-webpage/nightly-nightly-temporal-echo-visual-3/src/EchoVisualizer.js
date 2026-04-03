import React, { useRef, useEffect } from 'react';

const EchoVisualizer = ({ signature }) => {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    // Clear canvas
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    if (!signature) {
      ctx.font = '16px Arial';
      ctx.fillStyle = '#888';
      ctx.textAlign = 'center';
      ctx.fillText('Enter a temporal signature to visualize...', canvas.width / 2, canvas.height / 2);
      return;
    }

    // --- Whimsical Temporal Echo Pattern Generation Logic ---
    // Convert signature to a numerical seed for deterministic pattern generation
    const seed = signature.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);

    const numPoints = 50 + (seed % 50); // Number of points in the pattern (50 to 99)
    const maxRadius = Math.min(canvas.width, canvas.height) / 2 - 20;
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2;

    ctx.lineWidth = 1 + (seed % 3); // Line thickness variation
    ctx.lineCap = 'round';

    // Generate points in a spiral-like fashion, influenced by the seed
    const points = [];
    for (let i = 0; i < numPoints; i++) {
      const angle = (i / numPoints) * Math.PI * 2 * (1 + (seed % 3)); // Spiral turns
      const radius = (i / numPoints) * maxRadius * (0.8 + (seed % 20) / 100); // Expanding radius
      const x = centerX + Math.cos(angle) * radius;
      const y = centerY + Math.sin(angle) * radius;
      points.push({ x, y });
    }

    // Draw interconnected lines, with dynamic colors
    ctx.beginPath();
    if (points.length > 0) {
      ctx.moveTo(points[0].x, points[0].y);
    }

    for (let i = 1; i < points.length; i++) {
      const p2 = points[i];

      // Dynamic color based on point index and seed (HSL for vibrant colors)
      const hue = (seed + i * 10) % 360;
      const saturation = 70 + (seed % 30); // 70-99%
      const lightness = 50 + (i % 20);    // 50-69%
      ctx.strokeStyle = `hsl(${hue}, ${saturation}%, ${lightness}%)`;

      ctx.lineTo(p2.x, p2.y);
      ctx.stroke(); // Stroke each segment for varying colors
      ctx.beginPath(); // Start new path for next segment
      ctx.moveTo(p2.x, p2.y);
    }

    // Add a central "echo core" for emphasis
    ctx.beginPath();
    const coreRadius = 5 + (seed % 10);
    const coreHue = (seed * 2) % 360;
    ctx.arc(centerX, centerY, coreRadius, 0, Math.PI * 2);
    ctx.fillStyle = `hsl(${coreHue}, 80%, 60%)`;
    ctx.fill();
    ctx.strokeStyle = `hsl(${coreHue}, 90%, 40%)`;
    ctx.lineWidth = 2;
    ctx.stroke();

  }, [signature]); // Redraw the pattern whenever the signature prop changes

  return (
    <canvas
      ref={canvasRef}
      width={400}
      height={400}
      style={{ border: '1px solid #333', borderRadius: '8px', background: '#1a1a1a' }}
      aria-label="Temporal Echo Visualization"
    />
  );
};

export default EchoVisualizer;
