import React, { useState, useEffect } from 'react';
import MoodOrb from './MoodOrb';
import './App.css';

const LOCAL_STORAGE_KEY = 'apocalypsai-mood-orbs';

function App() {
  const [sentimentInput, setSentimentInput] = useState('');
  const [moodEntries, setMoodEntries] = useState([]);

  useEffect(() => {
    // # Mock rationale: localStorage is mocked in tests to ensure deterministic, offline execution.
    const storedMoods = JSON.parse(localStorage.getItem(LOCAL_STORAGE_KEY));
    if (storedMoods) {
      setMoodEntries(storedMoods);
    }
  }, []);

  useEffect(() => {
    // # Mock rationale: localStorage is mocked in tests to ensure deterministic, offline execution.
    localStorage.setItem(LOCAL_STORAGE_KEY, JSON.stringify(moodEntries));
  }, [moodEntries]);

  const handleSentimentChange = (event) => {
    const value = event.target.value;
    if (value === '' || (/^\d+$/.test(value) && parseInt(value, 10) >= 1 && parseInt(value, 10) <= 10)) {
      setSentimentInput(value);
    }
  };

  const logSentiment = () => {
    const sentiment = parseInt(sentimentInput, 10);
    if (sentiment >= 1 && sentiment <= 10) {
      setMoodEntries(prevEntries => [...prevEntries, { id: Date.now(), sentiment }]);
      setSentimentInput('');
    }
  };

  const getCollectiveResonance = () => {
    if (moodEntries.length === 0) return 'N/A';
    const lastFiveMoods = moodEntries.slice(-5); // Consider last 5 for collective resonance
    const sum = lastFiveMoods.reduce((acc, entry) => acc + entry.sentiment, 0);
    const average = sum / lastFiveMoods.length;
    return average.toFixed(1);
  };

  const getResonanceDescription = (score) => {
    if (score === 'N/A') return 'Awaiting first resonance...';
    const numScore = parseFloat(score);
    if (numScore >= 8) return 'Radiant Harmony!';
    if (numScore >= 4) return 'Steady Hum.';
    return 'Flickering Echoes...';
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Nightly Mood Orb Monitor</h1>
        <p className="subtitle">Gauge the ApocalypsAI Community Pulse</p>
      </header>
      <div className="input-section">
        <input
          type="number"
          min="1"
          max="10"
          value={sentimentInput}
          onChange={handleSentimentChange}
          placeholder="Log your sentiment (1-10)"
          aria-label="Sentiment input"
        />
        <button onClick={logSentiment} disabled={!sentimentInput}>
          Log Sentiment
        </button>
      </div>
      <div className="collective-resonance">
        <h2>Collective Resonance: {getCollectiveResonance()}</h2>
        <p className="resonance-description">{getResonanceDescription(getCollectiveResonance())}</p>
      </div>
      <div className="mood-orbs-container">
        {moodEntries.map(entry => (
          <MoodOrb key={entry.id} sentiment={entry.sentiment} />
        ))}
      </div>
    </div>
  );
}

export default App;
