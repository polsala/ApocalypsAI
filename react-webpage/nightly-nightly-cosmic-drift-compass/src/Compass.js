import React from 'react';
import './App.css'; // Using App.css for shared styles

function Compass({ celestialBodies }) {
  return (
    <div className="compass-container">
      <div className="compass-rose">
        {celestialBodies.map((body, index) => {
          const rotation = body.currentAngle;
          const x = 50 + 40 * Math.sin(rotation * Math.PI / 180);
          const y = 50 - 40 * Math.cos(rotation * Math.PI / 180);

          return (
            <div
              key={index}
              className="celestial-body"
              style={{
                left: `${x}%`,
                top: `${y}%`,
                transform: `translate(-50%, -50%)`,
              }}
              title={body.name}
            >
              {body.icon}
            </div>
          );
        })}
        <div className="compass-center">🧭</div>
      </div>
      <div className="cardinal-points">
        <span className="north">N</span>
        <span className="east">E</span>
        <span className="south">S</span>
        <span className="west">W</span>
      </div>
    </div>
  );
}

export default Compass;
