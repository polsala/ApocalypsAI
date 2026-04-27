import React, { useState, useEffect } from 'react';
import './App.css';

// Mock celestial bodies for the apocalypic theme
const celestialBodies = [
  { id: 1, name: 'The Shattered Moon', x: 10, y: 20, description: 'Once a beacon, now a fractured reminder.' },
  { id: 2, name: 'The Crimson Nebula', x: 70, y: 40, description: 'A swirling vortex of forgotten dreams and cosmic dust.' },
  { id: 3, name: 'The Whispering Comet', x: 40, y: 80, description: 'It carries secrets from the edge of the void.' },
  { id: 4, name: 'The Obsidian Star', x: 90, y: 10, description: 'A point of absolute darkness, absorbing all light.' },
  { id: 5, name: 'The Glimmering Debris Field', x: 25, y: 60, description: 'Remnants of a glorious past, now scattered.' },
];

function App() {
  const [userLocation, setUserLocation] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setUserLocation({
            lat: position.coords.latitude,
            lng: position.coords.longitude,
          });
        },
        (err) => {
          setError(`Error getting location: ${err.message}`);
        }
      );
    } else {
      setError('Geolocation is not supported by your browser.');
    }
  }, []);

  // Simple mapping of lat/lng to a hypothetical canvas coordinate system
  // This is a simplification for visualization purposes.
  const mapLocationToCanvas = (lat, lng) => {
    // Normalize latitude and longitude to a 0-100 range
    const canvasX = ((lng + 180) % 360) / 3.6;
    const canvasY = (90 - lat) / 1.8;
    return { x: canvasX, y: canvasY };
  };

  const userCanvasPos = userLocation ? mapLocationToCanvas(userLocation.lat, userLocation.lng) : null;

  return (
    <div className="App">
      <header className="App-header">
        <h1>ApocalypsAI Cosmic Compass</h1>
        <p>Navigating the remnants of existence.</p>
      </header>
      <main>
        <div className="star-map-container">
          <div className="star-map">
            {celestialBodies.map(body => (
              <div
                key={body.id}
                className="celestial-body"
                style={{ left: `${body.x}%`, top: `${body.y}%` }}
                title={body.description}
              >
                <span className="body-name">{body.name}</span>
              </div>
            ))}
            {userCanvasPos && (
              <div
                className="user-location"
                style={{ left: `${userCanvasPos.x}%`, top: `${userCanvasPos.y}%` }}
                title={`Your Location: Lat ${userLocation.lat.toFixed(2)}, Lng ${userLocation.lng.toFixed(2)}`}
              >
                <div className="pulsing-ring"></div>
                <div className="location-pin">📍</div>
              </div>
            )}
          </div>
        </div>
        {error && <p className="error-message">{error}</p>}
        {!userLocation && !error && <p>Locating your position in the cosmos...</p>}
      </main>
    </div>
  );
}

export default App;
