import React, { useState, useEffect } from 'react';
import './App.css';

// Helper function to convert HSL to Hex
function hslToHex(h, s, l) {
  l /= 100;
  const a = s * Math.min(l, 1 - l) / 100;
  const f = n => {
    const k = (n + h / 30) % 12;
    const color = l - a * Math.max(Math.min(k - 3, 9 - k, 1), -1);
    return Math.round(255 * color).toString(16).padStart(2, '0');
  };
  return `#${f(0)}${f(8)}${f(4)}`;
}

// Deterministic color palette generation based on mood
const generatePalette = (mood) => {
  let baseH, baseS, baseL;
  const colors = [];

  switch (mood) {
    case 'Despair':
      baseH = 220; baseS = 30; baseL = 20; // Muted blue-grey
      colors.push(hslToHex(baseH, baseS, baseL));
      colors.push(hslToHex(baseH + 10, baseS - 10, baseL + 10));
      colors.push(hslToHex(baseH - 10, baseS + 10, baseL - 5));
      colors.push(hslToHex(baseH + 5, baseS - 5, baseL + 20));
      colors.push(hslToHex(baseH - 5, baseS + 5, baseL - 10));
      break;
    case 'Hope':
      baseH = 100; baseS = 70; baseL = 60; // Vibrant green
      colors.push(hslToHex(baseH, baseS, baseL));
      colors.push(hslToHex(baseH + 20, baseS + 10, baseL + 5));
      colors.push(hslToHex(baseH - 10, baseS - 10, baseL - 5));
      colors.push(hslToHex(baseH + 5, baseS + 5, baseL + 10));
      colors.push(hslToHex(baseH - 5, baseS - 5, baseL - 10));
      break;
    case 'Scrappy':
      baseH = 30; baseS = 60; baseL = 40; // Earthy orange/brown
      colors.push(hslToHex(baseH, baseS, baseL));
      colors.push(hslToHex(baseH + 15, baseS - 10, baseL + 10));
      colors.push(hslToHex(baseH - 10, baseS + 5, baseL - 5));
      colors.push(hslToHex(baseH + 5, baseS - 5, baseL + 15));
      colors.push(hslToHex(baseH - 5, baseS + 10, baseL - 10));
      break;
    case 'Serene':
      baseH = 190; baseS = 40; baseL = 70; // Soft blue
      colors.push(hslToHex(baseH, baseS, baseL));
      colors.push(hslToHex(baseH + 10, baseS - 10, baseL + 5));
      colors.push(hslToHex(baseH - 5, baseS + 5, baseL - 5));
      colors.push(hslToHex(baseH + 5, baseS - 5, baseL + 10));
      colors.push(hslToHex(baseH - 10, baseS + 10, baseL - 10));
      break;
    case 'Mysterious':
      baseH = 270; baseS = 50; baseL = 30; // Deep purple
      colors.push(hslToHex(baseH, baseS, baseL));
      colors.push(hslToHex(baseH + 20, baseS + 10, baseL + 5));
      colors.push(hslToHex(baseH - 10, baseS - 10, baseL - 5));
      colors.push(hslToHex(baseH + 5, baseS + 5, baseL + 10));
      colors.push(hslToHex(baseH - 5, baseS - 5, baseL - 10));
      break;
    default: // Default to 'Scrappy' if an unknown mood is somehow selected
      return generatePalette('Scrappy');
  }
  return colors;
};

function App() {
  const [selectedMood, setSelectedMood] = useState('Scrappy');
  const [palette, setPalette] = useState([]);

  useEffect(() => {
    setPalette(generatePalette(selectedMood));
  }, [selectedMood]);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Nightly Lumina-Loom</h1>
        <p>Weaving colors from the threads of emotion.</p>
      </header>
      <main>
        <div className="mood-selector">
          <label htmlFor="mood-select">Choose your current vibe:</label>
          <select
            id="mood-select"
            value={selectedMood}
            onChange={(e) => setSelectedMood(e.target.value)}
          >
            <option value="Despair">Despair</option>
            <option value="Hope">Hope</option>
            <option value="Scrappy">Scrappy</option>
            <option value="Serene">Serene</option>
            <option value="Mysterious">Mysterious</option>
          </select>
        </div>
        <div className="palette-display">
          {palette.map((color, index) => (
            <div key={index} className="color-swatch" style={{ backgroundColor: color }}>
              <span className="hex-code">{color}</span>
            </div>
          ))}
        </div>
      </main>
    </div>
  );
}

export default App;
