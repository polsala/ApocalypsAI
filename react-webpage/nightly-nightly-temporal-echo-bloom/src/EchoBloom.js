import React, { useState, useEffect, useRef, useCallback } from 'react';
import Echo from './Echo';

const MAX_ECHOES = 50;
const ECHO_LIFESPAN = 10000; // milliseconds
const ECHO_SPAWN_INTERVAL = 500; // milliseconds

function EchoBloom() {
  const [echoes, setEchoes] = useState([]);
  const echoIdRef = useRef(0);
  const containerRef = useRef(null);

  const generateEcho = useCallback(() => {
    if (!containerRef.current) return null;

    const containerRect = containerRef.current.getBoundingClientRect();
    const id = echoIdRef.current++;
    const size = Math.random() * 20 + 10; // 10px to 30px
    const x = Math.random() * (containerRect.width - size);
    const y = Math.random() * (containerRect.height - size);
    const initialVelocityX = (Math.random() - 0.5) * 0.5; // -0.25 to 0.25
    const initialVelocityY = (Math.random() - 0.5) * 0.5; // -0.25 to 0.25

    return {
      id,
      x,
      y,
      size,
      harmonized: false,
      createdAt: Date.now(),
      velocityX: initialVelocityX,
      velocityY: initialVelocityY,
      temporalSignature: Math.random() // A value between 0 and 1
    };
  }, []);

  const updateEchoes = useCallback(() => {
    setEchoes(prevEchoes => {
      const now = Date.now();
      return prevEchoes
        .filter(echo => now - echo.createdAt < ECHO_LIFESPAN)
        .map(echo => {
          let newX = echo.x + echo.velocityX;
          let newY = echo.y + echo.velocityY;

          // Simple boundary check and bounce
          if (containerRef.current) {
            const containerRect = containerRef.current.getBoundingClientRect();
            if (newX < 0 || newX + echo.size > containerRect.width) {
              echo.velocityX *= -1;
              newX = Math.max(0, Math.min(newX, containerRect.width - echo.size));
            }
            if (newY < 0 || newY + echo.size > containerRect.height) {
              echo.velocityY *= -1;
              newY = Math.max(0, Math.min(newY, containerRect.height - echo.size));
            }
          }

          return { ...echo, x: newX, y: newY };
        });
    });
  }, []);

  // Effect for spawning new echoes
  useEffect(() => {
    const spawnInterval = setInterval(() => {
      setEchoes(prevEchoes => {
        if (prevEchoes.length < MAX_ECHOES) {
          const newEcho = generateEcho();
          return newEcho ? [...prevEchoes, newEcho] : prevEchoes;
        }
        return prevEchoes;
      });
    }, ECHO_SPAWN_INTERVAL);

    return () => clearInterval(spawnInterval);
  }, [generateEcho]);

  // Effect for updating echo positions (animation loop)
  useEffect(() => {
    let animationFrameId;
    const animate = () => {
      updateEchoes();
      animationFrameId = requestAnimationFrame(animate);
    };

    animationFrameId = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(animationFrameId);
  }, [updateEchoes]);

  const handleEchoClick = useCallback((id) => {
    setEchoes(prevEchoes =>
      prevEchoes.map(echo =>
        echo.id === id ? { ...echo, harmonized: !echo.harmonized } : echo
      )
    );
  }, []);

  return (
    <div ref={containerRef} className="echo-bloom-container">
      {echoes.map(echo => (
        <Echo key={echo.id} echo={echo} onClick={handleEchoClick} />
      ))}
    </div>
  );
}

export default EchoBloom;
