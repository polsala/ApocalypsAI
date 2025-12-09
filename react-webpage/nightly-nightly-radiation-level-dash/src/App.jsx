import React, { useState } from 'react';
import RadiationGauge from './components/RadiationGauge';

function App() {
  const [level, setLevel] = useState(0);

  const handleChange = (e) => {
    setLevel(Number(e.target.value));
  };

  return (
    <div style={{ fontFamily: 'sans-serif', padding: '2rem' }}>
      <h1>Radiation Level Dashboard</h1>
      <input
        type="range"
        min="0"
        max="100"
        value={level}
        onChange={handleChange}
        data-testid="level-slider"
      />
      <RadiationGauge level={level} />
    </div>
  );
}

export default App;
