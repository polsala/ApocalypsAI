import React, { useState, useCallback } from 'react';
import RippleCanvas from './RippleCanvas';

function App() {
  const [rippleCount, setRippleCount] = useState(5);
  const [rippleSpeed, setRippleSpeed] = useState(0.5); // Speed of expansion
  const [rippleDecay, setRippleDecay] = useState(0.01); // Rate of opacity decay
  const [colorScheme, setColorScheme] = useState('vibrant'); // Not fully implemented in canvas yet, but for future expansion

  const handleGenerateRipple = useCallback(() => {
    // In a real scenario, this would trigger a new ripple in RippleCanvas
    // For this simple setup, RippleCanvas manages its own ripple generation based on rippleCount
    // This button could be used to force a new ripple or reset the existing ones.
    // For now, it's a placeholder or could trigger a temporary increase in rippleCount.
    console.log("Generating a new ripple (logic handled by RippleCanvas's continuous generation)");
  }, []);

  return (
    <div className="app-container">
      <h1>Chronal Ripple Visualizer</h1>
      <div className="controls">
        <div className="control-group">
          <label htmlFor="rippleCount">Ripple Count: {rippleCount}</label>
          <input
            id="rippleCount"
            type="range"
            min="1"
            max="20"
            value={rippleCount}
            onChange={(e) => setRippleCount(Number(e.target.value))}
          />
        </div>

        <div className="control-group">
          <label htmlFor="rippleSpeed">Ripple Speed: {rippleSpeed.toFixed(2)}</label>
          <input
            id="rippleSpeed"
            type="range"
            min="0.1"
            max="2"
            step="0.05"
            value={rippleSpeed}
            onChange={(e) => setRippleSpeed(Number(e.target.value))}
          />
        </div>

        <div className="control-group">
          <label htmlFor="rippleDecay">Ripple Decay: {rippleDecay.toFixed(3)}</label>
          <input
            id="rippleDecay"
            type="range"
            min="0.001"
            max="0.05"
            step="0.001"
            value={rippleDecay}
            onChange={(e) => setRippleDecay(Number(e.target.value))}
          />
        </div>

        {/* <div className="control-group">
          <label htmlFor="colorScheme">Color Scheme:</label>
          <select
            id="colorScheme"
            value={colorScheme}
            onChange={(e) => setColorScheme(e.target.value)}
          >
            <option value="vibrant">Vibrant</option>
            <option value="monochromatic">Monochromatic</option>
            <option value="grayscale">Grayscale</option>
          </select>
        </div> */}
      </div>
      <button onClick={handleGenerateRipple}>Generate Ripple</button>
      <RippleCanvas
        rippleCount={rippleCount}
        rippleSpeed={rippleSpeed}
        rippleDecay={rippleDecay}
        colorScheme={colorScheme}
      />
    </div>
  );
}

export default App;
