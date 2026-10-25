import React, { useRef, useEffect, useState, useCallback } from 'react';

const RippleCanvas = ({ rippleCount, rippleSpeed, rippleDecay, colorScheme }) => {
  const canvasRef = useRef(null);
  const [ripples, setRipples] = useState([]);
  const animationFrameId = useRef(null);

  const generateRandomRipple = useCallback((canvasWidth, canvasHeight) => {
    return {
      id: Date.now() + Math.random(),
      x: Math.random() * canvasWidth,
      y: Math.random() * canvasHeight,
      radius: 0,
      maxRadius: Math.min(canvasWidth, canvasHeight) * (0.1 + Math.random() * 0.4), // 10-50% of min dimension
      opacity: 1,
      color: `hsl(${Math.random() * 360}, 70%, 60%)`, // Random vibrant color
      speedMultiplier: 0.5 + Math.random() * 1.5 // Vary speed slightly
    };
  }, []);

  const draw = useCallback((ctx, canvasWidth, canvasHeight) => {
    ctx.clearRect(0, 0, canvasWidth, canvasHeight);

    setRipples(prevRipples => {
      const newRipples = prevRipples
        .map(ripple => {
          const newRadius = ripple.radius + (rippleSpeed * ripple.speedMultiplier);
          const newOpacity = ripple.opacity - rippleDecay;

          if (newOpacity <= 0 || newRadius > ripple.maxRadius) {
            return null; // Mark for removal
          }

          return { ...ripple, radius: newRadius, opacity: newOpacity };
        })
        .filter(Boolean); // Remove nulls

      // Add new ripples if count is less than desired
      while (newRipples.length < rippleCount) {
        newRipples.push(generateRandomRipple(canvasWidth, canvasHeight));
      }

      // If too many ripples, remove the oldest ones
      while (newRipples.length > rippleCount) {
        newRipples.shift(); // Remove from the beginning
      }

      newRipples.forEach(ripple => {
        ctx.beginPath();
        ctx.arc(ripple.x, ripple.y, ripple.radius, 0, Math.PI * 2);
        ctx.strokeStyle = ripple.color;
        ctx.lineWidth = 2;
        ctx.globalAlpha = ripple.opacity;
        ctx.stroke();
      });

      return newRipples;
    });
  }, [rippleCount, rippleSpeed, rippleDecay, generateRandomRipple]);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    const dpr = window.devicePixelRatio || 1;
    const rect = canvas.getBoundingClientRect();

    canvas.width = rect.width * dpr;
    canvas.height = rect.height * dpr;
    ctx.scale(dpr, dpr);

    // Initial ripples
    setRipples(Array.from({ length: rippleCount }, () => generateRandomRipple(rect.width, rect.height)));

    const animate = () => {
      draw(ctx, rect.width, rect.height);
      animationFrameId.current = requestAnimationFrame(animate);
    };

    animationFrameId.current = requestAnimationFrame(animate);

    return () => {
      if (animationFrameId.current) {
        cancelAnimationFrame(animationFrameId.current);
      }
    };
  }, [draw, rippleCount, generateRandomRipple]); // Redraw effect when draw function or rippleCount changes

  return (
    <canvas ref={canvasRef} role="canvas" />
  );
};

export default RippleCanvas;
