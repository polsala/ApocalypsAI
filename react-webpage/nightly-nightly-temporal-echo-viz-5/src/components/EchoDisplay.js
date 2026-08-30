import React from 'react';

function EchoDisplay({ echo }) {
  return (
    <li className="echo-item">
      <strong>ID:</strong> {echo.id}<br />
      <strong>Type:</strong> {echo.type}<br />
      <strong>Intensity:</strong> {echo.intensity}<br />
      <strong>Timestamp:</strong> {new Date(echo.timestamp).toLocaleString()}<br />
      <strong>Description:</strong> {echo.description}
    </li>
  );
}

export default EchoDisplay;
