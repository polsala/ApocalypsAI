import React, { useState } from 'react';
import './App.css';
import MoodRing from './MoodRing';

function App() {
  const [inputText, setInputText] = useState('');
  const [moodResult, setMoodResult] = useState(null);

  const handleAnalyze = () => {
    setMoodResult(inputText);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Nightly Wasteland Mood Ring</h1>
        <p>Gauge the emotional resonance of your post-apocalyptic thoughts.</p>
      </header>
      <main className="App-main">
        <textarea
          className="mood-input"
          placeholder="Enter your thoughts, log entries, or whispers here..."
          value={inputText}
          onChange={(e) => setInputText(e.target.value)}
          rows="5"
        ></textarea>
        <button className="analyze-button" onClick={handleAnalyze}>
          Analyze Mood
        </button>
        {moodResult && <MoodRing text={moodResult} />}
      </main>
    </div>
  );
}

export default App;
