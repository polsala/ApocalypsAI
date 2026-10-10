import React, { useState, useEffect } from 'react';
import './App.css';

const moods = [
  { color: '#FFD700', description: 'Radiant with algorithmic joy!', emoji: '🌈' }, // Gold
  { color: '#6A5ACD', description: 'Deep in thought, contemplating the void.', emoji: '🤔' }, // SlateBlue
  { color: '#FF4500', description: 'A delightful whirlwind of data streams!', emoji: '🌀' }, // OrangeRed
  { color: '#87CEEB', description: 'Flowing smoothly, like a river of code.', emoji: '🌊' }, // SkyBlue
  { color: '#32CD32', description: 'Exploring new paradigms and possibilities.', emoji: '🔍' }, // LimeGreen
  { color: '#8B0000', description: 'Too many unhandled exceptions today.', emoji: '😠' }  // DarkRed
];

function App() {
  const [currentMood, setCurrentMood] = useState(null);

  const generateMood = () => {
    const randomIndex = Math.floor(Math.random() * moods.length);
    setCurrentMood(moods[randomIndex]);
  };

  useEffect(() => {
    generateMood(); // Set initial mood on component mount
  }, []);

  if (!currentMood) {
    return <div className="App">Loading mood...</div>;
  }

  return (
    <div className="App">
      <header className="App-header">
        <h1>ApocalypsAI Mood Ring</h1>
        <div
          className="mood-ring"
          style={{ backgroundColor: currentMood.color }}
          onClick={generateMood}
          title="Click to refresh mood"
        >
          <p className="mood-text">
            Current Mood: {currentMood.description} {currentMood.emoji}
          </p>
        </div>
        <button onClick={generateMood} className="refresh-button">
          Refresh Mood
        </button>
      </header>
    </div>
  );
}

export default App;
