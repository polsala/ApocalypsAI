import React from 'react';
import './Echo.css';

function Echo({ echo, onClick }) {
  const { id, x, y, size, harmonized, temporalSignature } = echo;

  const echoStyle = {
    left: `${x}px`,
    top: `${y}px`,
    width: `${size}px`,
    height: `${size}px`,
    backgroundColor: harmonized
      ? `hsl(${temporalSignature * 360}, 70%, 60%)` // Harmonized color based on signature
      : `rgba(255, 255, 255, ${0.2 + temporalSignature * 0.4})`, // Fading white/grey
    boxShadow: harmonized
      ? `0 0 ${size / 2}px ${size / 4}px hsl(${temporalSignature * 360}, 80%, 70%)`
      : 'none',
    transform: harmonized ? 'scale(1.2)' : 'scale(1)',
    transition: 'background-color 0.3s ease, box-shadow 0.3s ease, transform 0.3s ease'
  };

  return (
    <div
      className={`echo ${harmonized ? 'harmonized' : ''}`}
      style={echoStyle}
      onClick={() => onClick(id)}
      title={harmonized ? `Harmonized Echo #${id}` : `Echo #${id}`}
    ></div>
  );
}

export default Echo;
