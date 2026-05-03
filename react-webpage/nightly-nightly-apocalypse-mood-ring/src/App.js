import React, { useState, useEffect } from 'react';
import './App.css';

const moods = [
  { name: 'Serene Void', color: '#2196F3', description: 'A state of calm acceptance, perhaps even peace amidst the desolation. The community is stable and reflective.' },
  { name: 'Whispering Hope', color: '#4CAF50', description: 'Signs of growth, optimism, and resilience. New ideas are budding, and spirits are lifting.' },
  { name: 'Anxious Static', color: '#FFEB3B', description: 'A sense of unease, caution, or low-level stress. The community is vigilant, perhaps anticipating change or minor threats.' },
  { name: 'Temporal Flux', color: '#FF9800', description: 'Unpredictability and rapid shifts. Things are in motion, and adaptability is key. Could indicate minor temporal anomalies or rapid environmental changes.' },
  { name: 'Despair\'s Embrace', color: '#D32F2F', description: 'Low morale, distress, or significant challenges. The community might be struggling with resource scarcity, illness, or existential dread.' },
  { name: 'Chaotic Spark', color: '#9C27B0', description: 'High energy, unpredictable, and potentially volatile. This could be a precursor to innovation or conflict, a period of intense activity.' }
];

function App() {
  const [currentMood, setCurrentMood] = useState(moods[0]);

  const getRandomMood = () => {
    const randomIndex = Math.floor(Math.random() * moods.length);
    return moods[randomIndex];
  };

  const simulateNewMood = () => {
    setCurrentMood(getRandomMood());
  };

  useEffect(() => {
    // Optional: Set a default mood or fetch initial data
  }, []);

  return (
    <div className="App" style={{ '--mood-color': currentMood.color }}>
      <header className="App-header">
        <h1>Apocalypse Mood Ring</h1>
        <div className="mood-ring" style={{ backgroundColor: currentMood.color }}>
          <p className="mood-name">{currentMood.name}</p>
        </div>
        <p className="mood-description">{currentMood.description}</p>
        <button className="mood-button" onClick={simulateNewMood}>
          Simulate New Mood
        </button>
      </header>
    </div>
  );
}

export default App;
