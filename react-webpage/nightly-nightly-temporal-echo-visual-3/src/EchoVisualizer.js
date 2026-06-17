import React, { useRef, useEffect, useState } from 'react';

const EchoVisualizer = () => {
  const canvasRef = useRef(null);
  const animationFrameId = useRef(null);
  const [dimensions, setDimensions] = useState({ width: 600, height: 400 });

  // # Mock rationale: requestAnimationFrame and cancelAnimationFrame are browser APIs
  // # that need to be mocked for deterministic testing outside a browser environment.
  // # They control the animation loop, which is central to this component's functionality.
  // # These are fallback mocks for environments where window.requestAnimationFrame is not present.
  const mockRequestAnimationFrame = (callback) => setTimeout(callback, 16);
  const mockCancelAnimationFrame = (id) => clearTimeout(id);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const context = canvas.getContext('2d');
    let echoes = [];
    const maxEchoes = 10;
    const echoSpawnInterval = 1000; // milliseconds
    let lastSpawnTime = 0;

    // Function to create a new echo
    const createEcho = (x, y) => ({
      x,
      y,
      radius: 0,
      alpha: 1,
      speed: 0.5 + Math.random() * 0.5, // pixels per frame
      color: `hsl(${Math.random() * 360}, 70%, 50%)`
    });

    // Initial echoes
    for (let i = 0; i < 3; i++) {
      echoes.push(createEcho(
        Math.random() * dimensions.width,
        Math.random() * dimensions.height
      ));
    }

    const animate = (currentTime) => {
      context.clearRect(0, 0, dimensions.width, dimensions.height);

      // Spawn new echo if interval passed and not too many echoes
      if (currentTime - lastSpawnTime > echoSpawnInterval && echoes.length < maxEchoes) {
        echoes.push(createEcho(
          Math.random() * dimensions.width,
          Math.random() * dimensions.height
        ));
        lastSpawnTime = currentTime;
      }

      echoes = echoes.filter(echo => echo.alpha > 0.01);

      echoes.forEach(echo => {
        echo.radius += echo.speed;
        echo.alpha -= 0.005; // Decay rate

        context.beginPath();
        context.arc(echo.x, echo.y, echo.radius, 0, Math.PI * 2, false);
        context.strokeStyle = `rgba(97, 218, 251, ${echo.alpha})`; // React blue
        context.lineWidth = 2;
        context.stroke();

        // Add a secondary, fainter ripple for more depth
        if (echo.radius > 10) {
          context.beginPath();
          context.arc(echo.x, echo.y, echo.radius * 0.7, 0, Math.PI * 2, false);
          context.strokeStyle = `rgba(97, 218, 251, ${echo.alpha * 0.5})`;
          context.lineWidth = 1;
          context.stroke();
        }
      });

      animationFrameId.current = (window.requestAnimationFrame || mockRequestAnimationFrame)(animate);
    };

    animationFrameId.current = (window.requestAnimationFrame || mockRequestAnimationFrame)(animate);

    return () => {
      (window.cancelAnimationFrame || mockCancelAnimationFrame)(animationFrameId.current);
    };
  }, [dimensions]); // Re-run effect if dimensions change

  return (
    <canvas
      ref={canvasRef}
      width={dimensions.width}
      height={dimensions.height}
      aria-label="Temporal Echo Visualization"
      role="img"
    />
  );
};

export default EchoVisualizer;
