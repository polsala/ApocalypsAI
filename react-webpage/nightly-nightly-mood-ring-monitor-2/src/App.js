import React, { useState } from 'react';
import MoodRing from './components/MoodRing';
import { analyzeSentiment, getMoodColor } from './components/SentimentAnalyzer';
import './App.css';

function App() {
  const [text, setText] = useState('');
  const score = analyzeSentiment(text);
  const color = getMoodColor(score);

  return (
    <div className="App">
      <header className="App-header">
        <h1>ApocalypsAI Nightly Mood Ring Monitor</h1>
        <p>Enter community messages, logs, or whispers from the void to gauge their emotional temperature.</p>
      </header>
      <main>
        <textarea
          placeholder="Type your message here..."
          value={text}
          onChange={(e) => setText(e.target.value)}
          rows="10"
          cols="50"
        />
        <MoodRing score={score} color={color} />
      </main>
      <footer>
        <p>&copy; 2024 ApocalypsAI Community Utility</p>
      </footer>
    </div>
  );
}

export default App;
