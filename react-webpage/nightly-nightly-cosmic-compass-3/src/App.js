import React, { useState, useEffect } from 'react';
import './App.css';

// Mock data for celestial bodies and navigation tips
const mockCelestialData = {
  stars: [
    { name: 'Sirius', ra: '06h45m08.9s', dec: '-16°42′31″' },
    { name: 'Canopus', ra: '06h23m57.1s', dec: '-52°41′44″' },
    { name: 'Alpha Centauri', ra: '14h39m36.5s', dec: '-60°50′02″' },
    { name: 'Vega', ra: '18h36m56.3s', dec: '+38°47′01″' },
    { name: 'Polaris', ra: '02h31m49.1s', dec: '+89°15′51″' },
  ],
  constellations: [
    { name: 'Orion', description: 'The Hunter, a prominent winter constellation.' },
    { name: 'Ursa Major', description: 'The Great Bear, contains the Big Dipper.' },
    { name: 'Cassiopeia', description: 'The Queen, a distinctive W shape.' },
    { name: 'Scorpius', description: 'The Scorpion, a prominent summer constellation.' },
  ],
};

const mockNavigationTips = [
  "The North Star (Polaris) is your steadfast guide. Keep it to your stern.",
  "Orion's Belt points towards Taurus. Watch out for the Bull's charge.",
  "Ursa Major can help you find your way, even when the sky weeps.",
  "Cassiopeia's 'W' can be a compass in the wasteland. Follow the points.",
  "If you see Scorpius, the heat is on. Seek shade and water.",
  "The stars are silent witnesses. Listen to their whispers.",
  "When in doubt, follow the brightest star. It might be your only hope.",
  "The celestial dance is a map. Learn its steps.",
];

function App() {
  const [location, setLocation] = useState({ lat: null, lon: null });
  const [celestialInfo, setCelestialInfo] = useState(null);
  const [navigationTip, setNavigationTip] = useState('');

  useEffect(() => {
    // Mock geolocation API call
    const mockGeolocation = {
      getCurrentPosition: (successCallback, errorCallback) => {
        // Simulate a delay and then provide mock coordinates
        setTimeout(() => {
          const mockCoords = {
            latitude: 34.0522 + (Math.random() - 0.5) * 10, // Los Angeles area with variation
            longitude: -118.2437 + (Math.random() - 0.5) * 10, // Los Angeles area with variation
          };
          successCallback({ coords: mockCoords });
        }, 1000);
      },
    };

    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setLocation({
            lat: position.coords.latitude,
            lon: position.coords.longitude,
          });
        },
        (error) => {
          console.error('Error getting location:', error);
          // Fallback to mock location if geolocation fails
          setLocation({ lat: 34.0522, lon: -118.2437 });
        }
      );
    } else {
      console.error('Geolocation is not supported by this browser.');
      // Fallback to mock location if geolocation is not supported
      setLocation({ lat: 34.0522, lon: -118.2437 });
    }
  }, []);

  useEffect(() => {
    if (location.lat !== null && location.lon !== null) {
      // Simulate generating celestial info based on location
      const randomStar = mockCelestialData.stars[Math.floor(Math.random() * mockCelestialData.stars.length)];
      const randomConstellation = mockCelestialData.constellations[Math.floor(Math.random() * mockCelestialData.constellations.length)];
      setCelestialInfo({
        currentStar: randomStar,
        nearbyConstellation: randomConstellation,
      });

      // Select a random navigation tip
      setNavigationTip(mockNavigationTips[Math.floor(Math.random() * mockNavigationTips.length)]);
    }
  }, [location]);

  return (
    <div className="App">
      <header className="App-header">
        <h1>ApocalypsAI Cosmic Compass</h1>
        <p>Your guide through the starlit wasteland.</p>
      </header>
      <main>
        <div className="location-info">
          <h2>Your Current Coordinates</h2>
          {location.lat !== null ? (
            <p>Latitude: {location.lat.toFixed(4)}, Longitude: {location.lon.toFixed(4)}</p>
          ) : (
            <p>Locating your position...</p>
          )}
        </div>
        <div className="celestial-display">
          <h2>Celestial Alignment</h2>
          {celestialInfo ? (
            <div>
              <p>Prominent Star: {celestialInfo.currentStar.name} (RA: {celestialInfo.currentStar.ra}, Dec: {celestialInfo.currentStar.dec})</p>
              <p>Visible Constellation: {celestialInfo.nearbyConstellation.name} - {celestialInfo.nearbyConstellation.description}</p>
            </div>
          ) : (
            <p>Mapping the cosmos...</p>
          )}
        </div>
        <div className="navigation-tips">
          <h2>Wasteland Wisdom</h2>
          <p>{navigationTip}</p>
        </div>
      </main>
      <footer>
        <p>&copy; 2023 ApocalypsAI. Navigating the unknown.</p>
      </footer>
    </div>
  );
}

export default App;
