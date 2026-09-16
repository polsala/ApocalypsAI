import React, { useState, useEffect } from 'react';
import MoodRing from './MoodRing';
import './App.css';

const MOOD_TYPES = [
  { status: 'Stable', color: '#4CAF50', animationClass: 'calm' }, // Green
  { status: 'Fluctuating', color: '#FFC107', animationClass: 'pulse' }, // Yellow
  { status: 'Anomalous', color: '#F44336', animationClass: 'glitch' }, // Red
  { status: 'Unknown', color: '#9E9E9E', animationClass: 'static' }  // Grey
];

const COMPONENT_NAMES = [
  'Temporal Stability',
  'Agent Activity',
  'Resource Flux',
  'Void Echoes',
  'Reality Weave'
];

const generateRandomMood = (id) => {
  const randomComponentNameIndex = Math.floor(Math.random() * COMPONENT_NAMES.length);
  const randomMoodTypeIndex = Math.floor(Math.random() * MOOD_TYPES.length);
  return {
    id: id,
    name: COMPONENT_NAMES[randomComponentNameIndex],
    ...MOOD_TYPES[randomMoodTypeIndex]
  };
};

function App() {
  const [moods, setMoods] = useState([]);

  useEffect(() => {
    // Initialize with some moods
    const initialMoods = Array.from({ length: 3 }).map((_, i) => generateRandomMood(i));
    setMoods(initialMoods);
  }, []);

  const refreshMoods = () => {
    const newMoods = Array.from({ length: 3 }).map((_, i) => generateRandomMood(i));
    setMoods(newMoods);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Nightly Multiverse Mood Ring</h1>
        <p>Gauging the cosmic vibes of ApocalypsAI operations.</p>
      </header>
      <div className="mood-rings-container">
        {moods.map((mood) => (
          <MoodRing
            key={mood.id}
            name={mood.name}
            status={mood.status}
            color={mood.color}
            animationClass={mood.animationClass}
          />
        ))}
      </div>
      <button className="refresh-button" onClick={refreshMoods}>
        Refresh Multiverse Vibes
      </button>
    </div>
  );
}

export default App;
