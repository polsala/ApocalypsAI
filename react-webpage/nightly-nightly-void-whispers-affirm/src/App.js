import React, { useState } from 'react';
import './App.css';

const affirmations = [
  "The void whispers: you are stronger than you believe.",
  "In chaos, find your center. In darkness, find your light.",
  "Every sunrise after the apocalypse is a victory.",
  "Your resilience echoes through the wasteland.",
  "Even scattered stars can guide you home.",
  "The ruins are not an end, but a new beginning.",
  "Adaptation is the highest form of hope.",
  "The silence speaks louder than the storm.",
  "You are the author of your survival story.",
  "In the void, your courage creates light."
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
        <h1>.Void Whispers.</h1>
        <div className="affirmation-box">
          <p className="affirmation-text">{currentAffirmation}</p>
        </div>
        <button className="whisper-button" onClick={generateAffirmation}>
          Whisper Another Truth
        </button>
        <p className="footer-note">In the silence between heartbeats, you are infinite.</p>
      </header>
    </div>
  );
}

export default App;
