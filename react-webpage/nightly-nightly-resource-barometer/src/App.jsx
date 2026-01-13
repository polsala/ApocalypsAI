import React, { useState } from 'react';
import './App.css';

function App() {
  const [water, setWater] = useState(50);
  const [food, setFood] = useState(50);
  const [ammo, setAmmo] = useState(50);

  const rating = Math.round((water + food + ammo) / 3);

  return (
    <div className="container">
      <h1>ð¡ï¸ Resource Barometer</h1>
      <div className="resource">
        <label>Water: {water}%</label>
        <input
          type="range"
          min="0"
          max="100"
          value={water}
          onChange={e => setWater(+e.target.value)}
        />
      </div>
      <div className="resource">
        <label>Food: {food}%</label>
        <input
          type="range"
          min="0"
          max="100"
          value={food}
          onChange={e => setFood(+e.target.value)}
        />
      </div>
      <div className="resource">
        <label>Ammo: {ammo}%</label>
        <input
          type="range"
          min="0"
          max="100"
          value={ammo}
          onChange={e => setAmmo(+e.target.value)}
        />
      </div>
      <h2>Survival Rating: {rating}%</h2>
    </div>
  );
}

export default App;
