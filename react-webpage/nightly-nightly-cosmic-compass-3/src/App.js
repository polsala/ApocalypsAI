import React, { useState, useEffect } from 'react';
import './App.css';

// Mock data for celestial map and advice
const mockCelestialData = {
  stars: [
    { id: 1, name: 'Sirius', x: 100, y: 150 },
    { id: 2, name: 'Vega', x: 300, y: 200 },
    { id: 3, name: 'Polaris', x: 500, y: 100 },
  ],
  constellations: [
    { id: 1, name: 'Orion', points: [[100, 150], [300, 200], [500, 100]] },
  ]
};

const mockCosmicAdvice = [
  "The stars align for a moment of quiet contemplation.",
  "A gentle breeze whispers secrets of the cosmos; listen closely.",
  "Your path is illuminated by the faint glow of distant nebulae.",
  "Embrace the unknown, for it holds the greatest wonders.",
  "The universe is vast, and so is your potential."
];

function App() {
  const [location, setLocation] = useState(null);
  const [advice, setAdvice] = useState('');
  const [error, setError] = useState('');

  const getLocation = () => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setLocation({
            lat: position.coords.latitude,
            lng: position.coords.longitude
          });
          setError('');
          generateAdvice(); // Generate advice once location is found
        },
        (err) => {
          setError(`Error getting location: ${err.message}`);
          setLocation(null);
          setAdvice('');
        }
      );
    } else {
      setError('Geolocation is not supported by this browser.');
      setLocation(null);
      setAdvice('');
    }
  };

  const generateAdvice = () => {
    if (mockCosmicAdvice.length > 0) {
      const randomIndex = Math.floor(Math.random() * mockCosmicAdvice.length);
      setAdvice(mockCosmicAdvice[randomIndex]);
    } else {
      setAdvice("No cosmic wisdom available at this moment.");
    }
  };

  useEffect(() => {
    getLocation();
  }, []);

  // Simple function to map lat/lng to a position on the celestial map (highly simplified)
  // In a real app, this would involve complex projections or a dedicated map library.
  const getMapCoordinates = (lat, lng) => {
    // This is a placeholder. Real mapping would be complex.
    // For demonstration, we'll just use a simple scaling based on typical lat/lng ranges.
    const scaleLat = (lat + 90) / 180; // 0 to 1
    const scaleLng = (lng + 180) / 360; // 0 to 1
    return { x: scaleLng * 800, y: (1 - scaleLat) * 600 }; // Assuming a 800x600 map
  };

  const userMapPos = location ? getMapCoordinates(location.lat, location.lng) : null;

  return (
    <div className="App">
      <header className="App-header">
        <h1>Cosmic Compass</h1>
        <p>Your guide through the celestial unknown.</p>
      </header>
      <main>
        <div className="celestial-map-container">
          <svg width="800" height="600" viewBox="0 0 800 600" className="celestial-map">
            {/* Background and celestial elements */}
            <defs>
              <radialGradient id="skyGradient">
                <stop offset="0%" stopColor="#0a0a2a" />
                <stop offset="100%" stopColor="#1a1a4a" />
              </radialGradient>
            </defs>
            <rect width="100%" height="100%" fill="url(#skyGradient)" />

            {/* Stars */}
            {mockCelestialData.stars.map(star => (
              <circle key={star.id} cx={star.x} cy={star.y} r="3" fill="#ffffff" />
            ))}

            {/* Constellations */}
            {mockCelestialData.constellations.map(constellation => (
              <polyline 
                key={constellation.id}
                points={constellation.points.map(p => p.join(',')).join(' ')}
                fill="none" 
                stroke="rgba(255,255,255,0.5)" 
                strokeWidth="1" 
              />
            ))}

            {/* User Location Marker */}
            {userMapPos && (
              <g>
                <circle cx={userMapPos.x} cy={userMapPos.y} r="10" fill="#ff0000" />
                <circle cx={userMapPos.x} cy={userMapPos.y} r="15" fill="#ff0000" fillOpacity="0.3" />
                <text x={userMapPos.x + 20} y={userMapPos.y} fill="#ffffff" fontSize="14">You Are Here</text>
              </g>
            )}
          </svg>
        </div>

        <div className="advice-section">
          <h2>Cosmic Wisdom</h2>
          {error && <p className="error">{error}</p>}
          {advice && <p>"{advice}"</p>}
          <button onClick={generateAdvice} disabled={!location}>Seek New Wisdom</button>
        </div>
      </main>
    </div>
  );
}

export default App;
