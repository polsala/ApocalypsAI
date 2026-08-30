import React, { useState, useEffect } from 'react';
import './App.css';

// Mock celestial data generator for deterministic results
const generateCosmicAlignment = (seed) => {
  const random = (min, max) => {
    const x = Math.sin(seed++) * 10000;
    return min + (x - Math.floor(x)) * (max - min);
  };

  const alignment = {
    starColor: `hsl(${random(0, 360)}, 70%, 60%)`,
    planetColor: `hsl(${random(0, 360)}, 80%, 50%)`,
    nebulaColor: `hsl(${random(0, 360)}, 50%, 70%)`,
    starSize: random(5, 20),
    planetOrbit: random(50, 150),
    nebulaRadius: random(100, 250),
    message: "Your cosmic alignment is shimmering with potential!"
  };

  // Add some whimsical variations based on seed
  if (seed % 5 === 0) {
    alignment.message = "A celestial dance of joy awaits you!";
    alignment.starSize *= 1.2;
  } else if (seed % 3 === 0) {
    alignment.message = "The stars whisper secrets of wonder.";
    alignment.planetColor = `hsl(${random(0, 360)}, 90%, 40%)`;
  }

  return alignment;
};

function App() {
  const [alignment, setAlignment] = useState({});
  const [seed, setSeed] = useState(12345); // Fixed seed for deterministic output

  useEffect(() => {
    setAlignment(generateCosmicAlignment(seed));
  }, [seed]);

  return (
    <div className="App">
      <header className="App-header">
        <h1>The Cosmic Compass</h1>
        <p>Your daily celestial alignment, interpreted with whimsy.</p>
      </header>
      <main>
        <div className="cosmic-visualization">
          <div className="nebula" style={{ backgroundColor: alignment.nebulaColor, width: `${alignment.nebulaRadius}px`, height: `${alignment.nebulaRadius}px` }}></div>
          <div className="star-field">
            {[...Array(10)].map((_, i) => (
              <div key={i} className="star"
                   style={{
                     top: `${Math.random() * 100}%`,
                     left: `${Math.random() * 100}%`,
                     width: `${alignment.starSize}px`,
                     height: `${alignment.starSize}px`,
                     backgroundColor: alignment.starColor
                   }}></div>
            ))}
          </div>
          <div className="planet-orbit" style={{ width: `${alignment.planetOrbit * 2}px`, height: `${alignment.planetOrbit * 2}px` }}>
            <div className="planet" style={{ backgroundColor: alignment.planetColor }}></div>
          </div>
        </div>
        <div className="alignment-message">
          <p>{alignment.message}</p>
        </div>
      </main>
    </div>
  );
}

export default App;
