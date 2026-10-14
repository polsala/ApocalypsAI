// src/App.js
import React, { useState, useEffect } from 'react';
import './App.css';
import { getRandomMood } from './moodData';

function App() {
  const [currentMood, setCurrentMood] = useState(null);

  useEffect(() => {
    // Set initial mood on component mount
    setCurrentMood(getRandomMood());
  }, []);

  const handleNewMood = () => {
    setCurrentMood(getRandomMood());
  };

  if (!currentMood) {
    return <div className="app-loading">Loading Mood...</div>;
  }

  return (
    <div className="App" style={{ backgroundColor: currentMood.color }}>
      <header className="App-header">
        <h1>Apocalypse Mood Ring</h1>
        <div className="mood-display">
          <span className="mood-icon">{currentMood.icon}</span>
          <h2 className="mood-name">{currentMood.name}</h2>
        </div>
        <p className="mood-insight">{currentMood.insight}</p>
        <button className="mood-button" onClick={handleNewMood}>
          Simulate New Mood
        </button>
        <p className="footer-note">
          *This is a simulated mood for whimsical purposes only. Do not base critical survival decisions on it.
        </p>
      </header>
    </div>
  );
}

export default App;
