import React, { useRef, useEffect, useState, useCallback } from 'react';

function RippleCanvas({
  rippleSpeed,
  rippleDecay,
  maxRipples,
  rippleColor,
  isPaused,
  clearTrigger,
}) {
  const canvasRef = useRef(null);
  const animationFrameId = useRef(null);
  const [ripples, setRipples] = useState([]);
  const lastFrameTime = useRef(0);

  const addRipple = useCallback((x, y) => {
    setRipples(prevRipples => {
      const newRipple = {
        id: Date.now() + Math.random(),
        x,
        y,
        radius: 0,
        opacity: 1,
        startTime: performance.now(),
      };
      const updatedRipples = [...prevRipples, newRipple];
      // Keep only the latest 'maxRipples'
      return updatedRipples.slice(-maxRipples);
    });
  }, [maxRipples]);

  const draw = useCallback((timestamp) => {
    if (isPaused) {
      lastFrameTime.current = timestamp;
      animationFrameId.current = requestAnimationFrame(draw);
      return;
    }

    const deltaTime = timestamp - lastFrameTime.current;
    lastFrameTime.current = timestamp;

    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    setRipples(prevRipples => {
      const updatedRipples = prevRipples.map(ripple => {
        const elapsed = (timestamp - ripple.startTime) / 1000; // in seconds
        const newRadius = ripple.radius + rippleSpeed * deltaTime;
        const newOpacity = ripple.opacity - rippleDecay * deltaTime;

        return {
          ...ripple,
          radius: newRadius,
          opacity: Math.max(0, newOpacity),
        };
      }).filter(ripple => ripple.opacity > 0);

      updatedRipples.forEach(ripple => {
        ctx.beginPath();
        ctx.arc(ripple.x, ripple.y, ripple.radius, 0, Math.PI * 2);
        ctx.strokeStyle = rippleColor;
        ctx.lineWidth = 2;
        ctx.globalAlpha = ripple.opacity;
        ctx.stroke();
      });
      ctx.globalAlpha = 1; // Reset globalAlpha

      return updatedRipples;
    });

    animationFrameId.current = requestAnimationFrame(draw);
  }, [rippleSpeed, rippleDecay, rippleColor, isPaused]);

  // Effect for animation loop
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    // Set canvas dimensions to fill parent
    const resizeCanvas = () => {
      canvas.width = canvas.offsetWidth;
      canvas.height = canvas.offsetHeight;
    };
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);

    lastFrameTime.current = performance.now();
    animationFrameId.current = requestAnimationFrame(draw);

    return () => {
      window.removeEventListener('resize', resizeCanvas);
      cancelAnimationFrame(animationFrameId.current);
    };
  }, [draw]);

  // Effect for clearing ripples
  useEffect(() => {
    setRipples([]);
  }, [clearTrigger]);

  const handleCanvasClick = useCallback((event) => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const rect = canvas.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;
    addRipple(x, y);
  }, [addRipple]);

  return (
    <canvas
      ref={canvasRef}
      onClick={handleCanvasClick}
      style={{
        border: '1px solid #00ff00',
        backgroundColor: '#000',
        cursor: 'crosshair',
        flexGrow: 1,
        maxWidth: 'calc(100% - 290px)', // Account for control panel width + gap
        height: '100%',
        boxShadow: '0 0 10px rgba(0, 255, 0, 0.5)',
      }}
    />
  );
}

export default RippleCanvas;
