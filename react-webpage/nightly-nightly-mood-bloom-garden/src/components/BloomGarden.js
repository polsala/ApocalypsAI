import React from 'react';
import './BloomGarden.css';

function BloomGarden({ blooms }) {
  return (
    <div className="bloom-garden-container" data-testid="bloom-garden-container">
      {blooms.map(bloom => (
        <div
          key={bloom.id}
          className="bloom"
          data-testid="bloom-item"
          style={{
            width: `${bloom.size}px`,
            height: `${bloom.size}px`,
            backgroundColor: bloom.color,
            transform: `rotate(${bloom.rotation}deg)`,
            left: `${bloom.x}%`,
            top: `${bloom.y}%`,
            animationDelay: `${bloom.delay}s`
          }}
        ></div>
      ))}
    </div>
  );
}

export default BloomGarden;
