import React from 'react';

// Mock rationale: This component is a placeholder for a real map library (e.g., Leaflet, Mapbox).
// For the purpose of this utility and to ensure deterministic, offline testing, it simply
// displays the location coordinates and label as text. This avoids external API calls
// and complex rendering logic during tests.
function MapDisplay({ latitude, longitude, label }) {
  return (
    <div style={{
      border: '1px solid #61dafb',
      padding: '10px',
      marginTop: '15px',
      borderRadius: '5px',
      backgroundColor: '#3a3f47',
      color: '#fff',
      fontSize: '0.9em'
    }}>
      <p><strong>Map Display (Simulated):</strong></p>
      <p>Location: {label}</p>
      <p>Coordinates: Lat {latitude.toFixed(4)}, Lon {longitude.toFixed(4)}</p>
      <p>_A shimmering portal to this location is theoretically open._</p>
    </div>
  );
}

export default MapDisplay;
