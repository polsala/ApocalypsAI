import React, { useState } from 'react';
import './App.css';

function App() {
  const [cosmicDust, setCosmicDust] = useState(5);
  const [starlightIntensity, setStarlightIntensity] = useState(5);
  const [path, setPath] = useState([]);

  const generatePath = () => {
    const newPath = [];
    let currentX = 100;
    let currentY = 100;
    const steps = 50;
    const dustFactor = (11 - cosmicDust) * 5; // Higher dust = more erratic
    const lightFactor = (11 - starlightIntensity) * 3; // Higher light = straighter

    for (let i = 0; i < steps; i++) {
      newPath.push({ x: currentX, y: currentY });

      // Determine direction changes based on inputs
      let dx = Math.random() * dustFactor - dustFactor / 2;
      let dy = Math.random() * dustFactor - dustFactor / 2;

      // Adjust for starlight intensity (tend towards straight line)
      if (Math.random() < starlightIntensity / 10) {
        const angle = Math.atan2(dy, dx);
        dx = Math.cos(angle) * lightFactor;
        dy = Math.sin(angle) * lightFactor;
      }

      currentX += dx;
      currentY += dy;

      // Keep within bounds (simplified)
      currentX = Math.max(0, Math.min(500, currentX));
      currentY = Math.max(0, Math.min(500, currentY));
    }
    setPath(newPath);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Nightly Cosmic Compass</h1>
        <p>Chart your course through the celestial unknown!</p>
      </header>
      <main>
        <div className="controls">
          <label>
            Cosmic Dust:
            <input
              type="range"
              min="1"
              max="10"
              value={cosmicDust}
              onChange={(e) => setCosmicDust(parseInt(e.target.value))}
            />
            {cosmicDust}
          </label>
          <label>
            Starlight Intensity:
            <input
              type="range"
              min="1"
              max="10"
              value={starlightIntensity}
              onChange={(e) => setStarlightIntensity(parseInt(e.target.value))}
            />
            {starlightIntensity}
          </label>
          <button onClick={generatePath}>Chart Course</button>
        </div>
        <div className="visualization-container">
          <svg width="500" height="500" viewBox="0 0 500 500" style={{ border: '1px solid #ccc' }}>
            {path.length > 0 && (
              <polyline
                points={path.map(p => `${p.x},${p.y}`).join(' ')}
                fill="none"
                stroke="#00ff00"
                strokeWidth="2"
              />
            )}
            {/* Add a starting point marker */}
            <circle cx="100" cy="100" r="5" fill="yellow" />
          </svg>
        </div>
      </main>
    </div>
  );
}

export default App;
