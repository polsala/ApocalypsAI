import React, { useState, useEffect } from 'react';

const AffirmationTicker = () => {
  const affirmations = [
    "The void whispers strength through silence.",
    "Time bends, but you endure.",
    "Every echo carries a lesson.",
    "Chaos fuels creation."
  ];

  const [current, setCurrent] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrent(prev => (prev + 1) % affirmations.length);
    }, 3000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div style={{ padding: '1rem', background: '#222', color: '#fff', textAlign: 'center' }}>
      <marquee>{affirmations[current]}</marquee>
    </div>
  );
};

export default AffirmationTicker;
