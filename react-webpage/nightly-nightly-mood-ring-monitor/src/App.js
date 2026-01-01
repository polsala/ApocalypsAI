import React, { useState, useEffect } from 'react';
import './App.css';
import MoodRing from './MoodRing';

function App() {
  const [logText, setLogText] = useState('');
  const [sentiment, setSentiment] = useState('neutral'); // 'positive', 'negative', 'neutral'

  const positiveKeywords = ['great', 'good', 'happy', 'success', 'thrive', 'hope', 'victory', 'safe', 'calm', 'progress', 'stable', 'secure'];
  const negativeKeywords = ['bad', 'sad', 'fail', 'danger', 'threat', 'fear', 'chaos', 'broken', 'lost', 'struggle', 'unstable', 'risk'];

  const analyzeSentiment = (text) => {
    if (!text) {
      return 'neutral';
    }
    const lowerText = text.toLowerCase();
    let positiveScore = 0;
    let negativeScore = 0;

    positiveKeywords.forEach(keyword => {
      if (lowerText.includes(keyword)) {
        positiveScore++;
      }
    });

    negativeKeywords.forEach(keyword => {
      if (lowerText.includes(keyword)) {
        negativeScore++;
      }
    });

    if (positiveScore > negativeScore) {
      return 'positive';
    } else if (negativeScore > positiveScore) {
      return 'negative';
    } else {
      return 'neutral';
    }
  };

  useEffect(() => {
    setSentiment(analyzeSentiment(logText));
  }, [logText]);

  const handleLogTextChange = (event) => {
    setLogText(event.target.value);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Nightly Mood Ring Monitor</h1>
        <p>Enter your community logs below to see the collective sentiment reflected in the mood ring.</p>
      </header>
      <main>
        <textarea
          placeholder="Paste your daily logs, whispers from the void, or community messages here..."
          value={logText}
          onChange={handleLogTextChange}
          rows="10"
          cols="50"
        ></textarea>
        <div className="mood-display">
          <MoodRing sentiment={sentiment} />
          <p>Current Mood: <span className={`sentiment-${sentiment}`}>{sentiment.toUpperCase()}</span></p>
        </div>
      </main>
      <footer>
        <p>Powered by simple keyword analysis. For entertainment purposes only. The void has feelings too!</p>
      </footer>
    </div>
  );
}

export default App;
