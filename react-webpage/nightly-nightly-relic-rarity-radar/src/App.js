import React, { useState } from 'react';
import { assignRarity } from './utils/rarityLogic';
import './App.css';

function App() {
  const [itemName, setItemName] = useState('');
  const [relics, setRelics] = useState([]);

  const handleAnalyze = () => {
    if (itemName.trim() === '') return;
    const rarity = assignRarity(itemName);
    setRelics([{ name: itemName, rarity: rarity }, ...relics]);
    setItemName('');
  };

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      handleAnalyze();
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Nightly Relic Rarity Radar</h1>
        <p>Uncover the true value of your wasteland finds!</p>
      </header>
      <main className="App-main">
        <div className="input-section">
          <input
            type="text"
            value={itemName}
            onChange={(e) => setItemName(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Enter item name (e.g., 'Glow-in-the-dark Bolt', 'Temporal Shard')"
            aria-label="Item Name"
          />
          <button onClick={handleAnalyze}>Analyze Relic</button>
        </div>
        <div className="relic-list">
          <h2>Scavenged Relics</h2>
          {relics.length === 0 ? (
            <p>No relics analyzed yet. Start scanning!</p>
          ) : (
            <ul>
              {relics.map((relic, index) => (
                <li key={index} style={{ borderColor: relic.rarity.color }}>
                  <span className="relic-icon" role="img" aria-label="rarity icon">{relic.rarity.icon}</span>
                  <span className="relic-name">{relic.name}</span>
                  <span className="relic-rarity" style={{ color: relic.rarity.color }}>
                    {relic.rarity.level}
                  </span>
                </li>
              ))}
            </ul>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
