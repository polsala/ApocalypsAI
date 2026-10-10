import React from 'react';

function EchoDisplay({ selectedEcho }) {
  if (!selectedEcho) {
    return (
      <div className="echo-display">
        <h2>Echo Details</h2>
        <p>Select an echo on the map to see its details.</p>
      </div>
    );
  }

  return (
    <div className="echo-display">
      <h2>Echo ID: {selectedEcho.id}</h2>
      <p><strong>Location:</strong> Lat {selectedEcho.location.lat.toFixed(4)}, Lng {selectedEcho.location.lng.toFixed(4)}</p>
      <p><strong>Intensity:</strong> {selectedEcho.intensity} (out of 10)</p>
      <p><strong>Timestamp:</strong> {new Date(selectedEcho.timestamp).toLocaleString()}</p>
      <p><strong>Description:</strong> {selectedEcho.description}</p>
      <p><em>"A faint whisper from a forgotten yesterday..."</em></p>
    </div>
  );
}

export default EchoDisplay;
