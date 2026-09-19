import React, { useState, useEffect } from 'react';
import MoodRing from './MoodRing';
import { analyzeUtility } from './analyzer';
import './App.css';

function App() {
  const [utilityJson, setUtilityJson] = useState('');
  const [mood, setMood] = useState({
    name: 'Neutral Stability',
    color: '#808080',
    description: 'Awaiting utility data...'
  });
  const [error, setError] = useState('');

  useEffect(() => {
    if (utilityJson.trim() === '') {
      setMood({
        name: 'Neutral Stability',
        color: '#808080',
        description: 'Awaiting utility data...'
      });
      setError('');
      return;
    }

    try {
      const parsedJson = JSON.parse(utilityJson);
      const analyzedMood = analyzeUtility(parsedJson);
      setMood(analyzedMood);
      setError('');
    } catch (e) {
      setError('Invalid JSON format. Please check your input.');
      setMood({
        name: 'Error State',
        color: '#FF0000',
        description: 'Invalid JSON provided.'
      });
    }
  }, [utilityJson]);

  const handleJsonChange = (event) => {
    setUtilityJson(event.target.value);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>ApocalypsAI Nightly Mood Ring</h1>
        <p>Paste a utility's JSON below to see its mood!</p>
      </header>
      <main>
        <div className="mood-ring-container">
          <MoodRing mood={mood} />
        </div>
        <div className="input-section">
          <textarea
            placeholder="Paste Utility JSON Here..."
            value={utilityJson}
            onChange={handleJsonChange}
            rows="15"
            cols="80"
          />
          {error && <p className="error-message">{error}</p>}
        </div>
      </main>
      <footer>
        <p>Powered by ApocalypsAI Integrator Agent</p>
      </footer>
    </div>
  );
}

export default App;
