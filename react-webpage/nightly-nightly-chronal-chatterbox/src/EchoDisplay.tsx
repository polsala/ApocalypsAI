import React, { useEffect, useState } from 'react';
import { TemporalEcho } from './EchoGenerator';

interface EchoDisplayProps {
  echo: TemporalEcho;
  onFadeOut: (id: string) => void;
}

const EchoDisplay: React.FC<EchoDisplayProps> = ({ echo, onFadeOut }) => {
  const [opacity, setOpacity] = useState(1);
  const [scale, setScale] = useState(1);

  useEffect(() => {
    const fadeDuration = 5000; // Total duration for echo to be visible and fade
    const initialDelay = 1000; // How long it stays at full opacity
    const fadeStart = initialDelay;

    const timer = setTimeout(() => {
      const fadeInterval = setInterval(() => {
        setOpacity(prev => {
          const newOpacity = prev - (1 / (fadeDuration - initialDelay)) * 100; // Adjust fade speed
          if (newOpacity <= 0) {
            clearInterval(fadeInterval);
            onFadeOut(echo.id);
            return 0;
          }
          return newOpacity;
        });
        setScale(prev => prev + 0.005); // Slowly grow as it fades
      }, 50); // Update every 50ms
    }, fadeStart);

    return () => {
      clearTimeout(timer);
    };
  }, [echo.id, onFadeOut]);

  return (
    <div
      style={{
        opacity,
        transform: `scale(${scale})`,
        transition: 'opacity 0.1s linear, transform 0.1s ease-out',
        position: 'absolute',
        top: `${Math.random() * 80 + 10}vh`, // Random vertical position
        left: `${Math.random() * 80 + 10}vw`, // Random horizontal position
        padding: '10px 15px',
        backgroundColor: 'rgba(50, 50, 80, 0.7)',
        borderRadius: '8px',
        boxShadow: '0 4px 8px rgba(0, 0, 0, 0.3)',
        fontSize: '1.1em',
        color: '#b0b0ff',
        zIndex: 10,
        pointerEvents: 'none', // Allow clicks to pass through
        maxWidth: '300px',
        textAlign: 'center'
      }}
    >
      {echo.message}
    </div>
  );
};

export default EchoDisplay;
