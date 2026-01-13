import React, { useState } from 'react';

const gearMap = {
  desert: ['Sunshade Cloak', 'Cactus Water Filter', 'Sandstorm Goggles'],
  tundra: ['Thermal Fur Suit', 'Ice Pick', 'Snowshoe Boots'],
  urban: ['Crowbar', 'Flashlight', 'First Aid Kit'],
  forest: ['Camouflage Net', 'Mushroom Forager Kit', 'Bear Spray']
};

function App() {
  const [env, setEnv] = useState('');
  const [gear, setGear] = useState([]);

  const handleChange = (e) => {
    const selected = e.target.value;
    setEnv(selected);
    setGear(gearMap[selected] || []);
  };

  return (
    <div style={{ fontFamily: 'sans-serif', padding: '20px' }}>
      <h1>Apocalypse Survival Gear Recommender</h1>
      <label>
        Choose your environment: 
        <select data-testid="env-select" value={env} onChange={handleChange}>
          <option value="">--Select--</option>
          <option value="desert">Desert</option>
          <option value="tundra">Tundra</option>
          <option value="urban">Urban</option>
          <option value="forest">Forest</option>
        </select>
      </label>
      {gear.length > 0 && (
        <div data-testid="gear-list">
          <h2>Recommended Gear for {env.charAt(0).toUpperCase() + env.slice(1)}:</h2>
          <ul>
            {gear.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
