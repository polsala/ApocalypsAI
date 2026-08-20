import React, { useState } from 'react';
import MoodOrb from './MoodOrb';
import { analyzeSentiment } from './SentimentAnalyzer';

function App() {
  const [inputText, setInputText] = useState('');
  const [sentiment, setSentiment] = useState('neutral'); // Default sentiment

  const handleAnalyze = () => {
    const result = analyzeSentiment(inputText);
    setSentiment(result.label);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Nightly Mood Orb Calibrator</h1>
        <p>Gauge the emotional resonance of community communications.</p>
      </header>
      <main className="App-main">
        <textarea
          className="text-input"
          placeholder="Paste your message, log entry, or communication here..."
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          rows="10"
          cols="50"
        ></textarea>
        <button className="calibrate-button" onClick={handleAnalyze}>
          Calibrate Mood
        </button>
        <div className="mood-display">
          <h2>Current Resonance:</h2>
          <MoodOrb sentiment={sentiment} />
        </div>
      </main>
      <footer className="App-footer">
        <p>&copy; ApocalypsAI Community Integrator</p>
      </footer>
    </div>
  );
}

export default App;
