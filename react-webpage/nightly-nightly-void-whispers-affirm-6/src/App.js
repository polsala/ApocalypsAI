import React, { useState, useEffect } from 'react';
import './App.css';

const affirmations = [
  "The stars align in your favor today.",
  "Your potential is as vast as the cosmos.",
  "Embrace the unknown; it holds wonders.",
  "You are a beacon of light in the void.",
  "The universe whispers its secrets to you."
];

function App() {
  const [affirmation, setAffirmation] = useState("");

  useEffect(() => {
    setAffirmation(getRandomAffirmation());
  }, []);

  const getRandomAffirmation = () => {
    return affirmations[Math.floor(Math.random() * affirmations.length)];
  };

  const handleClick = () => {
    setAffirmation(getRandomAffirmation());
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>.Void Whispers</h1>
        <p className="affirmation">{affirmation}</p>
        <button onClick={handleClick}>
          Receive Another Whisper
        </button>
      </header>
    </div>
  );
}

export default App;
