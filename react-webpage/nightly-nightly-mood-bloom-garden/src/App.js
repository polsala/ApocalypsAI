import React, { useState, useEffect } from 'react';
import './App.css';
import MoodInput from './components/MoodInput';
import BloomGarden from './components/BloomGarden';

function App() {
  const [moodLevel, setMoodLevel] = useState(5); // Initial mood level
  const [gardenBlooms, setGardenBlooms] = useState([]);

  // Function to generate a bloom based on moodLevel
  const generateBloom = (level) => {
    const size = 20 + (level * 5); // Size from 25 to 70
    const hue = 120 - (level * 10); // Green (120) to Red (20)
    const saturation = 50 + (level * 5); // Saturation from 55 to 100
    const lightness = 50 + (level * 2); // Lightness from 52 to 70
    const color = `hsl(${hue}, ${saturation}%, ${lightness}%)`;
    const rotation = Math.random() * 360;
    const delay = Math.random() * 2; // Animation delay

    return {
      id: Date.now() + Math.random(), // Unique ID
      size,
      color,
      rotation,
      delay,
      x: Math.random() * 80 + 10, // Position between 10% and 90%
      y: Math.random() * 80 + 10,
    };
  };

  // Effect to initialize or update blooms when moodLevel changes
  useEffect(() => {
    // For simplicity, let's regenerate a few blooms based on the current mood
    // In a more complex app, we might update existing blooms or add/remove them
    const newBlooms = Array.from({ length: 3 + Math.floor(moodLevel / 3) }).map(() => generateBloom(moodLevel));
    setGardenBlooms(newBlooms);
  }, [moodLevel]); // Re-run when moodLevel changes

  const handleMoodChange = (newLevel) => {
    setMoodLevel(newLevel);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Nightly Mood Bloom Garden</h1>
      </header>
      <main className="App-main">
        <MoodInput currentMood={moodLevel} onMoodChange={handleMoodChange} />
        <BloomGarden blooms={gardenBlooms} />
      </main>
    </div>
  );
}

export default App;
