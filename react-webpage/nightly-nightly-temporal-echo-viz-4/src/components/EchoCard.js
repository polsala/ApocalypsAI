import React from 'react';

function EchoCard({ echo }) {
  const { timestamp, intensity, origin, description } = echo;
  const date = new Date(timestamp).toLocaleString();

  return (
    <div className="echo-card">
      <h3>
        <span>Echo ID: {echo.id}</span>
        <span className="timestamp">{date}</span>
      </h3>
      <p><strong>Intensity:</strong> <span className="intensity">{intensity}/5</span></p>
      <p><strong>Origin:</strong> <span className="origin">{origin}</span></p>
      <p><strong>Description:</strong> {description}</p>
    </div>
  );
}

export default EchoCard;
