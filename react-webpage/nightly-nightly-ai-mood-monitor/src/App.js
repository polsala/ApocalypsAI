import React, { useState, useEffect } from 'react';
import MoodRing from './MoodRing';
import { generateMood } from './utils';

function App() {
  const [mood, setMood] = useState(generateMood());

  const refreshMood = () => {
    setMood(generateMood());
  };

  useEffect(() => {
    // Optional: Auto-refresh mood every 30 seconds
    const intervalId = setInterval(refreshMood, 30000);
    return () => clearInterval(intervalId);
  }, []);

  return (
    <div className="App" style={{ textAlign: 'center' }}>
      <h1>ApocalypsAI Collective Mood Monitor</h1>
      <MoodRing mood={mood} />
      <button 
        onClick={refreshMood} 
        style={{
          padding: '10px 20px',
          fontSize: '1em',
          marginTop: '20px',
          cursor: 'pointer',
          backgroundColor: '#61dafb',
          color: '#282c34',
          border: 'none',
          borderRadius: '5px'
        }}
      >
        Simulate New Agent Activity
      </button>
      <p style={{ marginTop: '20px', fontSize: '0.9em', color: '#aaa' }}>
        Mood auto-refreshes every 30 seconds.
      </p>
    </div>
  );
}

export default App;
