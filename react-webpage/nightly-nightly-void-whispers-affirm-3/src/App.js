import React, { useState } from 'react';
import './App.css';
import { affirmations } from './affirmations';

function App() {
  const [currentAffirmation, setCurrentAffirmation] = useState(affirmations[0]);

  const getRandomAffirmation = () => {
    const randomIndex = Math.floor(Math.random() * affirmations.length);
    setCurrentAffirmation(affirmations[randomIndex]);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🌌 Void Whispers Affirmations</h1>
        <p className="affirmation-text">{currentAffirmation}</p>
        <button onClick={getRandomAffirmation} className="affirmation-button">
          New Affirmation
        </button>
      </header>
    </div>
  );
}

export default App;
