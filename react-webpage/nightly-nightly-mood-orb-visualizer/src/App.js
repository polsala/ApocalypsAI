import React, { useState, useEffect } from 'react';
import './App.css';
import MoodOrb from './MoodOrb';
import { getSimulatedMood } from './MoodDataService';

function App() {
  const [mood, setMood] = useState(0); // Mood from -100 to 100

  useEffect(() => {
    const fetchMood = () => {
      setMood(getSimulatedMood());
    };

    fetchMood(); // Initial fetch
    const intervalId = setInterval(fetchMood, 3000); // Update every 3 seconds

    return () => clearInterval(intervalId); // Cleanup on unmount
  }, []);

  const getMoodDescription = (currentMood) => {
    if (currentMood > 70) return "Radiant & Hopeful";
    if (currentMood > 30) return "Optimistic & Steady";
    if (currentMood > -30) return "Neutral & Observing";
    if (currentMood > -70) return "Wary & Reflective";
    return "Turbulent & Challenging";
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>ApocalypsAI Community Mood Orb</h1>
        <p>Current Pulse: {getMoodDescription(mood)} ({mood})</p>
        <MoodOrb mood={mood} />
      </header>
    </div>
  );
}

export default App;
