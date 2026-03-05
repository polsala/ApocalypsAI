import React from 'react';

const CelestialBody = ({ name, angle, color, radius = 10, orbitRadius = 150 }) => {
  // Convert angle to radians for CSS positioning
  const radians = (angle - 90) * (Math.PI / 180); // -90 to start from top (0 degrees at 12 o'clock)

  const x = orbitRadius * Math.cos(radians);
  const y = orbitRadius * Math.sin(radians);

  const style = {
    position: 'absolute',
    left: `calc(50% + ${x}px - ${radius}px)`,
    top: `calc(50% + ${y}px - ${radius}px)`,
    width: `${radius * 2}px`,
    height: `${radius * 2}px`,
    borderRadius: '50%',
    backgroundColor: color,
    display: 'flex',
    justifyContent: 'center',
    alignItems: 'center',
    fontSize: '0.7em',
    fontWeight: 'bold',
    color: 'black',
    border: '1px solid rgba(255,255,255,0.5)',
    boxShadow: `0 0 8px ${color}`,
    zIndex: 10
  };

  return (
    <div style={style} title={`${name} (${angle.toFixed(1)}°)`}>
      {name.charAt(0)}
    </div>
  );
};

export default CelestialBody;
