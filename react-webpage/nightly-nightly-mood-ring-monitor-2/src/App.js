import React, { useState, useEffect } from 'react';
import MoodRing from './MoodRing';
import MoodDisplay from './MoodDisplay';
import './App.css';

// # Mock rationale: Simulates an asynchronous API call to fetch mood data,
// ensuring tests are deterministic and do not rely on external network requests
// or actual sentiment analysis.
const fetchMoodData = async () => {
  return new Promise(resolve => {
    setTimeout(() => {
      // Simulate different moods over time for demonstration
      const moods = [
        { value: 20, text: 'Chaotic Whirlwind' },
        { value: 50, text: 'Uncertain Shimmer' },
        { value: 80, text: 'Balanced Glow' },
        { value: 95, text: 'Serene Aura' },
        { value: 35, text: 'Turbulent Haze' }
      ];
      const randomIndex = Math.floor(Math.random() * moods.length);
      resolve(moods[randomIndex]);
    }, 1500); // Simulate network delay
  });
};

function App() {
  const [mood, setMood] = useState({ value: 0, text: 'Initializing...' });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const getMood = async () => {
      setLoading(true);
      const data = await fetchMoodData();
      setMood(data);
      setLoading(false);
    };

    getMood();
    // Refresh mood every 10 seconds for dynamic demo
    const intervalId = setInterval(getMood, 10000);

    return () => clearInterval(intervalId);
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>ApocalypsAI Mood Ring Monitor</h1>
        {loading ? (
          <p>Analyzing cosmic vibrations...</p>
        ) : (
          <>
            <MoodRing moodValue={mood.value} />
            <MoodDisplay moodText={mood.text} />
          </>
        )}
      </header>
    </div>
  );
);
}

export default App;
