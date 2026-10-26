import React, { useState, useEffect } from 'react';

const DustBunny = ({ id, x, y, size, onCollect }) => {
  const [position, setPosition] = useState({ x, y });
  const [velocity, setVelocity] = useState({ dx: (Math.random() - 0.5) * 2, dy: (Math.random() - 0.5) * 2 });

  useEffect(() => {
    const animate = () => {
      setPosition(prevPos => {
        let newX = prevPos.x + velocity.dx;
        let newY = prevPos.y + velocity.dy;

        // Bounce off walls
        if (newX + size > window.innerWidth || newX < 0) {
          setVelocity(prevVel => ({ ...prevVel, dx: -prevVel.dx }));
          newX = Math.max(0, Math.min(window.innerWidth - size, newX)); // Clamp position
        }
        if (newY + size > window.innerHeight || newY < 0) {
          setVelocity(prevVel => ({ ...prevVel, dy: -prevVel.dy }));
          newY = Math.max(0, Math.min(window.innerHeight - size, newY)); // Clamp position
        }
        return { x: newX, y: newY };
      });
    };

    const animationFrame = requestAnimationFrame(function loop() {
      animate();
      requestAnimationFrame(loop);
    });

    return () => cancelAnimationFrame(animationFrame);
  }, [velocity, size]); // Re-run effect if velocity or size changes

  const handleClick = () => {
    onCollect(id);
  };

  return (
    <div
      className="dust-bunny"
      style={{
        position: 'absolute',
        left: position.x + 'px',
        top: position.y + 'px',
        width: size + 'px',
        height: size + 'px',
        borderRadius: '50%',
        backgroundColor: '#b0c4de', /* Light blue-grey */
        opacity: 0.7,
        cursor: 'pointer',
        boxShadow: '0 0 10px rgba(255,255,255,0.3)',
        transition: 'transform 0.1s ease-out',
        zIndex: 5
      }}
      onClick={handleClick}
      title="Click to collect this digital dust bunny!"
    ></div>
  );
};

export default DustBunny;
