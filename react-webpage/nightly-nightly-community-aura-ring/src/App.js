import React, { useState, useEffect } from 'react';
import MoodRing from './MoodRing';
import { analyzeSentiment } from './SentimentAnalyzer';
import './App.css';

// Mock GitHub event data for demonstration
const mockEvents = [
  { id: 1, message: "Found a critical bug in the latest release, needs immediate attention." },
  { id: 2, message: "Working on a new feature for the temporal distortion stabilizer." },
  { id: 3, message: "Resolved the minor UI glitch, looking good now!" },
  { id: 4, message: "This new integration is awesome, great work everyone!" },
  { id: 5, message: "Reviewing PR #1234, seems mostly fine." },
  { id: 6, message: "Encountered an unexpected error during deployment." },
  { id: 7, message: "Adding support for new resource types in the wasteland tracker." },
  { id: 8, message: "The latest patch fixed the performance issue, fantastic!" },
  { id: 9, message: "Just a quick comment on the documentation update." },
  { id: 10, message: "Another bug report came in, investigating now." }
];

function App() {
  const [currentMood, setCurrentMood] = useState('Neutral');

  useEffect(() => {
    // In a real scenario, this would fetch data from an API
    const mood = analyzeSentiment(mockEvents.map(event => event.message));
    setCurrentMood(mood);
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>ApocalypsAI Community Aura Ring</h1>
      </header>
      <main className="App-main">
        <MoodRing mood={currentMood} />
        <p className="App-description">
          The current collective aura of ApocalypsAI is: <strong>{currentMood}</strong>.
          (Based on mocked recent activity.)
        </p>
      </main>
    </div>
  );
}

export default App;
