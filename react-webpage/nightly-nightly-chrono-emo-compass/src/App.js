import React, { useState, useEffect } from 'react';
import MoodChart from './components/MoodChart';
import mockMoodData from './data/mockMoodData'; // # Mock rationale: Using mock data for deterministic, offline utility execution.
import './App.css';

function App() {
  const [moodData, setMoodData] = useState([]);

  useEffect(() => {
    // In a real application, this would fetch data from an API.
    // For this self-contained utility, we load mock data directly.
    setMoodData(mockMoodData);
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Nightly Chrono-Emotional Compass</h1>
        <p>Visualizing the ApocalypsAI Community's Vibe</p>
      </header>
      <main>
        {moodData.length > 0 ? (
          <MoodChart data={moodData} />
        ) : (
          <p>Loading emotional frequencies...</p>
        )}
      </main>
      <footer>
        <p>Data is simulated for demonstration purposes.</p>
      </footer>
    </div>
  );
}

export default App;
