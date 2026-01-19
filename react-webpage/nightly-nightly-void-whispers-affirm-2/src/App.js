import React, { useState } from 'react';
import './App.css';

const affirmations = [
  "Even in the void, your light persists.",
  "The wasteland shapes you, but does not define you.",
  "Every sunrise is a victory over the night.",
  "You are the ember that refuses to die.",
  "Chaos may reign, but so do you.",
  "In silence, you hear the whispers of hope.",
  "You are not lost — you are finding your way.",
  "The ruins are not an end, but a beginning.",
  "Your strength is forged in the fire of survival.",
  "Even echoes can carry love."
];

function App() {
  const [currentAffirmation, setCurrentAffirmation] = useState(affirmations[0]);

  const generateAffirmation = () => {
    const randomIndex = Math.floor(Math.random() * affirmations.length);
    setCurrentAffirmation(affirmations[randomIndex]);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>.Void Whispers</h1>
        <p className="affirmation-text">{currentAffirmation}</p>
        <button className="generate-btn" onClick={generateAffirmation}>
          New Affirmation
        </button>
      </header>
    </div>
  );
}

export default App;
