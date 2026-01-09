import React, { useState } from 'react';
import MapDisplay from './MapDisplay';

// Mock rationale: This function simulates a complex cosmic alignment calculation.
// In a real-world scenario, this might involve external APIs, complex algorithms,
// or sensor data. For deterministic, offline testing, we use a simple, predictable
// pseudo-random generation or a predefined set of outcomes.
const calculateCosmicAlignment = () => {
  const score = Math.floor(Math.random() * 100) + 1; // Score between 1 and 100
  const locations = [
    { name: 'The Whispering Nook', lat: 34.0522, lon: -118.2437, vibe: 'serene' }, // Los Angeles
    { name: 'The Temporal Tear Terrace', lat: 40.7128, lon: -74.0060, vibe: 'energetic' }, // New York
    { name: 'The Void-Touched Veranda', lat: 51.5074, lon: -0.1278, vibe: 'mysterious' }, // London
    { name: 'The Quantum Quasar Quarters', lat: 35.6895, lon: 139.6917, vibe: 'innovative' }, // Tokyo
    { name: 'The Galactic Grotto', lat: -33.8688, lon: 151.2093, vibe: 'ancient' } // Sydney
  ];
  const recommendedLocation = locations[Math.floor(Math.random() * locations.length)];

  let message;
  if (score > 80) {
    message = `The cosmos hums with harmony! Your alignment is exceptional.`;
  } else if (score > 50) {
    message = `A gentle cosmic breeze guides your path. Good alignment.`;
  } else {
    message = `Minor temporal eddies detected. Seek balance, wanderer.`;
  }

  return { score, recommendedLocation, message };
};

function CosmicCompass() {
  const [alignment, setAlignment] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleScan = () => {
    setLoading(true);
    // Simulate an async operation
    setTimeout(() => {
      const result = calculateCosmicAlignment();
      setAlignment(result);
      setLoading(false);
    }, 1000);
  };

  return (
    <div>
      <p>Consult the cosmic currents to find your optimal spot!</p>
      <button onClick={handleScan} disabled={loading}>
        {loading ? 'Scanning...' : 'Scan for Cosmic Alignment'}
      </button>

      {alignment && (
        <div className="compass-result">
          <p><strong>Cosmic Alignment Score:</strong> {alignment.score}/100</p>
          <p><strong>Cosmic Message:</strong> {alignment.message}</p>
          <p>
            <strong>Recommended Location:</strong> {alignment.recommendedLocation.name} 
            (Vibe: {alignment.recommendedLocation.vibe})
          </p>
          <MapDisplay 
            latitude={alignment.recommendedLocation.lat}
            longitude={alignment.recommendedLocation.lon}
            label={alignment.recommendedLocation.name}
          />
        </div>
      )}
    </div>
  );
}

export default CosmicCompass;
