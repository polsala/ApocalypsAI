import React, { useState, useEffect } from 'react';
import './App.css';

// Mocking the Geolocation API for deterministic testing
const mockGeolocation = {
  getCurrentPosition: (success, error) => {
    // Default mock coordinates (e.g., a desolate wasteland)
    const mockCoords = {
      latitude: 34.0522,
      longitude: -118.2437,
      accuracy: 100
    };
    success({ coords: mockCoords });
  }
};

function App() {
  const [location, setLocation] = useState(null);
  const [error, setError] = useState(null);
  const [mapCenter, setMapCenter] = useState({ lat: 0, lng: 0 });
  const [zoomLevel, setZoomLevel] = useState(2);

  useEffect(() => {
    const geo = navigator.geolocation || mockGeolocation;

    geo.getCurrentPosition(
      (position) => {
        setLocation({
          lat: position.coords.latitude,
          lng: position.coords.longitude
        });
        setMapCenter({ lat: position.coords.latitude, lng: position.coords.longitude });
      },
      (err) => {
        setError(`Error Code ${err.code} - ${err.message}`);
      }
    );
  }, []);

  const handleMapPan = (deltaX, deltaY) => {
    // Simple panning logic - adjust mapCenter based on delta
    // In a real app, this would be more sophisticated, possibly tied to map projection
    const LAT_DEG_PER_PIXEL = 0.0001; // Approximate degrees per pixel at a given zoom
    const LNG_DEG_PER_PIXEL = 0.0002; // Approximate degrees per pixel at a given zoom

    setMapCenter(prevCenter => ({
      lat: prevCenter.lat - (deltaY * LAT_DEG_PER_PIXEL),
      lng: prevCenter.lng + (deltaX * LNG_DEG_PER_PIXEL)
    }));
  };

  const handleZoom = (direction) => {
    setZoomLevel(prevZoom => {
      const newZoom = direction === 'in' ? prevZoom + 0.5 : Math.max(1, prevZoom - 0.5);
      return newZoom;
    });
  };

  // Placeholder for star map rendering - in a real app, this would be a canvas or SVG
  const renderStarMap = () => {
    const stars = [];
    // Generate some random 'stars' based on map bounds and zoom
    // This is a very simplified representation
    const numStars = Math.floor(50 * zoomLevel);
    for (let i = 0; i < numStars; i++) {
      const starLat = mapCenter.lat + (Math.random() - 0.5) * (360 / zoomLevel);
      const starLng = mapCenter.lng + (Math.random() - 0.5) * (360 / zoomLevel);
      const starSize = Math.random() * 3 + 1;
      const starStyle = {
        position: 'absolute',
        left: `${((starLng - mapCenter.lng) * 10 + 50)}%`, // Simplified projection
        top: `${(-(starLat - mapCenter.lat) * 10 + 50)}%`, // Simplified projection
        width: `${starSize}px`,
        height: `${starSize}px`,
        backgroundColor: 'white',
        borderRadius: '50%',
        opacity: Math.random() * 0.7 + 0.3
      };
      stars.push(<div key={i} className="star" style={starStyle}></div>);
    }
    return stars;
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>ApocalypsAI Cosmic Compass</h1>
        <p>Navigating the remnants of civilization under a new sky.</p>
      </header>
      <main>
        <div className="map-container">
          <div className="star-map" style={{ transform: `scale(${zoomLevel})`, transformOrigin: 'center center' }}>
            {renderStarMap()}
            {location && (
              <div 
                className="location-pin"
                style={{
                  position: 'absolute',
                  left: '50%',
                  top: '50%',
                  transform: 'translate(-50%, -50%)',
                  backgroundColor: 'red',
                  width: '20px',
                  height: '20px',
                  borderRadius: '50%',
                  zIndex: 10
                }}
              ></div>
            )}
          </div>
          <div className="map-controls">
            <button onClick={() => handleZoom('in')}>+</button>
            <button onClick={() => handleZoom('out')}>-</button>
            <button onClick={() => handleMapPan(0, 100)}>⬆️</button>
            <button onClick={() => handleMapPan(0, -100)}>⬇️</button>
            <button onClick={() => handleMapPan(100, 0)}>➡️</button>
            <button onClick={() => handleMapPan(-100, 0)}>⬅️</button>
          </div>
        </div>
        <div className="info-panel">
          <h2>Current Coordinates</h2>
          {location ? (
            <p>Latitude: {location.lat.toFixed(6)}, Longitude: {location.lng.toFixed(6)}</p>
          ) : error ? (
            <p className="error">{error}</p>
          ) : (
            <p>Acquiring stellar bearings...</p>
          )}
          <p><em>The stars may have shifted, but your position is known.</em></p>
        </div>
      </main>
    </div>
  );
}

export default App;
