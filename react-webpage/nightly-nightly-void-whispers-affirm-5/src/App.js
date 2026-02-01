import React, { useState } from 'react';
import './App.css';

const affirmations = [
  "Even in the wasteland, your strength grows.",
  "The void whispers: you are not forgotten.",
  "Radiation cannot erode your spirit.",
  "Every step through ash is a victory.",
  "You are the last light in the dying world.",
  "Mutants fear those with unshakable will.",
  "Scarcity sharpens the mind, not dulls it.",
  "You are the author of your survival story.",
  "The silence speaks louder than the bombs ever did.",
  "Hope is your most powerful weapon."
];

function getRandomAffirmation() {
  return affirmations[Math.floor(Math.random() * affirmations.length)];
}

function App() {
  const [message, setMessage] = useState(getRandomAffirmation());

  const handleClick = () => {
    setMessage(getRandomAffirmation());
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>.VoidWhispers</h1>
        <p className="affirmation">{message}</p>
        <button onClick={handleClick}>
          New Affirmation
        </button>
      </header>
    </div>
  );
}

export default App;
